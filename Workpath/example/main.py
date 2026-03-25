"""
TEM Simulation — Iterative Refinement Pipeline

Steps per iteration:
  1  TEMsimulation5.py                     initial setup test          (once)
  2  setdata3.0with_deadline_vibration.py  parameter sweep simulation
  3  imagecompare_ssim_value4.0.py SSIM calculation
  4  ssim_dashboard.py                     visualisation
  5  (internal)                            range analysis → config update

Group-based optimization strategy (Plan B):
  Parameters are split into 3 groups.  Each iteration sweeps ONE group while
  all other parameters are fixed at their best known values.  This keeps the
  combination count bounded regardless of parameter count.

  Group 0 — main imaging:    Cs  Df  Tk  Tilt  Tilta
  Group 1 — primary aberr.:  A1  A1a  A2  A2a
  Group 2 — secondary + vib: B2  B2a  Sod  virbx  virby

  Angle parameters (Tilta, A1a, A2a, B2a) always sweep the full 0–360 °
  when their group is active; fixed at best known value otherwise.

  Non-angle active parameters are narrowed ×0.5 range / ÷2 step each round,
  clamped to the initial range bounds so values stay physically meaningful.

Usage:
    python main.py
"""

import ast
import json
import os
import re
import subprocess
import sys

import numpy as np

try:
    import yaml
except ImportError:
    sys.exit("Please install pyyaml: pip install pyyaml")

# ═══════════════════════════════════════════════════════════════════════════════
# Settings — edit these before running
# ═══════════════════════════════════════════════════════════════════════════════

MAX_ITERATIONS = 12   # should be a multiple of 3 to complete full group cycles

# Max discrete values per active parameter per iteration.
# Total combinations ≈ MAX_POINTS_PER_PARAM ^ (active non-angle params)
#                    × (360 / angle_step) ^ (active angle params)
#
# Target: ≤ ~3 000 combos per iteration (≈ 5 min @ 10 img/s)
# Example with group size 3 non-angle + 1 angle (step=90):
#   5^3 × 4 = 500 combos ≈ 50 s  ✓
MAX_POINTS_PER_PARAM = 5

# Parameter groups — cycled round-robin across iterations.
# Keep group sizes ≤ 5 for manageable combination counts.
PARAM_GROUPS = [
    ["Cs", "Df", "Tk", "Tilt", "Tilta"],    # Group 0: main imaging params
    ["A1", "A1a", "A2", "A2a"],              # Group 1: primary aberrations
    ["B2", "B2a", "Sod", "virbx", "virby"], # Group 2: secondary + vibration
]

# Angle parameters always sweep the full 0–360 ° when their group is active.
# Keep angle steps coarse (≥ 30 °) to limit combination counts.
ANGLE_PARAMS    = {"Tilta", "A1a", "A2a", "B2a"}
ANGLE_STEP_DEG  = 45.0     # step for all angle params → 360/45 + 1 = 9 points

# ── Physical parameter ranges ──────────────────────────────────────────────
# Derived from physical constraints of the instrument and specimen.
# These are written into config_STO.yaml at startup (once per fresh run).
# Non-angle params: step is auto-computed so the range contains exactly
#   MAX_POINTS_PER_PARAM points.
# Angle params: always 0–360 °, step = ANGLE_STEP_DEG.
# Fixed params: start == end (set to a single value, no sweep).
#
# Format: param_name → (start, end)   or   param_name → fixed_value
#
PHYSICAL_RANGES = {
    # name    start    end
    "Cs":   (-15.0,  -10.0),    # Spherical aberration (um)  — keep negative
    "Df":   (  0.0,   5.0),    # Defocus (nm)
    "Tk":   (  2.0,   5.0),    # Thickness (nm)
    "Tilt": (  0.0,   5.0),    # Tilt magnitude (mrad)
    "Tilta": None,             # angle → 0–360 °
    "A1":   (  0.0,   1.0),    # 2-fold astigmatism (nm)
    "A1a":  None,              # angle → 0–360 °
    "A2":   ( 50.0, 100.0),    # 3-fold astigmatism (nm)
    "A2a":  None,              # angle → 0–360 °
    "B2":   ( 50.0, 100.0),    # Axial coma (nm)
    "B2a":  None,              # angle → 0–360 °
    "Sod":  2.5,               # Source diameter (nm) — fixed
    "virbx":(  0.0,   0.05),    # Vibration x (nm)
    "virby":(  0.0,   0.05),    # Vibration y (nm)
}

SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(SCRIPT_DIR, "config_STO.yaml")

# Persistent state: best known values + initial ranges, survives across runs.
STATE_FILE  = os.path.join(SCRIPT_DIR, "pipeline_state.json")

# Parameter names in the ORDER they appear as columns in ssim_values.txt.
# Must match PARAMETER_NAMES in Step3_imagecompare_ssim_value4.0.py.
PARAM_COLUMN_ORDER = [
    "Tilt", "Tilta", "Cs", "Df", "Tk",
    "A1", "A1a", "A2", "A2a",
    "B2", "B2a", "Sod", "virbx", "virby",
]

# ═══════════════════════════════════════════════════════════════════════════════


# ── Persistent state helpers ──────────────────────────────────────────────────

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"best_values": {}, "initial_ranges": {}}


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


# ── Subprocess helper ─────────────────────────────────────────────────────────

def run_script(script_name, *args):
    cmd = [sys.executable, os.path.join(SCRIPT_DIR, script_name)] + list(str(a) for a in args)
    sep = "=" * 64
    print(f"\n{sep}\nRunning: {' '.join(cmd)}\n{sep}")
    result = subprocess.run(cmd, cwd=SCRIPT_DIR)
    if result.returncode != 0:
        print(f"[WARNING] {script_name} exited with code {result.returncode}")
    return result.returncode


# ── Pipeline steps ────────────────────────────────────────────────────────────

def step1():
    """Initial setup test — runs TEMsimulation5 once with the base config."""
    print("\n" + "▶" * 3 + " STEP 1 — Initial setup test")
    run_script("Step1_TEMsimulation5.py", "--config", os.path.join(SCRIPT_DIR, "config.yaml"))


def step2(iteration):
    """Parameter sweep simulation for this iteration."""
    print(f"\n" + "▶" * 3 + f" STEP 2 — Dataset simulation  (iteration {iteration})")
    run_script(
        "Step2_setdata3.0with_deadline_vibration.py",
        "--config", CONFIG_FILE,
        "--iteration", iteration,
    )


def step3(iteration):
    """SSIM comparison — simulated vs experimental."""
    print(f"\n" + "▶" * 3 + f" STEP 3 — SSIM comparison  (iteration {iteration})")
    run_script(
        "Step3_imagecompare_ssim_value4.0_128x128.py",
        "--iteration", iteration,
    )


def step4(iteration):
    """SSIM dashboard — save visualisations."""
    print(f"\n" + "▶" * 3 + f" STEP 4 — SSIM dashboard  (iteration {iteration})")
    run_script(
        "Step4_ssim_dashboard.py",
        "--iteration", iteration,
    )


# ── Physical range initialisation ────────────────────────────────────────────

def init_physical_ranges():
    """
    Write PHYSICAL_RANGES into config_STO.yaml before the first sweep.

    Rules per parameter:
      • Angle (None in PHYSICAL_RANGES): start=0, end=360, step=ANGLE_STEP_DEG
      • Fixed (scalar in PHYSICAL_RANGES): start=end=value, step=1
      • Range (tuple): start/end from dict; step = span / (MAX_POINTS_PER_PARAM-1)
        so the initial sweep contains exactly MAX_POINTS_PER_PARAM evenly-spaced
        values across the full physical range.

    All other fields in config_STO.yaml (work_path, slc_name, …) are preserved.
    """
    print("\n" + "▶" * 3 + " INIT — Writing physical parameter ranges to config_STO.yaml")

    with open(CONFIG_FILE) as f:
        config_text = f.read()

    print(f"\n  {'Parameter':<10}  {'Type':<7}  [start, end, step]")
    print("  " + "-" * 50)

    for param_name, bounds in PHYSICAL_RANGES.items():

        if bounds is None:
            # Angle parameter — full sweep
            step = ANGLE_STEP_DEG
            new_start, new_end = 0.0, 360.0
            n = int((new_end - new_start) / step) + 1
            label = f"angle    [0, 360, {step:.4g}]  ({n} pts)"

        elif isinstance(bounds, (int, float)):
            # Fixed parameter
            new_start = new_end = float(bounds)
            step = 1.0
            label = f"fixed    {new_start:.4g}"

        else:
            # Swept range — evenly space MAX_POINTS_PER_PARAM points
            lo, hi = float(bounds[0]), float(bounds[1])
            new_start, new_end = lo, hi
            span = hi - lo
            step = span / (MAX_POINTS_PER_PARAM - 1) if span > 0 else 1.0
            n = MAX_POINTS_PER_PARAM
            label = f"range    [{new_start:.4g}, {new_end:.4g}, {step:.4g}]  ({n} pts)"

        config_text = update_range_in_yaml(
            config_text, param_name, new_start, new_end, step)
        print(f"  {param_name:<10}  {label}")

    with open(CONFIG_FILE, "w") as f:
        f.write(config_text)

    print(f"\n  config_STO.yaml updated with physical ranges.")


