# -*- coding: utf-8 -*-
"""
Step 3. SSIM-based image comparison against TEM simulation data (no GUI)

Each simulated image is individually aligned to the experimental reference
via phase correlation before SSIM is computed.  Both images are cropped to
the valid overlap region, guaranteeing identical sizes.

Usage:
    python imagecompare_ssim_value4.0_128x128.py [--iteration N]

When --iteration N is given, DATA_FOLDER is redirected to img/<N>/dat/ .

Edit the parameters in the "Parameters" section below before running.
"""
# ═══════════════════════════════════════════════════════════════════════════════

from skimage.metrics import structural_similarity as ssim
from skimage import io
import cv2
import os
import re
import numpy as np
# ═══════════════════════════════════════════════════════════════════════════════
# Parameters — edit these before running
# ═══════════════════════════════════════════════════════════════════════════════

# Path to the experimental reference image (.jpg or other grayscale image)
REFERENCE_IMAGE = r"C:\Users\chen\githubclone\clonefolder\TEMsimulationUI\Workpath\example\exp_data\sum_59x59.jpg"

# Folder containing simulated .dat files to compare against
DATA_FOLDER = r"C:\Users\chen\githubclone\clonefolder\TEMsimulationUI\Workpath\img\dat"

# Full pixel dimensions of each simulated .dat image (width x height)
IMAGE_WIDTH  = 89
IMAGE_HEIGHT = 90

# Crop size for the initial comparison region, applied before alignment
# (centered crop of the simulated image; width x height)
COMPARE_WIDTH  = 59
COMPARE_HEIGHT = 59

# Set False to skip phase-correlation alignment (useful for debugging)
ENABLE_ALIGNMENT = True

# Minimum valid overlap size in pixels after alignment.
# If the computed shift leaves fewer pixels than this in either dimension,
# the alignment result is discarded and a plain center-crop is used instead.
MIN_OVERLAP = 1600




# ── Parameter name list (must match order encoded in filenames) ───────────────
PARAMETER_NAMES = [
    "Tilt", "Tilta", "Cs", "Df", "Tk",
    "A1", "A1a", "A2", "A2a", "B2", "B2a",
    "Sod", "virbx", "virby",
]


# ── Filename parsing ──────────────────────────────────────────────────────────

def extract_parameters(filename):
    """Parse parameter names and values from a simulation filename."""
    filename = filename.split("_", 1)[-1]
    pattern = r"([^_]+)_([^_]+)"
    matches = re.findall(pattern, filename)
    parameters = []
    parameter_values = []
    for match in matches:
        parameters.append([match[0], match[1]])
        parameter_values.append(float(match[1]))
    return parameters, parameter_values


# ── Image loading ─────────────────────────────────────────────────────────────

def read_binary_file(file_path, height, width, centerx, centery):
    """Read a float32 binary .dat file, crop to center, and normalise to uint8."""
    image_data = np.fromfile(file_path, dtype=np.float32).reshape((height, width))

    if height > centery:
        sr = (height - centery) // 2
        image_data = image_data[sr : sr + centery, :]
    if width > centerx:
        sc = (width - centerx) // 2
        image_data = image_data[:, sc : sc + centerx]

    image_data = (image_data - image_data.min()) / (image_data.max() - image_data.min()) * 255
    return image_data.astype(np.uint8)


# ── Alignment ─────────────────────────────────────────────────────────────────

def compute_shift(ref_img, sim_img):
    """
    Compute the integer translation (dx, dy) that maps sim onto ref using
    phase correlation.  ref_img and sim_img must be uint8 and the same size.
    Returns (dx, dy) in (column, row) convention.
    """
    ref_f = ref_img.astype(np.float32)
    sim_f = sim_img.astype(np.float32)
    shift, _ = cv2.phaseCorrelate(ref_f, sim_f)
    return int(round(shift[0])), int(round(shift[1]))


