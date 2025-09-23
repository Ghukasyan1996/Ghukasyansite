import os
import re
import csv

# Base directory
base_dir = "Review_MAP/cells"

# Always required arguments
common_args = [
    "ArchkRunDate", "CellArea", "CellHeight", "CellHeightGrids",
    "CellWidth", "CellWidthGrids", "DiffAreas", "GDSCellName",
    "GateAreas", "LefGeneration", "NumTransistors", "RawGateDensity",
    "TransistorsPerGrid", "pin_V"
]

# Additional arguments only for special cell names
extra_args = ["IntNode_", "NoCKSkew_", "NACKSkew_"]

# Regex to identify special cell names
special_pattern = re.compile(r'^(fs|fd|fr|sync)|(_fs|_fd|_fr|_sync)', re.IGNORECASE)

results = {}

# Check all cells
for cell_name in os.listdir(base_dir):
    cell_path = os.path.join(base_dir, cell_name)
    if os.path.isdir(cell_path):
        info_file = os.path.join(cell_path, f"{cell_name}.info")
        if os.path.isfile(info_file):
            with open(info_file, 'r', errors='ignore') as f:
                content = f.read()

            # Base arguments to check
            args_to_check = list(common_args)

            # Add extra args if cell matches pattern
            if special_pattern.search(cell_name):
                args_to_check += extra_args

            # Find missing arguments
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

# Count totals for summary
total_cells = len(results)
failed_cells = sum(1 for cell in results if results[cell]['missing'])

# Generate CSV report
report_file = "cell_check_report.csv"
with open(report_file, 'w', newline='') as csvfile:
    fieldnames = ['Cell', 'Info File', 'Missing Arguments']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for cell, data in sorted(results.items()):
        missing_str = ', '.join(data['missing']) if data['missing'] else ''
        writer.writerow({
            'Cell': cell,
            'Info File': data['file'] if data['file'] else 'Not found',
            'Missing Arguments': missing_str if missing_str else 'None'
        })

# Print per-cell status
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

# Print summary
if failed_cells == 0:
    summary = "All cells passed"
else:
    total_missing_args = sum(len(data['missing']) for data in results.values())
    summary = f"Failed cells were missing {total_missing_args} arguments"

print("\n" + "=" * 60)
print("SUMMARY:")
print(summary)
print(f"Report file created: {os.path.abspath(report_file)}")
print("=" * 60)