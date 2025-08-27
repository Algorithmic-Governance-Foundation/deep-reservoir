#!/usr/bin/env python3
"""
Script to combine results from different model CSV files into a consolidated format.
Combines gpt-4-1.csv, gpt-4o-mini-2-pass.csv, and sonar-pro-2.csv into a new CSV
with format: Policy, Country, [GPT-4-1], [GPT-4o-Mini-2-Pass], [Sonar-Pro-2]
"""

import csv
from pathlib import Path

def main():
    # Define input files and their short names for headers
    input_files = {
        'results/gpt-4-1.csv': 'GPT-4-1',
        'results/gpt-4o-mini-2-pass.csv': 'GPT-4o-Mini-2-Pass', 
        'results/sonar-pro-2.csv': 'Sonar-Pro-2'
    }
    
    output_file = 'results/combined_results.csv'
    
    # Dictionary to store results: (policy, country) -> {model: status}
    results = {}
    
    # Read each input file
    for file_path, model_name in input_files.items():
        if not Path(file_path).exists():
            print(f"Warning: {file_path} not found, skipping...")
            continue
            
        print(f"Reading {file_path}...")
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                key = (row['policy'], row['country'])
                if key not in results:
                    results[key] = {}
                results[key][model_name] = row['status']
    
    # Write combined results
    print(f"Writing combined results to {output_file}...")
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        fieldnames = ['Policy', 'Country'] + list(input_files.values())
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for (policy, country), model_results in sorted(results.items()):
            row = {
                'Policy': policy,
                'Country': country
            }
            # Add results for each model, defaulting to empty string if missing
            for model_name in input_files.values():
                row[model_name] = model_results.get(model_name, '')
            
            writer.writerow(row)
    
    print(f"Successfully created {output_file} with {len(results)} policy-country combinations")

if __name__ == '__main__':
    main()