def apply_shift_and_crop(ref_img, sim_img, dx, dy):
    """
    Given a pre-computed shift (dx, dy) — where sim is displaced by (dx, dy)
    relative to ref — crop both images to the valid overlap region so that the
    returned pair is pixel-aligned and has identical dimensions.

    Falls back to a plain center crop of min-size if the shift is degenerate.
    """
    h, w = ref_img.shape[:2]

    # Overlap window in ref and sim coordinate spaces
    x0_r, x1_r = max(0,  dx), min(w, w + dx)
    y0_r, y1_r = max(0,  dy), min(h, h + dy)
    x0_s, x1_s = max(0, -dx), min(w, w - dx)
    y0_s, y1_s = max(0, -dy), min(h, h - dy)

    ref_crop = ref_img[y0_r:y1_r, x0_r:x1_r]
    sim_crop = sim_img[y0_s:y1_s, x0_s:x1_s]

    # Guarantee identical size (floating-point rounding safety)
    mh = min(ref_crop.shape[0], sim_crop.shape[0])
    mw = min(ref_crop.shape[1], sim_crop.shape[1])

    if mh < MIN_OVERLAP or mw < MIN_OVERLAP:
        # Shift too large — fall back to plain center crop
        mh = min(ref_img.shape[0], sim_img.shape[0])
        mw = min(ref_img.shape[1], sim_img.shape[1])
        cy_r, cx_r = ref_img.shape[0] // 2, ref_img.shape[1] // 2
        cy_s, cx_s = sim_img.shape[0] // 2, sim_img.shape[1] // 2
        ref_crop = ref_img[cy_r - mh//2 : cy_r + mh//2, cx_r - mw//2 : cx_r + mw//2]
        sim_crop = sim_img[cy_s - mh//2 : cy_s + mh//2, cx_s - mw//2 : cx_s + mw//2]
        # Re-clip to equal size
        mh = min(ref_crop.shape[0], sim_crop.shape[0])
        mw = min(ref_crop.shape[1], sim_crop.shape[1])

    return ref_crop[:mh, :mw], sim_crop[:mh, :mw]


# ── Main comparison ───────────────────────────────────────────────────────────

def run_comparison():
    w, h    = IMAGE_WIDTH, IMAGE_HEIGHT
    centerx = COMPARE_WIDTH
    centery = COMPARE_HEIGHT

    # Load reference and resize to the comparison crop size so that
    # phase correlation and SSIM operate in the same pixel space.
    image1_raw = cv2.imread(REFERENCE_IMAGE, cv2.IMREAD_GRAYSCALE)
    if image1_raw is None:
        raise FileNotFoundError(f"Reference image not found: {REFERENCE_IMAGE}")
    if image1_raw.shape != (centery, centerx):
        image1 = cv2.resize(image1_raw, (centerx, centery),
                            interpolation=cv2.INTER_AREA)
    else:
        image1 = image1_raw

    all_parameter_values = []
    top_10_ssim_values   = []
    best_ssim            = -1
    best_name            = None
    best_matching_image  = None

    ssim_log_path = os.path.join(DATA_FOLDER, "ssim_values.txt")
    with open(ssim_log_path, "a") as log:
        for filename in os.listdir(DATA_FOLDER):
            if not filename.endswith(".dat"):
                continue

            simulated_image = read_binary_file(
                os.path.join(DATA_FOLDER, filename), h, w, centerx, centery)

            if ENABLE_ALIGNMENT:
                dx, dy = compute_shift(image1, simulated_image)
                ref_crop, sim_crop = apply_shift_and_crop(
                    image1, simulated_image, dx, dy)
            else:
                ref_crop, sim_crop = image1, simulated_image

            ssim_value = ssim(ref_crop, sim_crop)
            _, parameter_values = extract_parameters(filename)
            parameter_values.append(ssim_value)
            all_parameter_values.append(parameter_values)
            log.write(f"{parameter_values}\n")

            # Track top 10
            if len(top_10_ssim_values) < 10:
                top_10_ssim_values.append((ssim_value, parameter_values))
            else:
                min_ssim, _ = min(top_10_ssim_values, key=lambda x: x[0])
                if ssim_value > min_ssim:
                    top_10_ssim_values = [
                        (s, p) if s != min_ssim else (ssim_value, parameter_values)
                        for s, p in top_10_ssim_values
                    ]

            if ssim_value > best_ssim:
                best_ssim           = ssim_value
                best_matching_image = sim_crop
                best_name           = filename

    # Summary statistics over top 10
    if top_10_ssim_values:
        parameter_arrays = [params[:-1] for _, params in top_10_ssim_values]
        avg = np.mean(parameter_arrays, axis=0)
        std = np.std(parameter_arrays, axis=0)

        avg_str = "_".join(f"{n}_{v:.2e}" for n, v in zip(PARAMETER_NAMES, avg))
        std_str = "_".join(f"{n}_{v:.2e}" for n, v in zip(PARAMETER_NAMES, std))
        print("Top-10 SSIM average parameters:\n", avg_str)
        print("Top-10 SSIM std deviation:\n", std_str)

    print(f"\nBest match: {best_name}")
    print(f"Best SSIM:  {best_ssim:.6f}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--iteration", type=int, default=None,
                        help="Iteration index; reads from img/<N>/dat/")
    args = parser.parse_args()

    if args.iteration is not None:
        # Redirect DATA_FOLDER: .../img/dat → .../img/<N>/dat
        _parent = os.path.dirname(DATA_FOLDER.rstrip("/\\"))
        DATA_FOLDER = os.path.join(_parent, str(args.iteration), "dat")

    run_comparison()
