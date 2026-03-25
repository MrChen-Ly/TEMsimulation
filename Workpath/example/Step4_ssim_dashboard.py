# -*- coding: utf-8 -*-
"""
Step 4. SSIM Dashboard — visualise how SSIM varies across the parameter sweep.

Reads:
  - config_STO.yaml  : parameter ranges (to know axis labels / units)
  - ssim_values.txt  : output of imagecompare_ssim_value4.0_128x128.py

Saves all figures to:  <DATA_FOLDER>/facebake_borad/

Usage:
    python ssim_dashboard.py [--iteration N]

When --iteration N is given, DATA_FOLDER is redirected to img/<N>/dat/ .
"""
# ═══════════════════════════════════════════════════════════════════════════════

import ast
import os
import sys

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")          # headless — no display needed
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

try:
    import yaml
except ImportError:
    sys.exit("Please install pyyaml: pip install pyyaml")

try:
    import seaborn as sns
    HAS_SEABORN = True
except ImportError:
    HAS_SEABORN = False
    print("seaborn not found — heatmaps will use plain matplotlib.")

    
# ═══════════════════════════════════════════════════════════════════════════════
# Parameters — edit these before running
# ═══════════════════════════════════════════════════════════════════════════════

# Folder that contains ssim_values.txt (same as DATA_FOLDER in imagecompare)
DATA_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), r'img\dat')

# Path to config_STO.yaml (used for axis labels and range info)
CONFIG_PATH ="config_STO.yaml"   # relative to this script, or use absolute path

# Parameter names — must match the order encoded in the .dat filenames
PARAMETER_NAMES = [
    "Tilt", "Tilta", "Cs", "Df", "Tk",
    "A1", "A1a", "A2", "A2a",
    "B2", "B2a", "Sod", "virbx", "virby",
]

# Units for each parameter (for axis labels, same order as PARAMETER_NAMES)
PARAMETER_UNITS = {
    "Tilt":  "mrad", "Tilta": "deg",
    "Cs":    "um",   "Df":    "nm",  "Tk":  "nm",
    "A1":    "nm",   "A1a":   "deg",
    "A2":    "nm",   "A2a":   "deg",
    "B2":    "nm",   "B2a":   "deg",
    "Sod":   "nm",   "virbx": "nm",  "virby": "nm",
}

# Aggregation used when collapsing other dimensions for 1D / 2D plots
# "max"  — best SSIM achievable at that parameter value
# "mean" — average SSIM at that parameter value
AGGREGATE = "max"




# ── Helpers ───────────────────────────────────────────────────────────────────

