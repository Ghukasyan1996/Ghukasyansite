import os

# Base directory
base_dir = "Review_MAP/cells"

# Required arguments to check
required_args = [
    "ArchkRunDate", "CellArea", "CellHeight", "CellHeightGrids", "CellWidth",
    "CellWidthGrids", "DiffAreas", "GDSCellName", "GateAreas", "LefGeneration",
    "NumTransistors", "RawGateDensity", "TransistorsPerGrid", "pin_VNW_N",
    "pin_VPW_P", "NACKSkew_", "NoCKSkew_", "IntNode_"
]

# Dictionary to store results
results = {}

for cell_name in os.listdir(base_dir):
    cell_path = os.path.join(base_dir, cell_name)
    if os.path.isdir(cell_path):  # Only directories
        info_file = os.path.join(cell_path, f"{cell_name}.info")
        if os.path.isfile(info_file):
            with open(info_file, 'r', errors='ignore') as f:
                content = f.read()

            missing = [arg for arg in required_args if arg not in content]
            results[cell_name] = {
                'file': info_file,
                'missing': missing
            }
        else:
            results[cell_name] = {
                'file': None,
                'missing': 'Info file not found'
            }

# Print report
for cell, data in results.items():
    print(f"\nCell: {cell}")
    if data['file']:
        print(f"  Info file: {data['file']}")
        if data['missing']:
            print(f"  Missing arguments: {', '.join(data['missing'])}")
        else:
            print("  All required arguments present.")
    else:
        print("  Info file not found.")