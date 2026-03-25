# AI-Assisted NCS-TEM Iterative Refinement Method

A computer-aided negative-Cs (NCS) TEM simulation and parameter optimisation pipeline interfaces with [Dr.Probe](https://er-c.org/barthel/drprobe/).
The system automates the traditionally manual process of matching simulated images to experimental NCS-TEM data by combining exhaustive grid optimisation with iterative range narrowing, progressively converging all 14 microscope and sample parameters towards the experimental optimum.

---

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Configuration](#configuration)
- [Output Files](#output-files)
- [Key Parameters](#key-parameters)
- [Demo](#demo)
- [H-Atom Position Refinement](#H-Atom-Position-Refinement)
- [Users Without a Coding Background](#users-without-a-coding-background)
- [Acknowledgements](#acknowledgements)
- [Authors](#authors)


---

## Overview

Accurate interpretation of NCS-TEM images requires precise knowledge of numerous interdependent microscope and specimen parameters. Manual trial-and-error adjustment of these parameters is time-consuming and prone to bias. This pipeline addresses the problem through a fully automated, computer-aided optimisation workflow.

The system extends the Dr.Probe electron-microscopy simulation package with the following capabilities:

1. **Negative-Cs TEM simulation** — instrument parameters are set via `config.yaml`; the Dr.Probe toolchain (`msa` + `wavimg`) generates simulated exit-wave and image output for a given parameter set.

2. **Structured 14-parameter grid optimisation** — rather than performing a single exhaustive search over the full 14-dimensional parameter space (which would require 5¹⁴ ≈ 6 billion simulations), the pipeline uses a **group-rotation grid strategy**: parameters are divided into three physically motivated groups and swept one group at a time. Within each group, a dense grid of candidate values is evaluated, producing a thorough, unbiased sampling of that subspace while keeping computation tractable.

3. **Automated image alignment and SSIM-based scoring** — each simulated image is automatically registered to the experimental reference via phase-correlation alignment before the Structural Similarity Index (SSIM) is computed, removing manual cropping and alignment bias from the comparison.

4. **Iterative range narrowing** — after each group sweep, the pipeline identifies the parameter values that maximise SSIM and automatically halves the search range around that optimum. This coarse-to-fine refinement strategy efficiently concentrates computation in the most promising region of parameter space, converging towards the global optimum over successive iterations without requiring any user intervention.

5. **Convergence visualisation** — SSIM trends across all iterations are plotted automatically, providing a clear record of parameter convergence and a direct visual measure of simulation quality improvement.

---

## Installation

### 1. Download Dr.Probe

Download the Dr.Probe package from the official website:

```
https://er-c.org/barthel/drprobe/
```

Extract the executables (`wavimg.exe`, `msa.exe`, `celslc.exe`, etc.) and place them in:

```
system/win32/
```

Make sure this directory is added to the system `PATH` so the executables can be called directly from the command line.

### 2. Set Up the Working Directory

Copy the `workpath/` folder from this repository to your local machine. It contains the directory structure and `.prm` template files required by Dr.Probe:

```
workpath/
├── prm/            ← Dr.Probe parameter file templates (msa_*.prm, wavimg_*.prm)
├── slc/            ← Output directory for slice files
├── cel/            ← Output directory for unit-cell files
├── wav/            ← Output directory for wave-function files (msa)
├── img/
│   └── 1/
│       └── dat/    ← Simulated image output per iteration (auto-created)
├── cif/
│   └── SrTiO3.cif  ← Atomic structure model corresponding to the experiment
└── example/
    └── ref.jpg     ← Place your experimental reference image here
```

### 3. Install Python Dependencies

```bash
pip install numpy pyyaml scikit-image opencv-python matplotlib seaborn pandas tqdm tifffile
```

Python ≥ 3.8 is required.

---


## Configuration

### `config.yaml` (Step 1 — initial simulation)

Used for a single test simulation to verify that the working directory, slice files, and instrument parameters are correct. Key fields to edit:

| Field | Description |
|-------|-------------|
| `work_path` | Absolute path to the Dr.Probe working directory (Windows path, trailing `\\`) |
| `slc_name` | Crystal slice filename prefix (must match `.prm` file naming) |
| `voltage` | Accelerating voltage (kV) |
| `Cs` | Spherical aberration coefficient (μm; negative for negative-Cs mode) |
| `defocus` | Defocus value (nm) |

### `config_STO.yaml` (Steps 2–5 — grid sweep)

**Parameter ranges are written automatically at startup** — no manual editing required. The following path fields must be filled in manually:

```yaml
work_path:  "H:\\DrProbe\\SrTiO\\"   # Working directory (must match config.yaml)
slc_name:   "SrTiO"                   # Crystal filename prefix
width:   89                            # Simulated image width (pixels)
height:  90                            # Simulated image height (pixels)
z_nm:    0.3885                        # Total unit-cell length along c (nm)
z_slices: 4                            # Number of slices along z
```

### `Step3_imagecompare_ssim_value4.0.py` — top-of-file parameters

Edit before running:

```python
REFERENCE_IMAGE = r"C:\TEM\experiment\ref.jpg"  # Path to experimental reference image
DATA_FOLDER     = r"C:\TEM\img\dat"             # Directory containing simulated .dat files
IMAGE_WIDTH     = 89                             # Simulated image width (must match config_STO)
IMAGE_HEIGHT    = 90                             # Simulated image height
COMPARE_WIDTH   = 59                             # Crop width used for SSIM comparison
COMPARE_HEIGHT  = 59                             # Crop height used for SSIM comparison
```

---

### Group-Rotation Grid Strategy

A naive full grid search over all 14 parameters simultaneously is computationally intractable (5 points × 14 parameters = 5¹⁴ ≈ 6 billion simulations). The pipeline solves this by decomposing the parameter space into three physically motivated groups, sweeping one group per iteration while holding all other parameters fixed at their current best-known values. This preserves the thoroughness of a grid search within each subspace while reducing each iteration to a manageable size.

14 parameters are split into 3 groups:

| Group | Parameters | Typical combinations | Time (@ 10 img/s) |
|-------|-----------|----------------------|-------------------|
| Group 1 | Cs, Df, Tk, Tilt, Tilta | ≈ 5,625 | ~9 min |
| Group 2 | A1, A1a, A2, A2a | ≈ 2,025 | ~3 min |
| Group 3 | B2, B2a, Sod, virbx, virby | ≈ 225 | < 1 min |

Six iterations take approximately **1–2 hours** in total; each group undergoes two rounds of progressive refinement.

---

## Output Files

```
workpath/
└── img/
    ├── 1/dat/
    │   ├── *.dat                  ← All simulated images from iteration 1 (float32 binary)
    │   ├── ssim_values.txt        ← One line per simulation: [param list..., SSIM]
    │   └── facebake_borad/
    │       ├── 1d_Cs.png          ← 1D SSIM-vs-parameter curves
    │       ├── summary_1d_grid.png← Summary grid of all parameters
    │       ├── 2d_Cs_vs_Df.png    ← 2D SSIM heatmaps for parameter pairs
    │       └── best_parameters.txt← Best parameter combination and SSIM for this iteration
    ├── 2/dat/ …
    ├── …
    └── ssim_progression.png       ← Cross-iteration SSIM improvement summary
pipeline_state.json                ← Current best-known values and initial ranges (auto-maintained)
```

### How to Read `ssim_progression.png`

Each panel corresponds to one iteration; the x-axis is the simulation rank sorted by SSIM (ascending):

- **Grey thin line** — all simulations from this iteration
- **Coloured thick line** — only simulations that exceed the previous iteration's best SSIM (the improvement)
- **Red dashed line** — previous iteration's best SSIM (the threshold this iteration must surpass)
- **Dot + annotation** — best SSIM achieved in this iteration

As iterations progress, the coloured line should shift upward, indicating effective parameter convergence.

---

## Key Parameters

All located at the top of `main.py`; changes take effect immediately on the next run:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `MAX_ITERATIONS` | 6 | Total iterations; recommended to be a multiple of 3 |
| `MAX_POINTS_PER_PARAM` | 5 | Max discrete values per active parameter per iteration; controls total combination count |
| `ANGLE_STEP_DEG` | 45 | Step size for angle parameters (°); larger = faster but coarser |
| `PHYSICAL_RANGES` | see below | Physical bounds for each parameter; auto-written to config on startup |

**Default physical ranges:**

| Parameter | Range | Unit |
|-----------|-------|------|
| `Cs` | −15 to −10 | μm |
| `Df` | 0 to 5 | nm |
| `Tk` | 1 to 5 | nm |
| `Tilt` | 0 to 5 | mrad |
| `Tilta` | 0 to 360 | deg |
| `A1` | 0 to 1 | nm |
| `A1a` | 0 to 360 | deg |
| `A2` | 50 to 100 | nm |
| `A2a` | 0 to 360 | deg |
| `B2` | 50 to 100 | nm |
| `B2a` | 0 to 360 | deg |
| `Sod` | 2.5 (fixed) | nm |
| `virbx` | 0 to 0.05 | nm |
| `virby` | 0 to 0.05 | nm |

---

## Demo

The **[example](Workpath/example)** directory contains a ready-to-run demonstration **[main.py](Workpath/example/main.py)**. To keep runtime short and make it easy to verify the setup, the demo uses **reduced parameter ranges and fewer iterations**. It is intended for confirming that the environment is configured correctly and does not represent the full search precision required for real experimental data.
## Repository Structure (Demo)

```
example/
├── main.py                                        ← One-click pipeline entry point
├── Step1_TEMsimulation5.py                        ← Step 1: initial parameter test simulation
├── Step2_setdata3.0with_deadline_vibration.py     ← Step 2: 14-parameter grid simulation
├── Step3_imagecompare_ssim_value4.0.py            ← Step 3: image alignment and SSIM calculation
├── Step4_ssim_dashboard.py                        ← Step 4: SSIM visualisation dashboard
├── config.yaml                                    ← Step 1 instrument parameters
├── config_STO.yaml                                ← Steps 2–5 sweep ranges (auto-written at startup)
├── pipeline_state.json                            ← Auto-generated; stores best-known parameter values
└── ReadMe.md
```

## Running

```bash
cd /.../Workpath/example
python main.py
```

The pipeline executes automatically without any further user input:

```
Step 1  Initial simulation test
        Verifies working directory, .prm files, and instrument parameters
        ↓
INIT    Write physical parameter bounds to config_STO.yaml
        Step sizes are auto-computed; Group 0 parameters are activated
        ↓
Iterations 1–6  (one full group cycle every 3 iterations):
  Step 2  Grid simulation
          Only the active group is swept; the other 10 parameters are fixed
          at their current best-known values
  Step 3  SSIM calculation
          Each simulated image is phase-correlation-aligned to the reference,
          cropped to the same size, then SSIM is computed
  Step 4  Visualisation
          1D SSIM-vs-parameter curves and 2D heatmaps are generated and saved
  Step 5  Range narrowing
          Best-SSIM parameter values are identified; the active group's search
          range is halved and the step size halved for the next iteration
        ↓
FINAL   ssim_progression.png — cross-iteration SSIM improvement summary
```
---
### H-Atom Position Refinement

`example/Hchange/` provides an example of structural refinement focused on H-atom positions. This can be run after the main parameter convergence to further optimise atomic coordinates.

---

## Users Without a Coding Background

For users who prefer not to work with code, a complete GUI-based simulation program is available, packaged as a standalone `.exe` file**[exe](Workpath/exe)**  — no Python installation required. See **[TEMsimulation_SOP.md](Workpath/exe/TEMsimulation_UI.md)** for full instructions.

The super-resolution imaging and in-depth structural refinement presented in the associated publication were performed by group members using this GUI software. Technical details are provided in the Methods section of the paper.

---

## Acknowledgements

We thank **Juri Barthel** for technical support with the Dr.Probe simulation package; **Zhanqi** for suggestions on the initial code design; and **Zhiyao Liang** and **Feng Liu** for user feedback during test runs and debugging.

---

## Authors

**Linyuan Chen**, **Xian-Kui Wei**

---
## Patent Notice

The method implemented in this repository is covered by a patent.

Permission is granted to use this code for academic and research purposes only.

Commercial use requires explicit permission from the author.