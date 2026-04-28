# Data Availability

This repository includes the runnable notebooks, converted RTK survey products, raw `.rw5` field survey files, NOAA metadata XML files, extracted per-survey NOAA point CSVs, model checkpoints, and model-output figures/tables used to verify the reported results.

Large raw NOAA ZIP and GeoTIFF files are not included because they are public source products and are too large for a practical GitHub repository. They can be retrieved from NOAA Digital Coast using the beach-specific study areas and source identifiers recorded in the metadata and extracted CSV filenames.

The generated combined NOAA CSV files are also not tracked because each exceeds GitHub's normal single-file size limit. They can be regenerated from the tracked per-survey CSV files with:

```bash
python scripts/build_noaa_combined.py --beach all
```

