# -*- coding: utf-8 -*-
"""
Step 1. TEM Simulation — Dr.Probe script (no GUI)
Version history: v1(2023-12), v2(2024-01), v3(2026-01), v5(config-driven)

Usage:
    python TEMsimulation5.py [--config config.yaml]

All parameters are read from config.yaml; no manual input required.
Run once as an initial setup test before the iterative sweep pipeline.
"""

import os
import sys
import math
import argparse
import numpy as np
import tifffile as tiff
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

try:
    import yaml
except ImportError:
    sys.exit("Please install pyyaml first: pip install pyyaml")


# ── Config loading ───────────────────────────────────────────────────────────

def load_config(config_path="config.yaml"):
    if not os.path.isabs(config_path):
        config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), config_path)
    if not os.path.exists(config_path):
        sys.exit(f"Config file not found: {config_path}")
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


# ── Image I/O and display ─────────────────────────────────────────────────────

def read_binary_file(file_path, height, width):
    """Read float32 image data from a binary .dat file."""
    image_data = np.fromfile(file_path, dtype=np.float32)
    return image_data.reshape((height, width))


def create_custom_cmap(color_type):
    if color_type == 1:
        colors = [(0, 0, 0), (0, 0, 1), (0, 1, 0), (1, 0, 0), (1, 1, 0), (1, 1, 1)]
        return LinearSegmentedColormap.from_list("custom_gradient", colors)
    else:
        return LinearSegmentedColormap.from_list("custom_graymap", [(0, 0, 0), (1, 1, 1)])


def show_image(image_data, color_type=1, title="TEM Simulation Result"):
    """Display the simulated image using matplotlib."""
    fig, ax = plt.subplots(figsize=(8, 8))
    cax = ax.matshow(image_data, cmap=create_custom_cmap(color_type))
    fig.colorbar(cax)
    ax.set_title(title)
    plt.tight_layout()
    plt.show()


def export_to_tiff(file_path, height, width, output_folder):
    """Export a binary .dat file to .tif."""
    image_data = read_binary_file(file_path, height, width)
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    output_path = os.path.join(output_folder, f"{file_name}.tif")
    tiff.imsave(output_path, image_data)
    print(f"Export successful: {output_path}")
    return image_data


def batch_export_to_tiff(input_folder, output_folder, height, width):
    """Batch-export all .dat files in input_folder to .tif."""
    import glob
    dat_files = glob.glob(os.path.join(input_folder, "*.dat"))
    if not dat_files:
        print(f"No .dat files found in: {input_folder}")
        return
    for file_path in dat_files:
        export_to_tiff(file_path, height, width, output_folder)


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


# ── Batch file execution ─────────────────────────────────────────────────────

def runbatfile(batch_file_path):
    import subprocess
    try:
        result = subprocess.run(
            batch_file_path, shell=True, check=True,
            stdout=subprocess.PIPE, text=True
        )
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error running batch file: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


# ── Folder management ────────────────────────────────────────────────────────

def check_and_create_folder(folder_path):
    import shutil
    if os.path.exists(folder_path):
        try:
            shutil.rmtree(folder_path)
            os.makedirs(folder_path)
            print(f"Folder '{folder_path}' cleared and recreated.")
        except Exception as e:
            print(f"Error clearing folder: {e}")
    else:
        try:
            os.makedirs(folder_path)
            print(f"Folder '{folder_path}' created.")
        except Exception as e:
            print(f"Error creating folder: {e}")


# ── Aberration scan utilities ─────────────────────────────────────────────────

def aberration_scan_angle(length, angle_begin, angle_step, angle_end):
    """Scan aberration by angle. Returns [[length, abberX, abberY, angle], ...]."""
    num = int((angle_end - angle_begin) / angle_step)
    result = []
    for i in range(num):
        angle = angle_step * i + angle_begin
        abberX = round(math.cos(angle / 180 * math.pi) * length, 4)
        abberY = round(math.sin(angle / 180 * math.pi) * length, 4)
        result.append([length, abberX, abberY, angle])
    return result


def aberration_scan_length(length_begin, length_step, length_end, angle):
    """Scan aberration by magnitude. Returns [[length, abberX, abberY, angle], ...]."""
    num = int((length_end - length_begin) / length_step)
    result = []
    for i in range(num):
        length = length_begin + i * length_step
        abberX = round(math.cos(angle / 180 * math.pi) * length, 4)
        abberY = round(math.sin(angle / 180 * math.pi) * length, 4)
        result.append([length, abberX, abberY, angle])
    return result