# ── YAML range update (preserves inline comments) ─────────────────────────────

def update_range_in_yaml(text, key, new_start, new_end, new_step):
    """
    Replace start/end/step values for *key* inside inline-dict YAML entries
    like:   Cs:  { start: -15.0, end: 0.0, step: 0.5 }   # comment
    The trailing comment is preserved.
    """
    pattern = (
        rf'(^{re.escape(key)}:\s*\{{)'      # key: {
        rf'\s*start:\s*[-\d.e+]+,'           # start: X,
        rf'\s*end:\s*[-\d.e+]+,'             # end: Y,
        rf'\s*step:\s*[-\d.e+]+'             # step: Z
    )
    replacement = (
        rf'\g<1>'
        rf' start: {new_start:.6g},'
        rf' end: {new_end:.6g},'
        rf' step: {new_step:.6g}'
    )
    return re.sub(pattern, replacement, text, flags=re.MULTILINE)


# ── Step 0: initialise config for Group 0 before first sweep ──────────────────

def init_group_sweep():
    """
    Run once before iteration 1.
    • Records every parameter's initial range in pipeline_state.json.
    • Configures config_STO.yaml so that:
        - Group 0 non-angle params: sweep their initial range (capped at
          MAX_POINTS_PER_PARAM points; range must stay within same order of
          magnitude as the centre value — set sensible values in config_STO.yaml)
        - Group 0 angle params: sweep 0–360 ° at their initial step
        - All other params: fixed at range centre
    """
    print("\n" + "▶" * 3 + " INIT — Configuring Group 0 sweep for iteration 1")

    with open(CONFIG_FILE) as f:
        cfg = yaml.safe_load(f)
    with open(CONFIG_FILE) as f:
        config_text = f.read()

    state = load_state()
    init_ranges = state.setdefault("initial_ranges", {})
    best_known  = state.setdefault("best_values", {})

    group_0 = set(PARAM_GROUPS[0])

    print(f"\n  {'Parameter':<10}  {'Action':<8}  value / range")
    print("  " + "-" * 52)

    for param_name in PARAM_COLUMN_ORDER:
        if param_name not in cfg:
            continue

        entry     = cfg[param_name]
        p_start   = float(entry["start"])
        p_end     = float(entry["end"])
        p_step    = float(entry["step"])
        center    = (p_start + p_end) / 2.0

        # Record initial range on first call
        if param_name not in init_ranges:
            init_ranges[param_name] = {
                "start": p_start, "end": p_end, "step": p_step
            }

        # Initialise best_known to range centre
        if param_name not in best_known:
            best_known[param_name] = center

        if param_name in ANGLE_PARAMS and param_name in group_0:
            # Active angle param: sweep full circle
            config_text = update_range_in_yaml(
                config_text, param_name, 0.0, 360.0, p_step)
            n = int(360.0 / p_step) + 1
            print(f"  {param_name:<10}  sweep    0–360 °  step={p_step:.4g}  ({n} pts)")

        elif param_name in group_0:
            # Active non-angle param: keep initial range, enforce point cap
            new_start, new_end, new_step = p_start, p_end, p_step
            span = new_end - new_start
            if new_step > 0 and span > 0:
                n_pts = round(span / new_step) + 1
                if n_pts > MAX_POINTS_PER_PARAM:
                    new_step = span / (MAX_POINTS_PER_PARAM - 1)
            new_step = max(new_step, 1e-9)
            config_text = update_range_in_yaml(
                config_text, param_name, new_start, new_end, new_step)
            n_pts = round((new_end - new_start) / new_step) + 1 if new_step > 0 else 1
            print(f"  {param_name:<10}  sweep    [{new_start:.4g}, {new_end:.4g}]  "
                  f"step={new_step:.4g}  ({n_pts} pts)")

        else:
            # Inactive param: fix at centre
            config_text = update_range_in_yaml(
                config_text, param_name, center, center, p_step)
            print(f"  {param_name:<10}  fixed    {center:.4g}")

    state["initial_ranges"] = init_ranges
    state["best_values"]    = best_known
    save_state(state)

    with open(CONFIG_FILE, "w") as f:
        f.write(config_text)

    print(f"\n  config_STO.yaml written for Group 0: {sorted(group_0)}")
    print(f"  State saved → {STATE_FILE}")


