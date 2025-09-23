#!/usr/bin/env python3
import os
import re
import csv
import sys

# ----------------------------
# Argument parsing
# ----------------------------
if len(sys.argv) != 3:
    print("Usage: python3 check_cells.py <path_to_cells> <cell_list_file | -all>")
    sys.exit(1)

base_dir = sys.argv[1]
cell_list_arg = sys.argv[2]

# ----------------------------
# Cell list
# ----------------------------
if cell_list_arg.lower() == "-all":
    cell_list = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]
else:
    # Read cell names from file
    if not os.path.isfile(cell_list_arg):
        print(f"Cell list file {cell_list_arg} not found.")
        sys.exit(1)
    with open(cell_list_arg, 'r') as f:
        cell_list = [line.strip() for line in f if line.strip()]

# ----------------------------
# Arguments to check
# ----------------------------
common_args = [
    "ArchkRunDate", "CellArea", "CellHeight", "CellHeightGrids",
    "CellWidth", "CellWidthGrids", "DiffAreas", "GDSCellName",
    "GateAreas", "LefGeneration", "NumTransistors", "RawGateDensity",
    "TransistorsPerGrid", "pin_V"
]

extra_args = ["IntNode_", "NoCKSkew_", "NACKSkew_"]

special_pattern = re.compile(r'^(fs|fd|fr|sync)|(_fs|_fd|_fr|_sync)', re.IGNORECASE)

# ----------------------------
# Check each cell
# ----------------------------
results = {}

for cell_name in cell_list:
    cell_path = os.path.join(base_dir, cell_name)
    if os.path.isdir(cell_path):
        info_file = os.path.join(cell_path, f"{cell_name}.info")
        if os.path.isfile(info_file):
            with open(info_file, 'r', errors='ignore') as f:
                content = f.read()

            # Determine args to check
            args_to_check = list(common_args)
            if special_pattern.search(cell_name):
                args_to_check += extra_args

            # Find missing args
            missing = [arg for arg in args_to_check if arg not in content]

            results[cell_name] = {
                'file': info_file,
                'missing': missing
            }
        else:
            results[cell_name] = {
                'file': None,
                'missing': ['Info file not found']
            }
    else:
        results[cell_name] = {
            'file': None,
            'missing': ['Cell directory not found']
        }

# ----------------------------
# Summarize
# ----------------------------
failed_cells = sum(1 for cell in results if results[cell]['missing'])
total_missing_args = sum(len(data['missing']) for data in results.values())

if failed_cells == 0:
    summary = "All cells Passed"
else:
    summary = f"Failed cells were missing {total_missing_args} arguments"

# ----------------------------
# Write CSV report
# ----------------------------
report_file = "cell_check_report.csv"
with open(report_file, 'w', newline='') as csvfile:
    fieldnames = ['Cell', 'Info File', 'Missing Arguments']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for cell, data in sorted(results.items()):
        missing_str = ', '.join(data['missing']) if data['missing'] else 'None'
        writer.writerow({
            'Cell': cell,
            'Info File': data['file'] if data['file'] else 'Not found',
            'Missing Arguments': missing_str
        })

    # Add summary as the last row
    writer.writerow({'Cell': 'SUMMARY', 'Info File': '', 'Missing Arguments': summary})

# ----------------------------
# Print results to console
# ----------------------------
for cell, data in sorted(results.items()):
    print(f"\nCell: {cell}")
    if data['file']:
        print(f"  Info file: {data['file']}")
        if data['missing']:
            print(f"  Missing arguments: {', '.join(data['missing'])}")
        else:
            print("  All required arguments present.")
    else:
        print("  Info file not found.")

print("\n" + "=" * 60)
print("SUMMARY:")
print(summary)
print(f"Report file created: {os.path.abspath(report_file)}")
print("=" * 60)