def load_config(config_path):
    if not os.path.isabs(config_path):
        config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), config_path)
    if not os.path.exists(config_path):
        sys.exit(f"Config file not found: {config_path}")
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_ssim_data(data_folder, param_names):
    """Parse ssim_values.txt into a DataFrame.  Last column is SSIM."""
    txt_path = os.path.join(data_folder, "ssim_values.txt")
    if not os.path.exists(txt_path):
        sys.exit(f"ssim_values.txt not found in: {data_folder}")

    rows = []
    with open(txt_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                values = ast.literal_eval(line)
                rows.append(values)
            except Exception:
                pass   # skip malformed lines

    if not rows:
        sys.exit("ssim_values.txt is empty or could not be parsed.")

    # Each row: [p0, p1, ..., pN-1, ssim]
    cols = param_names[:len(rows[0]) - 1] + ["SSIM"]
    df = pd.DataFrame(rows, columns=cols)
    df = df.drop_duplicates()
    return df


def active_params(df, param_names):
    """Return parameters that have more than one unique value in the data."""
    return [p for p in param_names if p in df.columns and df[p].nunique() > 1]


def param_label(name):
    unit = PARAMETER_UNITS.get(name, "")
    return f"{name} ({unit})" if unit else name


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def agg(series):
    return series.max() if AGGREGATE == "max" else series.mean()


# ── 1-D plots: SSIM vs each active parameter ─────────────────────────────────

def plot_1d(df, active, out_dir):
    """One figure per active parameter showing SSIM vs that parameter."""
    for param in active:
        grouped = df.groupby(param)["SSIM"]
        x      = np.array(sorted(df[param].unique()))
        y_agg  = np.array([agg(grouped.get_group(v)) for v in x])
        y_mean = np.array([grouped.get_group(v).mean() for v in x])
        y_std  = np.array([grouped.get_group(v).std(ddof=0) for v in x])

        fig, ax = plt.subplots(figsize=(7, 4))
        ax.plot(x, y_agg,  "o-",  color="steelblue", label=f"SSIM ({AGGREGATE})", zorder=3)
        ax.fill_between(x, y_mean - y_std, y_mean + y_std,
                        alpha=0.25, color="steelblue", label="mean ± std")
        ax.plot(x, y_mean, "--",  color="steelblue", alpha=0.6, linewidth=1)

        best_idx = np.argmax(y_agg)
        ax.axvline(x[best_idx], color="tomato", linestyle=":", linewidth=1.2,
                   label=f"best = {x[best_idx]:.4g}")

        ax.set_xlabel(param_label(param), fontsize=11)
        ax.set_ylabel("SSIM", fontsize=11)
        ax.set_title(f"SSIM vs {param}", fontsize=13)
        ax.legend(fontsize=9)
        ax.grid(True, alpha=0.3)
        fig.tight_layout()
        fig.savefig(os.path.join(out_dir, f"1d_{param}.png"), dpi=150)
        plt.close(fig)
        print(f"  Saved: 1d_{param}.png")


# ── Summary grid: all 1-D plots on one page ──────────────────────────────────

def plot_1d_grid(df, active, out_dir):
    n = len(active)
    if n == 0:
        return
    ncols = min(3, n)
    nrows = (n + ncols - 1) // ncols
    fig, axes = plt.subplots(nrows, ncols, figsize=(5 * ncols, 3.5 * nrows))
    axes = np.array(axes).flatten()

    for i, param in enumerate(active):
        ax = axes[i]
        grouped = df.groupby(param)["SSIM"]
        x     = np.array(sorted(df[param].unique()))
        y_agg = np.array([agg(grouped.get_group(v)) for v in x])
        y_mean = np.array([grouped.get_group(v).mean() for v in x])
        y_std  = np.array([grouped.get_group(v).std(ddof=0) for v in x])

        ax.plot(x, y_agg, "o-", color="steelblue", linewidth=1.5, markersize=4)
        ax.fill_between(x, y_mean - y_std, y_mean + y_std, alpha=0.2, color="steelblue")
        best_idx = np.argmax(y_agg)
        ax.axvline(x[best_idx], color="tomato", linestyle=":", linewidth=1)
        ax.set_xlabel(param_label(param), fontsize=9)
        ax.set_ylabel("SSIM", fontsize=9)
        ax.set_title(param, fontsize=10)
        ax.grid(True, alpha=0.3)

    for j in range(i + 1, len(axes)):
        axes[j].set_visible(False)

    fig.suptitle(f"SSIM vs each parameter  (aggregation: {AGGREGATE})", fontsize=13)
    fig.tight_layout()
    fig.savefig(os.path.join(out_dir, "summary_1d_grid.png"), dpi=150)
    plt.close(fig)
    print("  Saved: summary_1d_grid.png")


# ── 2-D heatmaps: SSIM for every pair of active parameters ───────────────────

def plot_2d_heatmaps(df, active, out_dir):
    if len(active) < 2:
        return

    pairs = [(active[i], active[j])
             for i in range(len(active))
             for j in range(i + 1, len(active))]

    for px, py in pairs:
        pivot = df.groupby([px, py])["SSIM"].agg(
            "max" if AGGREGATE == "max" else "mean"
        ).unstack(level=py)

        fig, ax = plt.subplots(figsize=(max(6, len(pivot.columns) * 0.8 + 2),
                                        max(5, len(pivot.index) * 0.6 + 2)))
        if HAS_SEABORN:
            sns.heatmap(pivot, ax=ax, cmap="viridis", annot=(pivot.size <= 100),
                        fmt=".3f", linewidths=0.3 if pivot.size <= 100 else 0,
                        cbar_kws={"label": f"SSIM ({AGGREGATE})"})
        else:
            im = ax.imshow(pivot.values, aspect="auto", cmap="viridis",
                           origin="lower")
            ax.set_xticks(range(len(pivot.columns)))
            ax.set_xticklabels([f"{v:.3g}" for v in pivot.columns], rotation=45, ha="right")
            ax.set_yticks(range(len(pivot.index)))
            ax.set_yticklabels([f"{v:.3g}" for v in pivot.index])
            fig.colorbar(im, ax=ax, label=f"SSIM ({AGGREGATE})")

        ax.set_xlabel(param_label(py), fontsize=11)
        ax.set_ylabel(param_label(px), fontsize=11)
        ax.set_title(f"SSIM: {px} vs {py}", fontsize=13)
        fig.tight_layout()
        fname = f"2d_{px}_vs_{py}.png"
        fig.savefig(os.path.join(out_dir, fname), dpi=150)
        plt.close(fig)
        print(f"  Saved: {fname}")


# ── Best-match summary text ───────────────────────────────────────────────────

def save_best_summary(df, param_names, out_dir):
    best_row = df.loc[df["SSIM"].idxmax()]
    lines = ["Best parameter combination (highest SSIM)\n",
             "=" * 45 + "\n"]
    for p in param_names:
        if p in best_row.index:
            lines.append(f"  {p:10s}: {best_row[p]:.6g}\n")
    lines.append(f"  {'SSIM':10s}: {best_row['SSIM']:.6f}\n")
    txt_path = os.path.join(out_dir, "best_parameters.txt")
    with open(txt_path, "w") as f:
        f.writelines(lines)
    print("  Saved: best_parameters.txt")
    print("".join(lines))


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    cfg     = load_config(CONFIG_PATH)
    df      = load_ssim_data(DATA_FOLDER, PARAMETER_NAMES)
    active  = active_params(df, PARAMETER_NAMES)
    out_dir = os.path.join(DATA_FOLDER, "facebake_borad")
    ensure_dir(out_dir)

    print(f"Loaded {len(df)} data points from ssim_values.txt")
    print(f"Active parameters ({len(active)}): {active}")
    print(f"Output folder: {out_dir}\n")

    print("Generating 1D plots...")
    plot_1d(df, active, out_dir)

    print("Generating summary grid...")
    plot_1d_grid(df, active, out_dir)

    print("Generating 2D heatmaps...")
    plot_2d_heatmaps(df, active, out_dir)

    print("Saving best-match summary...")
    save_best_summary(df, PARAMETER_NAMES, out_dir)

    print(f"\nDone. All figures saved to: {out_dir}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--iteration", type=int, default=None,
                        help="Iteration index; reads from img/<N>/dat/")
    args = parser.parse_args()

    if args.iteration is not None:
        _parent = os.path.dirname(DATA_FOLDER.rstrip("/\\"))
        DATA_FOLDER = os.path.join(_parent, str(args.iteration), "dat")

    main()
