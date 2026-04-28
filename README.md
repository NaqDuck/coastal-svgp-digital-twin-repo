# Coastal SVGP Digital Twin

This repository contains the runnable code and curated data products for a coastal elevation digital-twin workflow at Bass Drive and Bicentennial Park. The workflow combines multi-epoch NOAA LiDAR-derived elevation products with sequential RTK-GNSS surveys, then trains and updates a streaming Sparse Variational Gaussian Process (SVGP) model for point-level validation, prediction surfaces, uncertainty diagnostics, and forecast-staleness summaries.

The repository is intentionally curated for reproducibility. Large raw NOAA GeoTIFF and ZIP downloads are not included. Instead, the extracted per-survey NOAA point CSVs, RTK survey files, metadata, notebooks, model checkpoints, and result figures are included.

## Repository Layout

```text
Codes/
  toclip.ipynb                         # Optional NOAA raster clipping workflow
  NOAA to CSV.ipynb                    # Optional raster-to-point extraction workflow
  Rw5 file CONVERTER.ipynb             # Converts raw .rw5 survey files to CSV
  Streaming SVGP Shared.ipynb          # Main SVGP training, validation, update workflow

Datasets/
  Extracted/                           # Per-survey NOAA point CSVs
  Metadata/                            # NOAA XML metadata files
  Sunday Data/
    Original survey files/             # Raw RTK .rw5 files
    Bass/                              # Converted Bass RTK CSVs
    BicantP/                           # Converted Bicentennial RTK CSVs

Models/
  BASS 3/                              # Bass model checkpoints, figures, summaries
  BICENTP 2/                           # Bicentennial model checkpoints, figures, summaries

scripts/
  build_noaa_combined.py               # Rebuilds generated combined NOAA CSVs
```

## Setup

Create a Python environment and install the project dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

The SVGP notebook uses TensorFlow and GPflow. On Apple Silicon or managed university machines, TensorFlow installation may require environment-specific setup.

## Rebuild Generated NOAA Inputs

The main SVGP notebook expects a combined NOAA CSV for each beach:

```text
Datasets/Extracted/Bass CSV/NOAA_all_surveys_combined.csv
Datasets/Extracted/Bicent CSV/NOAA_all_surveys_combined.csv
```

Those two generated files are larger than GitHub's normal file-size limit, so they are not stored in this repository. Rebuild them from the included per-survey point CSVs:

```bash
python scripts/build_noaa_combined.py --beach all
```

## Run Order

For the main reproducible path from included data products:

1. Rebuild the combined NOAA CSVs:

   ```bash
   python scripts/build_noaa_combined.py --beach all
   ```

2. Open `Codes/Streaming SVGP Shared.ipynb`.

3. Set `BEACH = "bass"` or `BEACH = "bicentennial"` in the configuration cell.

4. Run the notebook from top to bottom. Outputs are written to:

   ```text
   Models/BASS 3/
   Models/BICENTP 2/
   ```

Optional preprocessing paths:

- Use `Codes/Rw5 file CONVERTER.ipynb` to regenerate converted RTK CSVs from the raw `.rw5` files.
- Use `Codes/toclip.ipynb` and `Codes/NOAA to CSV.ipynb` only if the original NOAA GeoTIFF products are available locally.

## Outputs Included

The model output folders include:

- held-out RTK validation summaries
- streaming update impact summaries
- forecast-staleness summaries
- calibration diagnostics
- final prediction surfaces
- model checkpoints and run metadata

These outputs can be used to verify the numerical results reported in the manuscript.

## Data Notes

NOAA source products originate from NOAA Digital Coast. Large raw NOAA ZIP and GeoTIFF files are omitted from this repository to keep it usable on GitHub. The included metadata XML files and per-survey extracted point CSVs preserve the survey provenance needed by the runnable SVGP workflow.

