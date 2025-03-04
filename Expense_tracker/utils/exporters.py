import csv

def export_to_csv(data, filename):
    try:
        with open(filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(data[0].keys())  # Write header
            for row in data:
                writer.writerow(row.values())
        return True
    except Exception as e:
        print(f"Error exporting to CSV: {e}")
        return False