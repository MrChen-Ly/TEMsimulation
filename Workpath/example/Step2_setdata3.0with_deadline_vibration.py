"""
Step 2. TEM Simulation — STO parameter sweep with vibration (no GUI)

Usage:
    python setdata3.0with_deadline_vibration.py [--config config_STO.yaml] [--iteration N]

All parameters are read from the config file; no manual input required.
When --iteration N is given, output .dat files are written to img\<N>\dat\ .
"""

import itertools
import math
import subprocess
import argparse
import sys
import os

import tifffile as tiff
import numpy as np
from tqdm import tqdm

try:
    import yaml
except ImportError:
    sys.exit("Please install pyyaml first: pip install pyyaml")

# ── Global state set once from config ────────────────────────────────────────
workingDir = ""
slcname    = ""
heightval  = 0
widthval   = 0


# ── Config loading ────────────────────────────────────────────────────────────

def load_config(config_path="config_STO.yaml"):
    if not os.path.isabs(config_path):
        config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), config_path)
    if not os.path.exists(config_path):
        sys.exit(f"Config file not found: {config_path}")
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


# ── Range helper ─────────────────────────────────────────────────────────────

def rangetodata(data_st, data_end, data_step):
    data = []
    num = round((data_end - data_st) / data_step) + 1
    for i in range(num):
        data.append(data_st + data_step * i)
    return data


def range_from_cfg(entry):
    """Build a value list from a config dict with keys start / end / step."""
    return rangetodata(float(entry["start"]), float(entry["end"]), float(entry["step"]))


# ── Coordinate helpers ────────────────────────────────────────────────────────

def polar_to_cartesian(r, theta):
    theta_rad = math.radians(theta)
    x = round(r * math.cos(theta_rad), 6)
    y = round(r * math.sin(theta_rad), 6)
    return x, y


# ── File patching utilities ───────────────────────────────────────────────────

def replace_single_line_in_file(file_path, line_number, new_line, new_path):
    with open(file_path, "r") as f:
        lines = f.readlines()
    if line_number <= len(lines):
        lines[line_number - 1] = new_line + "\n"
    else:
        print(f"Line number {line_number} exceeds total lines in file!")
    with open(new_path, "w") as f:
        f.writelines(lines)


def replace_lines(file_path, start_line, end_line, new_content, new_path):
    with open(file_path, "r") as f:
        lines = f.readlines()
    if start_line <= len(lines):
        lines[start_line - 1 : end_line - 1] = new_content
    with open(new_path, "w") as f:
        f.writelines(lines)


# ── Image I/O ─────────────────────────────────────────────────────────────────

def read_binary_file(file_path, height, width):
    image_data = np.fromfile(file_path, dtype=np.float32).reshape((height, width))
    return image_data


def export_to_tiff(file_path, height, width, output_folder):
    image_data = read_binary_file(file_path, height, width)
    file_name  = os.path.splitext(os.path.basename(file_path))[0]
    output_path = os.path.join(output_folder, f"{file_name}.tif")
    tiff.imsave(output_path, image_data)


def batch_export_to_tiff(input_folder, output_folder, height, width):
    file_paths = [
        os.path.join(input_folder, fn)
        for fn in os.listdir(input_folder)
        if fn.endswith(".dat")
    ]
    for file_path in file_paths:
        export_to_tiff(file_path, height, width, output_folder)


# ── Simulation core ───────────────────────────────────────────────────────────

def runwav():
    """Run wavimg for the current slcname."""
    cmd = (
        f"cd /d {workingDir}&& {workingDir[:2]} && "
        f"wavimg -prm prm\\wavimg_{slcname}.prm /nli"
    )
    log_path = os.path.join(workingDir, "RumLog.txt")
    with open(log_path, "w") as f:
        subprocess.run(cmd, shell=True, check=True, stdout=f, text=True)


def msachange(tilt, tilta):
    """Patch the msa .prm file with the given tilt values."""
    tilt_scaled = tilt * (0.18 / math.pi)
    tiltx, tilty = polar_to_cartesian(tilt_scaled, tilta)
    prm = workingDir + "prm\\msa_%s.prm" % slcname
    replace_single_line_in_file(prm, 13, "%f" % tiltx, prm)
    replace_single_line_in_file(prm, 14, "%f" % tilty, prm)


def runmsa():
    """Run the msa command for the current slcname."""
    cmd = (
        f"cd /d {workingDir} && "
        f"msa -prm prm\\msa_{slcname}.prm -out wav\\{slcname} /ctem"
    )
    output = subprocess.check_output(cmd, shell=True, encoding="utf-8")
    #print(output)
    #subprocess.run(cmd, shell=True, check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)