# ── Main simulation function ──────────────────────────────────────────────────

def run_simulation(cfg):
    """Read all parameters from cfg dict and execute the TEM simulation."""

    # ── Paths and basic parameters ────────────────────
    workingDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + os.sep
    docname    = cfg["sub_folder"]
    cifname    = cfg["cif_name"]
    celname    = cfg["cel_name"]
    celname2   = celname + "1"
    typef      = int(cfg["work_type"])
    color_type = int(cfg.get("color_type", 1))

    # ── Crystal structure ─────────────────────────────
    a = float(cfg["cell_a"]) * 0.1   # Å → nm
    b = float(cfg["cell_b"]) * 0.1
    c = float(cfg["cell_c"]) * 0.1
    rpx    = int(cfg["repeat_x"])
    rpy    = int(cfg["repeat_y"])
    slice1 = int(cfg["slice_number"])
    a = a * rpx
    b = b * rpy

    # ── Sampling and image dimensions ─────────────────
    sample_rate = float(cfg["sample_rate"])
    xa = round(a / sample_rate, 0) * 2
    yb = round(b / sample_rate, 0) * 2
    zc = slice1
    na = a / xa
    nb = b / yb

    # ── Defocus range ─────────────────────────────────
    dfmin  = float(cfg["defocus_min"])
    dfmax  = float(cfg["defocus_max"])
    dfstep = float(cfg["defocus_step"])
    dfcont = round((dfmax - dfmin) / dfstep + 1, 0)
    defocus = dfmin

    # ── Thickness range ───────────────────────────────
    tkmin_nm  = float(cfg["thickness_min"])
    tkmax_nm  = float(cfg["thickness_max"])
    tkstep_nm = float(cfg["thickness_step"])
    tkcont    = round((tkmax_nm - tkmin_nm) / tkstep_nm + 1, 0)
    tkmin     = round(tkmin_nm / (c / slice1), 0)
    tkmax     = round(tkmax_nm / (c / slice1), 0)
    tkminnm   = tkmin * (c / slice1)

    # ── Output image size ─────────────────────────────
    if typef == 1:
        xp = round(xa * 0.5, 0)
        yp = round(yb * 0.5, 0)
    else:
        xp = round(xa * 0.5 * dfcont, 0)
        yp = round(yb * 0.5 * tkcont, 0)

    # ── Aberration parameters ─────────────────────────
    A1_str   = str(cfg["A1"])
    coma_str = str(cfg["coma"])
    A2_str   = str(cfg["A2"])
    A1x  = float(A1_str.split(",")[0])   * math.cos(float(A1_str.split(",")[1])   / 180 * math.pi)
    A1y  = float(A1_str.split(",")[0])   * math.sin(float(A1_str.split(",")[1])   / 180 * math.pi)
    comax = float(coma_str.split(",")[0]) * math.cos(float(coma_str.split(",")[1]) / 180 * math.pi)
    comay = float(coma_str.split(",")[0]) * math.sin(float(coma_str.split(",")[1]) / 180 * math.pi)
    A2x  = float(A2_str.split(",")[0])   * math.cos(float(A2_str.split(",")[1])   / 180 * math.pi)
    A2y  = float(A2_str.split(",")[0])   * math.sin(float(A2_str.split(",")[1])   / 180 * math.pi)
    CS   = float(cfg["Cs"])
    Oapx = float(cfg["Oapx"])
    vibx = float(cfg["vibration_x"])
    viby = float(cfg["vibration_y"])

    # ── Other optical parameters ──────────────────────
    fs      = float(cfg["focus_spread"])
    sc      = float(cfg["semi_convergence"])
    fr      = float(cfg["frame_rotation"])
    Voltage = float(cfg["voltage"])
    use_mtf = int(cfg["use_mtf"])

    # ── Tilt parameters ───────────────────────────────
    tilt_len = float(cfg["tilt_angle"]) * 0.18 / math.pi
    tiltx    = tilt_len * math.cos(float(cfg["rotation_angle"]) / 180 * math.pi)
    tilty    = tilt_len * math.sin(float(cfg["rotation_angle"]) / 180 * math.pi)

    # ── Atoms and Debye-Waller factors ────────────────
    Atom_string = str(cfg["atoms"])
    Dw_string   = str(cfg["debye_waller"])
    atoms_list  = Atom_string.split(",")
    DW          = [round(float(x) * 0.01, 8) for x in Dw_string.split(",")]
    result_string = ""
    for i, atom in enumerate(atoms_list):
        result_string += " -B %2s," % atom + str(DW[i])

    # ── Work type special handling ────────────────────
    slcname = celname
    if typef == 3:
        defocus = 0.0

    # ── Patch msa_strd.prm → msa_<slcname>.prm ───────
    file_path = workingDir + "prm\\msa_strd.prm"
    newpath   = workingDir + "prm\\msa_%s.prm" % slcname
    replace_single_line_in_file(file_path, 27, "'slc\\%s'" % slcname, newpath)

    file_path = workingDir + "prm\\msa_%s.prm" % slcname
    replace_single_line_in_file(file_path, 6, "%d" % Voltage, file_path)

    # ── Patch wavimg prm ──────────────────────────────
    if typef == 1:
        src_wavimg = workingDir + "prm\\wavimg_1.prm"
        replace_single_line_in_file(
            src_wavimg, 1,
            "'wav\\%s_sl%03d.wav'" % (slcname, tkmin),
            workingDir + "prm\\wavimg_%s.prm" % slcname
        )
        xp = round(xa * 0.5, 0)
        yp = round(yb * 0.5, 0)
    else:
        src_wavimg = workingDir + "prm\\wavimg_%d.prm" % typef
        replace_single_line_in_file(
            src_wavimg, 1,
            "'wav\\%s_sl.wav'" % slcname,
            workingDir + "prm\\wavimg_%s.prm" % slcname
        )

    wav_prm = workingDir + "prm\\wavimg_%s.prm" % slcname
    replace_single_line_in_file(wav_prm, 2, "%d,%d" % (xa, yb), wav_prm)
    replace_single_line_in_file(wav_prm, 3, "%0.9f,%0.9f" % (na, nb), wav_prm)
    replace_single_line_in_file(wav_prm, 4, "%d." % Voltage, wav_prm)

    replace_single_line_in_file(wav_prm, 6,
        "'img\\%s\\%s_map.dat'" % (docname, slcname), wav_prm)
    replace_single_line_in_file(wav_prm, 7, "%d,%d" % (xp, yp), wav_prm)
    replace_single_line_in_file(wav_prm, 10, "%.6f" % sample_rate, wav_prm)
    replace_single_line_in_file(wav_prm, 12, "%0.1f" % fr, wav_prm)
    replace_single_line_in_file(wav_prm, 14, "1, %0.1f" % fs, wav_prm)
    replace_single_line_in_file(wav_prm, 15, "1, %0.1f" % sc, wav_prm)
    replace_single_line_in_file(wav_prm, 16,
        "%d, 1., 'prm\\MTF-US2k-300.mtf'" % use_mtf, wav_prm)
    replace_single_line_in_file(wav_prm, 17, "2,%.3f,%.3f,0.0" % (vibx, viby), wav_prm)

    aberr_block = (
        "10\n"
        "0.0 0.0 0.0 0.0\n"
        "1, %0.1f, 0.\n" % defocus +
        "2, %0.1f,%0.1f 0.\n" % (A1x, A1y) +
        "3, %0.1f, %0.1f 0.0\n" % (comax, comay) +
        "4, %0.1f, %0.1f 0.0\n" % (A2x, A2y) +
        "5, %0.1f, 0.\n" % CS +
        "6.0 0.0 0.0 0.0\n"
        "7.0 0.0 0.0 0.0\n"
        "8.0 0.0 0.0 0.0\n"
        "9.0 0.0 0.0 0.0\n"
        "%0.1f ,0.03 \n" % Oapx
    )
    replace_lines(wav_prm, 18, 30, aberr_block, wav_prm)

    # ── Loop parameters (typef == 2 / 3) ─────────────
    if typef == 3:
        replace_single_line_in_file(
            wav_prm, 35,
            "%0.1f,%0.1f,%d" % (dfmin, dfmax, dfcont), wav_prm)
        replace_single_line_in_file(
            wav_prm, 40,
            "%d,%d,%d" % (tkmin, tkmax, tkcont), wav_prm)
    elif typef == 2:
        replace_single_line_in_file(
            wav_prm, 35,
            "%d,%d,%d" % (tkmin, tkmax, tkcont), wav_prm)
        xp = round(xa * 0.5, 0)
        replace_single_line_in_file(wav_prm, 7, "%d,%d" % (xp, yp), wav_prm)
    else:  # typef == 1
        replace_single_line_in_file(
            wav_prm, 6,
            "'img\\%s\\%s_TK_%s.dat'" % (docname, slcname, tkminnm), wav_prm)

    # ── Patch msa prm: slice sequence ────────────────
    think = tkmax
    repeat = "".join("%d\n" % i for i in range(slice1))
    num_rows = int(think / slice1) + 1
    repeated_text = (
        "%d\n1\n1\n1\n%d\n" % (slice1, think)
        + repeat * num_rows
    )
    msa_prm = workingDir + "prm\\msa_%s.prm" % slcname
    replace_lines(msa_prm, 28, 150, repeated_text, msa_prm)

    # ── Patch msa prm: tilt angles ───────────────────
    replace_single_line_in_file(msa_prm, 13, "%f" % tiltx, msa_prm)
    replace_single_line_in_file(msa_prm, 14, "%f" % tilty, msa_prm)

    # ── Generate runPrm.bat ───────────────────────────
    check_and_create_folder(workingDir + "cel")
    bat_path = workingDir + "img\\runPrm.bat"
    drive = workingDir[:2]
    tz = 1.0 / (slice1 * 2)

    with open(bat_path, "w") as bat:
        bat.write("cd %s" % workingDir[:-1])
        bat.write("\n%s" % drive)
        bat.write("\nBuildcell --cif=cif\\%s.cif --output=cel\\%s.cel" % (cifname, celname))
        bat.write("\ncellmuncher -f cel\\%s.cel -o cel\\%s.cel %s  --cif --override"
                  % (celname, celname2, result_string))
        bat.write("\nCellMuncher -f cel\\%s.cel -o cel\\%s5.cel --repeat=x,%d --repeat=y,%d --cif"
                  % (celname2, celname2, rpx, rpy))
        bat.write("\ncelslc -cel cel\\%s5.cel -slc slc\\%s -nx %d -ny %d -nz %d -ht %d. -abs -dwf"
                  % (celname2, slcname, xa, yb, zc, Voltage))
        bat.write("\nmd img\\%s" % docname)
        bat.write("\nmsa -prm prm\\msa_%s.prm -out wav\\%s /ctem" % (slcname, slcname))
        bat.write("\nwavimg -prm prm\\wavimg_%s.prm /nli" % slcname)

    print("Output image size: %dx%d pixels" % (xp, yp))
    print("runPrm.bat saved to: %simg" % workingDir)

    # ── Run simulation ────────────────────────────────
    runbatfile(bat_path)

    # ── Export result image ───────────────────────────
    out_folder = workingDir + "img\\%s" % docname
    if typef == 1:
        dat_file = workingDir + "img\\%s\\%s_TK_%s.dat" % (docname, slcname, tkminnm)
    else:
        dat_file = workingDir + "img\\%s\\%s_map.dat" % (docname, slcname)

    image_data = export_to_tiff(dat_file, int(yp), int(xp), out_folder)

    if cfg.get("show_image", True):
        show_image(image_data, color_type=color_type)

    # ── Tilt loop (optional) ──────────────────────────
    tl = cfg.get("tilt_loop", {})
    if tl.get("run", False):
        run_tilt_loop(cfg, workingDir, slcname, typef, tkmin, xp, yp, xa, yb, tilt_len)

    # ── Aberration loop (optional) ────────────────────
    al = cfg.get("aberration_loop", {})
    if al.get("run", False):
        run_aberration_loop(cfg, workingDir, slcname, xp, yp)


