from .pars import Pars_minimal, Pars_with_date_and_time
import csv
import json
from datetime import datetime
from typing import List


# Экспорт в текстовый файл
def export_to_text(objects: List[Pars_minimal], filename: str):
    with open(filename, 'w', encoding='utf-8') as file:
        for obj in objects:
            file.write(str(obj) + '\n')


# Экспорт в CSV файл
def export_to_csv(objects: List[Pars_minimal], filename: str):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        fieldnames = ["name", "group", "auditorium", "date", "timestamp"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        for obj in objects:
            writer.writerow(obj.to_dict())


# Экспорт в JSON файл
def export_to_json(objects: List[Pars_minimal], filename: str):
    data = [obj.to_dict() for obj in objects]
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)