# ── Step 5: range analysis → config update for next iteration ─────────────────

def load_ssim_txt(path):
    """Parse ssim_values.txt into a 2-D numpy array (rows × columns)."""
    rows = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    rows.append(ast.literal_eval(line))
                except Exception:
                    pass
    if not rows:
        return None
    return np.array(rows)


def step5(iteration):
    """
    Analyse SSIM results from *iteration*.
    • Determines the next group to sweep (round-robin).
    • Updates best known values from current iteration's results.
    • Rewrites config_STO.yaml:
        - Next group non-angle params: narrowed range (÷2) around best value,
          clamped to initial bounds, capped at MAX_POINTS_PER_PARAM.
        - Next group angle params: full 0–360 ° at initial step.
        - All other params: fixed at best known value.
    """
    next_iter  = iteration + 1
    group_idx  = (iteration) % len(PARAM_GROUPS)   # 0-based: iter1→group1, iter2→group2 …
    active_group = set(PARAM_GROUPS[group_idx])

    print(f"\n" + "▶" * 3 +
          f" STEP 5 — Range analysis  (iter {iteration} → {next_iter},"
          f" sweeping Group {group_idx + 1}: {sorted(active_group)})")

    # ── load SSIM data ────────────────────────────────────────────────────────
    with open(CONFIG_FILE) as f:
        cfg = yaml.safe_load(f)

    work_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + os.sep
    ssim_txt  = os.path.join(work_path, "img", str(iteration), "dat", "ssim_values.txt")

    if not os.path.exists(ssim_txt):
        print(f"  [SKIP] ssim_values.txt not found: {ssim_txt}")
        return

    data = load_ssim_txt(ssim_txt)
    if data is None or len(data) == 0:
        print("  [SKIP] No valid SSIM data found.")
        return

    ssim_col  = data[:, -1]
    best_ssim = ssim_col.max()
    print(f"  Best SSIM this iteration: {best_ssim:.6f}")

    if best_ssim >= 0.99:
        print("  SSIM ≥ 0.99 — convergence reached, skipping range update.")
        return

    # ── load persistent state ─────────────────────────────────────────────────
    state       = load_state()
    best_known  = state["best_values"]
    init_ranges = state["initial_ranges"]

    # ── update best known values from this iteration's results ───────────────
    for col_idx, param_name in enumerate(PARAM_COLUMN_ORDER):
        if param_name not in cfg:
            continue
        param_vals  = data[:, col_idx]
        unique_vals = np.unique(param_vals)
        if len(unique_vals) > 1:
            best_val = float(unique_vals[
                np.argmax([ssim_col[param_vals == v].mean() for v in unique_vals])
            ])
        elif len(unique_vals) == 1:
            best_val = float(unique_vals[0])
        else:
            continue
        best_known[param_name] = best_val

    # ── build new config ──────────────────────────────────────────────────────
    with open(CONFIG_FILE) as f:
        config_text = f.read()

    print(f"\n  {'Parameter':<10}  {'Action':<8}  new [start, end, step]")
    print("  " + "-" * 58)

    for param_name in PARAM_COLUMN_ORDER:
        if param_name not in cfg:
            continue

        entry    = cfg[param_name]
        cur_start = float(entry["start"])
        cur_end   = float(entry["end"])
        cur_step  = float(entry["step"])

        ir        = init_ranges.get(param_name, {
            "start": cur_start, "end": cur_end, "step": cur_step
        })
        best_val  = best_known.get(param_name,
                                   (float(ir["start"]) + float(ir["end"])) / 2.0)

        # ── active group param: narrow range around best value ───────────────
        # Applies to both angle and non-angle params.
        # Angle params: initial range is 0–360; no bound clamping (periodic).
        # Non-angle params: clamped to initial physical bounds.
        if param_name in active_group:
            # If currently fixed (was inactive last round), restore from initial range
            if cur_start == cur_end:
                old_half     = (float(ir["end"]) - float(ir["start"])) / 2.0
                old_step_ref = float(ir["step"])
            else:
                old_half     = (cur_end - cur_start) / 2.0
                old_step_ref = cur_step

            new_half  = old_half / 2.0
            new_step  = old_step_ref / 2.0
            new_start = best_val - new_half
            new_end   = best_val + new_half

            # Non-angle params: clamp to initial physical bounds
            if param_name not in ANGLE_PARAMS:
                new_start = max(new_start, float(ir["start"]))
                new_end   = min(new_end,   float(ir["end"]))

            # Cap points per parameter
            if new_step > 0 and (new_end - new_start) > 0:
                n_pts = round((new_end - new_start) / new_step) + 1
                if n_pts > MAX_POINTS_PER_PARAM:
                    new_step = (new_end - new_start) / (MAX_POINTS_PER_PARAM - 1)
            new_step = max(new_step, 1e-9)

            config_text = update_range_in_yaml(
                config_text, param_name, new_start, new_end, new_step)
            n_pts = round((new_end - new_start) / new_step) + 1 if new_step > 0 else 1
            tag = "angle" if param_name in ANGLE_PARAMS else "narrow"
            print(f"  {param_name:<10}  {tag:<8} [{new_start:.4g}, {new_end:.4g}, {new_step:.4g}]"
                  f"  best={best_val:.4g}  ({n_pts} pts)")

        # ── all other params: fix at best known value ─────────────────────────
        else:
            config_text = update_range_in_yaml(
                config_text, param_name, best_val, best_val, cur_step)
            print(f"  {param_name:<10}  fixed    {best_val:.4g}")

    # ── save ──────────────────────────────────────────────────────────────────
    state["best_values"] = best_known
    save_state(state)

    with open(CONFIG_FILE, "w") as f:
        f.write(config_text)

    print(f"\n  config_STO.yaml updated for iteration {next_iter}.")
    print(f"  State saved → {STATE_FILE}")


