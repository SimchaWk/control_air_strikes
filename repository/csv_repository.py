import csv
from typing import List, Dict, Any


def write_to_csv(data: List[Dict[str, Any]], file_path: str, fieldnames: List[str] = None) -> bool:
    try:
        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
            if not fieldnames and data:
                fieldnames = list(data[0].keys())

            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for row in data:
                writer.writerow(row)

        return True

    except FileNotFoundError:
        print(f"Error: The directory for '{file_path}' was not found.")
    except PermissionError:
        print(f"Error: Permission denied when trying to write to '{file_path}'.")
    except Exception as e:
        print(f"An unexpected error occurred while writing to CSV: {e}")

        return False


def save_missions_to_csv(missions: List[Dict[str, Any]], file_path: str = 'missions.csv') -> bool:
    fieldnames = ['target_city', 'target_priority', 'aircraft_type', 'pilot_name', 'mission_score']

    csv_data = [
        {
            'target_city': mission['target']['city'],
            'target_priority': mission['target']['priority'],
            'aircraft_type': mission['aircraft']['type'],
            'pilot_name': mission['pilot']['name'],
            'mission_score': mission.get('score', 0)
        }
        for mission in missions
    ]

    return write_to_csv(csv_data, file_path, fieldnames)