# ── Tilt Loop ────────────────────────────────────────────────────────────────

def run_tilt_loop(cfg, workingDir, slcname, typef, tkmin, xp, yp, xa, yb, tilt_len):
    tl       = cfg["tilt_loop"]
    tilt_bg  = float(tl["begin"])
    tilt_ic  = float(tl["increment"])
    tilt_ed  = float(tl["end"])

    abber_list = aberration_scan_angle(tilt_len, tilt_bg, tilt_ic, tilt_ed)
    numl = len(abber_list)

    folder = os.path.join(workingDir + "img", "tiltloop")
    os.makedirs(folder, exist_ok=True)

    with open(os.path.join(folder, "recordingtxt.txt"), "w") as f:
        f.write("length abberX abberY angle\n")
        for item in abber_list:
            f.write(f"{item}\n")

    for i in range(numl):
        msa_src = workingDir + "prm\\msa_%s.prm" % slcname
        msa_dst = workingDir + "prm\\msa_%s_tilt_%s.prm" % (slcname, i)
        replace_single_line_in_file(msa_src, 13, "%f" % abber_list[i][1], msa_dst)
        replace_single_line_in_file(msa_dst, 14, "%f" % abber_list[i][2], msa_dst)
        print("tilt: %f, %f" % (abber_list[i][1], abber_list[i][2]))

        wav_src = workingDir + "prm\\wavimg_%s.prm" % slcname
        wav_dst = workingDir + "prm\\wavimg_%s_tilt_%s.prm" % (slcname, i)
        if typef == 1:
            new_wav_line = "'wav\\%s_tilt_%s_sl%03d.wav'" % (slcname, i, tkmin)
        else:
            new_wav_line = "'wav\\%s_tilt_%s_sl.wav'" % (slcname, i)
        replace_single_line_in_file(wav_src, 1, new_wav_line, wav_dst)
        replace_single_line_in_file(
            wav_dst, 6,
            "'img\\tiltloop\\mapping_%s_tilt_%s.dat'" % (slcname, i), wav_dst)

    bat_path = os.path.join(folder, "TiltrunPrm.bat")
    drive = workingDir[:2]
    with open(bat_path, "w") as bat:
        bat.write("cd %s" % workingDir[:-1])
        bat.write("\n%s" % drive)
        for j in range(numl):
            bat.write("\nmsa -prm prm\\msa_%s_tilt_%s.prm -out wav\\%s_tilt_%s /ctem"
                      % (slcname, j, slcname, j))
            bat.write("\nwavimg -prm prm\\wavimg_%s_tilt_%s.prm /nli" % (slcname, j))

    runbatfile(bat_path)
    batch_export_to_tiff(folder, folder, int(yp), int(xp))


