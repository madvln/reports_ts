import csv
import os
import glob
from config import DATA_DIR


def load_csv_data(file_path):
    data = []
    with open(file_path, "r", encoding="utf-8") as csvfile:
        csv_reader = csv.reader(csvfile)
        header = next(csv_reader)
        for row in csv_reader:
            data.append(
                {
                    "key_1": row[0],  # account_login
                    "key_2": row[1],  # password
                    "key_4": row[3],  # address
                }
            )
    return data


def get_csv_file_path_for_city(city_name):
    pattern = os.path.join(
        DATA_DIR, f"*{city_name}*.csv"
    )  # Ищем файл, содержащий city_name
    matching_files = glob.glob(pattern)  # Получаем список подходящих файлов

    if matching_files:
        return matching_files[0]  # Берем первый найденный файл
    else:
        return None  # Файл не найден


# city_name = "astrahan"
# file_path = get_csv_file_path_for_city(city_name)

# if file_path:
#     print(f"Файл найден: {file_path}")
# else:
#     print("Файл не найден")

# def get_csv_file_path_for_city(city_name):
#     return os.path.join(DATA_DIR, f"{city_name}.csv")

# from openpyxl import load_workbook


# def load_excel_data(file_path):
#     wb = load_workbook(file_path)
#     sheet = wb.active
#     data = []
#     for row in sheet.iter_rows(min_row=2, values_only=True):
#         data.append(
#             {
#                 "key_1": row[0],  # Предположим, что столбцы в Excel следующие
#                 "key_2": row[1],
#                 "key_4": row[3],
#             }
#         )
#     return data
