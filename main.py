import os
from concurrent.futures import ThreadPoolExecutor
import math
from config import OUTPUT_DIR, BATCH_SIZE, TEMPLATES_DIR
from data_loader import load_csv_data, get_csv_file_path_for_city
from html_renderer import render_html
from pdf_converter import convert_html_to_pdf
from sanitazer import sanitize_filename

# Количество потоков для обработки городов
NUM_CITY_THREADS = 4
# Количество потоков для создания PDF внутри каждого города
NUM_PDF_THREADS = 4


def generate_pdfs_for_city(city_name):
    data_file = get_csv_file_path_for_city(city_name)
    data = load_csv_data(data_file)
    city_output_dir = os.path.join(OUTPUT_DIR, city_name)
    os.makedirs(city_output_dir, exist_ok=True)
    template_name = f"{city_name}.htm"

    num_batches = math.ceil(len(data) / BATCH_SIZE)

    def process_batch(batch_data):
        """Функция для параллельной обработки одного пакета данных."""
        pdf_filenames = []
        pdf_paths = []
        row_datas = []

        for row_data in batch_data:
            if row_data["key_4"] is None or row_data["key_4"] == "":
                row_data["key_4"] = "Без указания улицы"
                pdf_filename = f"{row_data['key_1']} {row_data['key_4']}.pdf"
                pdf_path = os.path.join(city_output_dir, row_data["key_4"])
            else:
                # address = row_data["key_4"].replace('"', "")
                address = sanitize_filename(row_data["key_4"])
                pdf_filename = f"{row_data['key_1']} {address}.pdf"
                if "," in address:
                    pdf_path = os.path.join(
                        city_output_dir, address.split(",")[1].strip()
                    )
                else:
                    pdf_path = os.path.join(city_output_dir, address.strip())

            os.makedirs(pdf_path, exist_ok=True)
            pdf_path = os.path.join(pdf_path, pdf_filename)

            if os.path.exists(pdf_path):
                continue

            pdf_filenames.append(pdf_filename)
            pdf_paths.append(pdf_path)
            row_datas.append(row_data)

        # Рендерим HTML
        html_contents = render_html(template_name, row_datas)
        # Конвертируем HTML в PDF
        convert_html_to_pdf(html_contents, pdf_paths)

    # Используем ThreadPoolExecutor для параллельной обработки пакетов
    with ThreadPoolExecutor(max_workers=NUM_PDF_THREADS) as pdf_executor:
        for i in range(num_batches):
            start_index = i * BATCH_SIZE
            end_index = min((i + 1) * BATCH_SIZE, len(data))
            batch_data = data[start_index:end_index]
            pdf_executor.submit(process_batch, batch_data)


def generate_pdfs():
    cities = [
        filename.split(".")[0]
        for filename in os.listdir(TEMPLATES_DIR)
        if filename.endswith(".htm")
    ]

    with ThreadPoolExecutor(max_workers=NUM_CITY_THREADS) as city_executor:
        city_executor.map(generate_pdfs_for_city, cities)


if __name__ == "__main__":
    generate_pdfs()