# ── Aberration Loop ───────────────────────────────────────────────────────────

def run_aberration_loop(cfg, workingDir, slcname, xp, yp):
    al = cfg["aberration_loop"]
    ab_type = int(al.get("type", 1))
    type_map  = {1: ("A1", 21), 2: ("A2", 23), 3: ("B2", 22), 4: ("def", 20)}
    if ab_type not in type_map:
        print("Invalid aberration_loop.type; must be 1/2/3/4")
        return
    selected_options, selected_line = type_map[ab_type]

    scan_mode = al.get("scan_mode", "length")
    if scan_mode == "length":
        abber_list = aberration_scan_length(
            float(al["length_begin"]), float(al["length_step"]),
            float(al["length_end"]),  float(al["angle_fixed"]))
    else:
        abber_list = aberration_scan_angle(
            float(al["length_fixed"]),
            float(al["angle_begin"]), float(al["angle_step"]),
            float(al["angle_end"]))

    numl = len(abber_list)
    folder = os.path.join(workingDir + "img", "%sloop" % selected_options)
    os.makedirs(folder, exist_ok=True)

    with open(os.path.join(folder, "recordingtxt.txt"), "w") as f:
        f.write("length abberX abberY angle\n")
        for item in abber_list:
            f.write(f"{item}\n")

    wav_src = workingDir + "prm\\wavimg_%s.prm" % slcname
    for i in range(numl):
        wav_dst = workingDir + "prm\\wavimg_%s_%s_No_%s.prm" % (slcname, selected_options, i)
        new_line = "%d," % (selected_line - 19) + str(abber_list[i][1]) + ", " + str(abber_list[i][2])
        replace_single_line_in_file(wav_src, selected_line, new_line, wav_dst)
        replace_single_line_in_file(
            wav_dst, 6,
            "'img\\%sloop\\%s_%s_No_%s.dat'" % (selected_options, slcname, selected_options, i),
            wav_dst)

    bat_path = os.path.join(folder, "%srunLoop.bat" % selected_options)
    drive = workingDir[:2]
    with open(bat_path, "w") as bat:
        bat.write("cd %s" % workingDir[:-1])
        bat.write("\n%s" % drive)
        for i in range(numl):
            bat.write("\nwavimg -prm prm\\wavimg_%s_%s_No_%s.prm /nli"
                      % (slcname, selected_options, i))

    runbatfile(bat_path)
    batch_export_to_tiff(folder, folder, int(yp), int(xp))


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TEM Simulation (Dr.Probe, no GUI)")
    parser.add_argument("--config", default="config.yaml", help="Path to config file")
    args = parser.parse_args()

    cfg = load_config(args.config)
    run_simulation(cfg)