# ── Final summary plot ────────────────────────────────────────────────────────

def plot_ssim_progression():
    """
    Generate one summary figure after all iterations.

    Layout: one subplot per iteration.
      - Within each iteration, all SSIM values are sorted ascending and
        plotted as a line (rank on x-axis, SSIM on y-axis).
      - From iteration 2 onward, only simulations whose SSIM exceeds the
        previous iteration's best are shown (the rest are greyed out).
      - A horizontal dashed threshold line marks where each new iteration
        must improve upon.

    Saved to: <work_path>/ssim_progression.png
    """
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import matplotlib.gridspec as gridspec
    except ImportError:
        print("  [SKIP] matplotlib not available — skipping progression plot.")
        return

    with open(CONFIG_FILE) as f:
        cfg = yaml.safe_load(f)
    work_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + os.sep

    # ── collect data ──────────────────────────────────────────────────────────
    all_ssim = {}          # iteration → full array of SSIM values
    for it in range(1, MAX_ITERATIONS + 1):
        txt = os.path.join(work_path, "img", str(it), "dat", "ssim_values.txt")
        if not os.path.exists(txt):
            continue
        data = load_ssim_txt(txt)
        if data is not None and len(data):
            all_ssim[it] = np.sort(data[:, -1])   # sorted ascending

    if not all_ssim:
        print("  [SKIP] No SSIM data found for progression plot.")
        return

    iterations = sorted(all_ssim.keys())
    n_iters    = len(iterations)

    # ── colour palette (one colour per iteration) ─────────────────────────────
    cmap   = plt.cm.plasma
    colors = {it: cmap(0.15 + 0.7 * (i / max(n_iters - 1, 1)))
              for i, it in enumerate(iterations)}

    # ── figure: one panel per iteration, stacked vertically ──────────────────
    fig = plt.figure(figsize=(11, 3.2 * n_iters))
    gs  = gridspec.GridSpec(n_iters, 1, hspace=0.55)

    prev_best = None

    for panel_idx, it in enumerate(iterations):
        ax     = fig.add_subplot(gs[panel_idx])
        ssim   = all_ssim[it]              # sorted ascending
        n_all  = len(ssim)
        group_idx  = (it - 1) % len(PARAM_GROUPS)
        group_name = ", ".join(PARAM_GROUPS[group_idx])

        # ── grey background: all simulations this iteration ───────────────────
        ax.fill_between(np.arange(1, n_all + 1), ssim,
                        alpha=0.12, color=colors[it], linewidth=0)
        ax.plot(np.arange(1, n_all + 1), ssim,
                color="lightgrey", linewidth=0.8, zorder=1,
                label=f"all simulations (n={n_all})")

        # ── threshold line from previous best ────────────────────────────────
        if prev_best is not None:
            ax.axhline(prev_best, color="tomato", linestyle="--",
                       linewidth=1.2, zorder=2,
                       label=f"prev best = {prev_best:.4f}")

        # ── highlighted: only simulations above previous best ────────────────
        if prev_best is not None:
            mask    = ssim > prev_best
            hi_ssim = ssim[mask]
        else:
            hi_ssim = ssim

        if len(hi_ssim):
            x_hi = np.arange(n_all - len(hi_ssim) + 1, n_all + 1)
            ax.plot(x_hi, hi_ssim,
                    color=colors[it], linewidth=2.0, zorder=3,
                    label=f"above threshold (n={len(hi_ssim)})")
            ax.scatter([x_hi[-1]], [hi_ssim[-1]],
                       color=colors[it], s=70, zorder=5)
            # annotate best SSIM of this iteration
            ax.annotate(f"  best = {hi_ssim[-1]:.4f}",
                        xy=(x_hi[-1], hi_ssim[-1]),
                        fontsize=8.5, color=colors[it],
                        va="center")

        ax.set_xlim(0, n_all + 1)
        y_lo = (prev_best - 0.05) if prev_best is not None else max(ssim.min() - 0.05, 0)
        ax.set_ylim(max(y_lo, 0), min(ssim.max() + 0.05, 1.0))
        ax.set_xlabel("Simulation rank (sorted by SSIM ↑)", fontsize=9)
        ax.set_ylabel("SSIM", fontsize=9)
        ax.set_title(
            f"Iteration {it}  —  Group {group_idx + 1}: [{group_name}]",
            fontsize=10, fontweight="bold")
        ax.legend(fontsize=8, loc="upper left")
        ax.grid(True, alpha=0.25)

        prev_best = float(ssim[-1])   # update threshold for next panel

    fig.suptitle("SSIM Progression Across Iterations\n"
                 "highlighted: simulations that surpass previous iteration's best",
                 fontsize=12, y=1.01)

    out_path = os.path.join(work_path, "ssim_progression.png")
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"\n  SSIM progression plot saved → {out_path}")


