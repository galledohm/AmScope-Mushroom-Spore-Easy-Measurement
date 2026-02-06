# AmScope Mushroom Spore Easy Measurement

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)

Lightweight utility to calculate spore dimension statistics and mycological parameters from CSV measurements.

Features
- Parses CSV rows with a "Length" column like "8.177, 5.515". These measurments are generated at the AMScope software using the "Vertical- Four Points" feature and then exporting the measurements to a CSV file.
- Computes min/max/mean/std for length and width, Q (L/W) statistics, coefficient of variation C, Me (mean of extremes) and Qe.
- Outputs a concise console summary and a detailed analysis log next to the input CSV.

Quick start

1. Install dependencies:
```sh
pip install -r requirements.txt
```

1. Run the script:
```sh
python spore_mean_meas.py samples/Collybia_nuda.csv
```

Files and symbols
- Main script: [spore_mean_meas.py](spore_mean_meas.py) — see functions [`calculate_spore_dimensions`](spore_mean_meas.py) and [`write_log_file`](spore_mean_meas.py).
- Sample data: [samples/Collybia_nuda.csv](samples/Collybia_nuda.csv), [samples/Lepiota_subincarnata.csv](samples/Lepiota_subincarnata.csv)
- Dependencies: [requirements.txt](requirements.txt)
- License: [LICENSE](LICENSE)

Usage details
- Input CSV must contain a header with a column named `Length` where each cell is formatted "height, width" (quotes optional).
- The script writes an analysis log file next to the CSV named `<original>_analysis.log`.

Example output (console)
```
6.11-7.52 (6.53) µm x 4.04-5.19 (4.56) µm; Q=1.43; σ=0.12; C=81.36%; Me=6.32 x 4.62; Qe=1.43
Analysis log saved to: samples/Collybia_nuda_analysis.log
```

Contributing
- Open issues or pull requests for fixes and improvements.
- Keep changes minimal and include tests where appropriate.

Acknowledgements
- Special thanks to the outstanding work of the Asociación Micológica La Senderuela for their contributions to mycology, fieldwork, and community education — their efforts inspired and supported projects like this one.

License
- Released under the MIT License — see [LICENSE](LICENSE).