def sim_function(Tilt, Tilta, Cs, Df, Tk, A1, A1a, A2, A2a, B2, B2a, Sod,
                 virbx, virby, zval, iteration=None):
    """Patch wavimg .prm for one parameter combination and run wavimg."""
    TkV = round(Tk / zval)

    prm = workingDir + "prm\\wavimg_%s.prm" % slcname

    # Slice index → wave file
    replace_single_line_in_file(
        prm, 1, "'wav\\%s_sl%03d.wav'" % (slcname, TkV), prm)

    # Source diameter
    replace_single_line_in_file(prm, 14, "1,%f" % Sod, prm)

    # Vibration
    replace_single_line_in_file(
        prm, 17, "2,%.3f,%.3f,0.0" % (virbx, virby), prm)

    # Aberration block (lines 18–28)
    A1x, A1y = polar_to_cartesian(A1, A1a)
    A2x, A2y = polar_to_cartesian(A2, A2a)
    B2x, B2y = polar_to_cartesian(B2, B2a)
    Cs_scaled = Cs * 1000
    aberr_block = (
        "10\n"
        "0.0 0.0 0.0 0.0\n"
        "1, %0.1f, 0.\n" % Df +
        "2, %0.1f,%0.1f 0.\n" % (A1x, A1y) +
        "3, %0.1f, %0.1f 0.0\n" % (B2x, B2y) +
        "4, %0.1f, %0.1f 0.0\n" % (A2x, A2y) +
        "5, %0.1f, 0.\n" % Cs_scaled +
        "6.0 0.0 0.0 0.0\n"
        "7.0 0.0 0.0 0.0\n"
        "8.0 0.0 0.0 0.0\n"
        "9.0 0.0 0.0 0.0\n"
    )
    replace_lines(prm, 18, 29, aberr_block, prm)

    # Output dat filename
    slcname2 = slcname.split("_")[0]
    Tk1 = Tk * 1000
    dat_subdir = "img\\%s\\dat" % str(iteration) if iteration is not None else "img\\dat"
    os.makedirs(os.path.join(workingDir, dat_subdir), exist_ok=True)
    replace_single_line_in_file(
        prm, 6,
        f'%s\\%s_Tilt_{Tilt}_Tilta_{Tilta}_Cs_{Cs}_Df_{Df}_Tk_{Tk}_A1_{A1}_A1a_{A1a}_A2_{A2}_A2a_{A2a}_B2_{B2}_B2a_{B2a}_Sod_{Sod}_virbx_%.3f_virby_%.3f_map.dat'% (dat_subdir,slcname2,virbx,virby) , prm)

    runwav()


# ── Main sweep ────────────────────────────────────────────────────────────────

def run_sweep(cfg, iteration=None):
    global workingDir, slcname, heightval, widthval

    workingDir = workingDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + os.sep
    slcname    = cfg["slc_name"]
    widthval   = int(cfg["width"])
    heightval  = int(cfg["height"])
    zval       = float(cfg["z_nm"]) / int(cfg["z_slices"])

    Cs_range    = range_from_cfg(cfg["Cs"])
    Df_range    = range_from_cfg(cfg["Df"])
    Tk_range    = range_from_cfg(cfg["Tk"])
    Tilt_range  = range_from_cfg(cfg["Tilt"])
    Tilta_range = range_from_cfg(cfg["Tilta"])
    A1_range    = range_from_cfg(cfg["A1"])
    A1a_range   = range_from_cfg(cfg["A1a"])
    A2_range    = range_from_cfg(cfg["A2"])
    A2a_range   = range_from_cfg(cfg["A2a"])
    B2_range    = range_from_cfg(cfg["B2"])
    B2a_range   = range_from_cfg(cfg["B2a"])
    Sod_range   = range_from_cfg(cfg["Sod"])
    virbx_range = range_from_cfg(cfg["virbx"])
    virby_range = range_from_cfg(cfg["virby"])

    total_count = (
        len(Cs_range) * len(Df_range) * len(Tk_range) * len(Tilt_range) *
        len(Tilta_range) * len(A1_range) * len(A1a_range) * len(A2_range) *
        len(A2a_range) * len(B2_range) * len(B2a_range) * len(Sod_range) *
        len(virbx_range) * len(virby_range)
    )

    print("Cs_range:",    Cs_range)
    print("Df_range:",    Df_range)
    print("Tk_range:",    Tk_range)
    print("Tilt_range:",  Tilt_range)
    print("Tilta_range:", Tilta_range)
    print("A1_range:",    A1_range)
    print("A1a_range:",   A1a_range)
    print("A2_range:",    A2_range)
    print("A2a_range:",   A2a_range)
    print("B2_range:",    B2_range)
    print("B2a_range:",   B2a_range)
    print("Sod_range:",   Sod_range)
    print("virbx_range:", virbx_range)
    print("virby_range:", virby_range)
    print("Total combinations:", total_count)

    pbar = tqdm(total=total_count, desc="Sweep progress")

    for tilt, tilta in itertools.product(Tilt_range, Tilta_range):
        msachange(tilt, tilta)
        runmsa()

        for combo in itertools.product(
            Cs_range, Df_range, Tk_range,
            A1_range, A1a_range, A2_range, A2a_range,
            B2_range, B2a_range, Sod_range,
            virbx_range, virby_range
        ):
            sim_function(tilt, tilta, *combo, zval, iteration=iteration)
            pbar.update(1)

    pbar.close()


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="TEM STO parameter sweep with vibration (no GUI)")
    parser.add_argument("--config", default="config_STO.yaml",
                        help="Path to config file")
    parser.add_argument("--iteration", type=int, default=None,
                        help="Iteration index; output goes to img/<N>/dat/")
    args = parser.parse_args()

    cfg = load_config(args.config)
    run_sweep(cfg, iteration=args.iteration)
