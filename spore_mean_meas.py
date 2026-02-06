import pandas as pd
import argparse
import os
import sys
from datetime import datetime

def calculate_spore_dimensions(csv_file_path):
    """
    Reads a CSV file with 'Length' column formatted as 'height,width' strings
    and returns the spore size statistics including mycology parameters.
    """
    df = pd.read_csv(csv_file_path)

    # Split 'Length' into Height and Width
    df[['Height', 'Width']] = df['Length'].str.split(',', expand=True).astype(float)

    # Calculations
    lmin = df['Height'].min()
    lmax = df['Height'].max()
    lmean = df['Height'].mean()
    lstd = df['Height'].std()

    wmin = df['Width'].min()
    wmax = df['Width'].max()
    wmean = df['Width'].mean()
    wstd = df['Width'].std()

    df['Q'] = df['Height'] / df['Width']
    Qmean = df['Q'].mean()
    Qstd = df['Q'].std()
    
    # Mycology parameters
    # C = Coefficient of variation of length
    C = 100 - ((lstd / lmean) * 100 if lmean != 0 else 0)
    
    # Me = Mean of extremes (average of min and max length)
    Me = [(lmin + lmax) / 2, (wmin + wmax) / 2]
    
    # Qe = Q value at extremes (ratio of mean length to mean width)
    Qe = lmean / wmean if wmean != 0 else 0

    return lmin, lmax, lmean, wmin, wmax, wmean, Qmean, Qstd, C, Me, Qe, len(df)

def write_log_file(csv_file_path, results):
    """
    Writes the results to a log file in the same directory as the CSV.
    """
    log_file_path = csv_file_path.replace('.csv', '_analysis.log')
    
    lmin, lmax, lmean, wmin, wmax, wmean, Qmean, Qstd, C, Me, Qe, n_spores = results
    
    with open(log_file_path, 'w', encoding='utf-8') as f:
        f.write("=" * 60 + "\n")
        f.write("SPORE DIMENSION ANALYSIS REPORT\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Input File: {csv_file_path}\n")
        f.write(f"Number of Spores Measured: {n_spores}\n\n")
        
        f.write("-" * 60 + "\n")
        f.write("DIMENSION STATISTICS\n")
        f.write("-" * 60 + "\n")
        f.write(f"Length (L):  {lmin:.1f}-{lmax:.1f} µm (mean: {lmean:.1f} µm)\n")
        f.write(f"Width (W):   {wmin:.1f}-{wmax:.1f} µm (mean: {wmean:.1f} µm)\n\n")
        
        f.write("-" * 60 + "\n")
        f.write("MYCOLOGY PARAMETERS\n")
        f.write("-" * 60 + "\n")
        f.write(f"Q (L/W ratio):           {Qmean:.2f} (σ = {Qstd:.2f})\n")
        f.write(f"C (Coefficient of Var):  {C:.2f}%\n")
        f.write(f"Me (Mean of extremes):   {Me[0]:.2f} x {Me[1]:.2f} µm\n")
        f.write(f"Qe (Mean L/W ratio):     {Qe:.2f}\n\n")
        
        f.write("-" * 60 + "\n")
        f.write("FORMATTED OUTPUT\n")
        f.write("-" * 60 + "\n")
        f.write(f"{lmin:.1f}-{lmax:.1f} ({lmean:.1f}) µm x {wmin:.1f}-{wmax:.1f} ({wmean:.1f}) µm; ")
        f.write(f"Q={Qmean:.2f}; σ={Qstd:.2f}; C={C:.2f}%; Me={Me[0]:.2f} x {Me[1]:.2f}; Qe={Qe:.2f}\n")
        f.write("=" * 60 + "\n")
    
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
        lmin, lmax, lmean, wmin, wmax, wmean, Qmean, Qstd, C, Me, Qe, n_spores = results
        
        # Console output
        output = f"{lmin:.1f}-{lmax:.1f} ({lmean:.1f}) µm x {wmin:.1f}-{wmax:.1f} ({wmean:.1f}) µm; "
        output += f"Q={Qmean:.2f}; σ={Qstd:.2f}; C={C:.2f}%; Me={Me[0]:.2f} x {Me[1]:.2f}; Qe={Qe:.2f}"
        print(output)
        
        # Write log file
        log_file = write_log_file(args.csv_file, results)
        print(f"\nAnalysis log saved to: {log_file}")
        
    except Exception as e:
        print(f"Error processing file: {e}")
        sys.exit(1)