# ── Main loop ─────────────────────────────────────────────────────────────────

def main():
    n_groups = len(PARAM_GROUPS)
    print("╔" + "═" * 62 + "╗")
    print("║  TEM Iterative Refinement Pipeline — Group Rotation         ║")
    print(f"║  MAX_ITERATIONS = {MAX_ITERATIONS:<3}  ({MAX_ITERATIONS // n_groups} full cycles × {n_groups} groups)  "
          f"{'':>14}║")
    print("╚" + "═" * 62 + "╝")

    # Step 1 runs once
    step1()

    # Write physical bounds into config_STO.yaml, then restrict to Group 0
    init_physical_ranges()
    init_group_sweep()

    for iteration in range(1, MAX_ITERATIONS + 1):
        group_idx = (iteration - 1) % n_groups
        print(f"\n{'━'*64}")
        print(f"  ITERATION {iteration} / {MAX_ITERATIONS}"
              f"  —  Group {group_idx + 1}: {PARAM_GROUPS[group_idx]}")
        print(f"{'━'*64}")

        step2(iteration)
        step3(iteration)
        step4(iteration)

        if iteration < MAX_ITERATIONS:
            step5(iteration)
        else:
            print(f"\n  Final iteration complete — no further range update needed.")

    print("\n" + "▶" * 3 + " FINAL — SSIM progression plot")
    plot_ssim_progression()

    print("\n" + "═" * 64)
    print("  Pipeline finished.  Results in img/1/ … img/%d/" % MAX_ITERATIONS)
    print(f"  Best parameter values saved in: {STATE_FILE}")
    print(f"  Summary plot:       <work_path>/ssim_progression.png")
    print("═" * 64)


if __name__ == "__main__":
    main()
