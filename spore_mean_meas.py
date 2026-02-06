"""Spore dimension analysis tool for AmScope measurements.

This module processes CSV files exported from AmScope microscopy software
to calculate spore size statistics and mycological parameters including
length, width, Q ratio (L/W), coefficient of variation, and mean extremes.

Functions:
    calculate_spore_dimensions: Compute spore statistics from CSV data.
    write_log_file: Write analysis results to a log file.

Usage:
    python spore_mean_meas.py <csv_file>

The input CSV must contain a 'Length' column with values formatted as
'height, width' (numeric, comma-separated).
"""

import argparse
import os
import sys
from datetime import datetime

import pandas as pd

def calculate_spore_dimensions(csv_file_path):
    """
    Reads a CSV file with 'Length' column formatted as 'height,width' strings
    and returns a dictionary of spore size statistics and mycology parameters.
    """
    data_frame = pd.read_csv(csv_file_path)

    # Split 'Length' into Height and Width
    data_frame[['Height', 'Width']] = (
        data_frame['Length'].str.split(',', expand=True).astype(float)
    )

    # Calculations
    height_min = data_frame['Height'].min()
    height_max = data_frame['Height'].max()
    height_mean = data_frame['Height'].mean()
    height_std = data_frame['Height'].std()

    width_min = data_frame['Width'].min()
    width_max = data_frame['Width'].max()
    width_mean = data_frame['Width'].mean()

    data_frame['Q'] = data_frame['Height'] / data_frame['Width']
    q_mean = data_frame['Q'].mean()
    q_std = data_frame['Q'].std()

    # Mycology parameters
    # C = Coefficient of variation of length
    coeff_var = (
        100 - ((height_std / height_mean) * 100 if height_mean != 0 else 0)
    )
    # Me = Mean of extremes (average of min and max length)
    mean_of_extremes = [
        (height_min + height_max) / 2,
        (width_min + width_max) / 2,
    ]
    # Qe = Q value at extremes (ratio of mean length to mean width)
    q_extremes = height_mean / width_mean if width_mean != 0 else 0

    return {
        'lmin': height_min,
        'lmax': height_max,
        'lmean': height_mean,
        'wmin': width_min,
        'wmax': width_max,
        'wmean': width_mean,
        'q_mean': q_mean,
        'q_std': q_std,
        'c_var': coeff_var,
        'mean_of_extremes': mean_of_extremes,
        'q_e': q_extremes,
        'n_spores': len(data_frame),
    }

def write_log_file(csv_file_path, analysis_results):
    """
    Writes the results to a log file in the same directory as the CSV.
    """
    log_file_path = csv_file_path.replace('.csv', '_analysis.log')

    with open(log_file_path, 'w', encoding='utf-8') as file_obj:
        file_obj.write("=" * 60 + "\n")
        file_obj.write("SPORE DIMENSION ANALYSIS REPORT\n")
        file_obj.write("=" * 60 + "\n\n")
        file_obj.write(
            f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        )
        file_obj.write(f"Input File: {csv_file_path}\n")
        file_obj.write(f"Number of Spores Measured: {analysis_results['n_spores']}\n\n")
        file_obj.write("-" * 60 + "\n")
        file_obj.write("DIMENSION STATISTICS\n")
        file_obj.write("-" * 60 + "\n")
        file_obj.write(
            f"Length (L):  {analysis_results['lmin']:.1f}-"
            f"{analysis_results['lmax']:.1f} µm "
            f"(mean: {analysis_results['lmean']:.1f} µm)\n"
        )
        file_obj.write(
            f"Width (W):   {analysis_results['wmin']:.1f}-"
            f"{analysis_results['wmax']:.1f} µm "
            f"(mean: {analysis_results['wmean']:.1f} µm)\n\n"
        )

        file_obj.write("-" * 60 + "\n")
        file_obj.write("MYCOLOGY PARAMETERS\n")
        file_obj.write("-" * 60 + "\n")
        file_obj.write(
            f"Q (L/W ratio):           {analysis_results['q_mean']:.2f} "
            f"(σ = {analysis_results['q_std']:.2f})\n"
        )
        file_obj.write(
            f"C (Coefficient of Var):  {analysis_results['c_var']:.2f}%\n"
        )
        file_obj.write(
            f"Me (Mean of extremes):   "
            f"{analysis_results['mean_of_extremes'][0]:.2f} x "
            f"{analysis_results['mean_of_extremes'][1]:.2f} µm\n"
        )
        file_obj.write(
            f"Qe (Mean L/W ratio):     {analysis_results['q_e']:.2f}\n\n"
        )

        file_obj.write("-" * 60 + "\n")
        file_obj.write("FORMATTED OUTPUT\n")
        file_obj.write("-" * 60 + "\n")
        formatted_line = (
            f"{analysis_results['lmin']:.1f}-{analysis_results['lmax']:.1f} "
            f"({analysis_results['lmean']:.1f}) µm x "
            f"{analysis_results['wmin']:.1f}-{analysis_results['wmax']:.1f} "
            f"({analysis_results['wmean']:.1f}) µm; "
            f"Q={analysis_results['q_mean']:.2f}; "
            f"σ={analysis_results['q_std']:.2f}; "
            f"C={analysis_results['c_var']:.2f}%; "
            f"Me={analysis_results['mean_of_extremes'][0]:.2f} x "
            f"{analysis_results['mean_of_extremes'][1]:.2f}; "
            f"Qe={analysis_results['q_e']:.2f}\n"
        )
        file_obj.write(formatted_line)
        file_obj.write("=" * 60 + "\n")

    return log_file_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate spore dimensions from CSV with mycology parameters.")
    parser.add_argument("csv_file", help="Path to the CSV file containing 'Length' column (format: height,width)")
    args = parser.parse_args()

    if not os.path.exists(args.csv_file):
        print(f"Error: File '{args.csv_file}' does not exist.")
        sys.exit(1)

    try:
        results = calculate_spore_dimensions(args.csv_file)

        # Console output
        output = (
            f"{results['lmin']:.1f}-{results['lmax']:.1f} "
            f"({results['lmean']:.1f}) µm x "
            f"{results['wmin']:.1f}-{results['wmax']:.1f} "
            f"({results['wmean']:.1f}) µm; "
            f"Q={results['q_mean']:.2f}; σ={results['q_std']:.2f}; "
            f"C={results['c_var']:.2f}%; "
            f"Me={results['mean_of_extremes'][0]:.2f} x "
            f"{results['mean_of_extremes'][1]:.2f}; "
            f"Qe={results['q_e']:.2f}; N={results['n_spores']}"
        )
        print(output)

        # Write log file
        log_file = write_log_file(args.csv_file, results)
        print(f"\nAnalysis log saved to: {log_file}")

    except (ValueError, OSError, KeyError, pd.errors.ParserError) as error:
        print(f"Error processing file: {error}")
        sys.exit(1)
