import os
from PyPDF2 import PdfMerger
from concurrent.futures import ThreadPoolExecutor


def merge_pdfs_for_deliverer(deliverer_path, deliverer_name):
    """Объединяет PDF-файлы для одного доставщика."""
    pdf_files = sorted([f for f in os.listdir(deliverer_path) if f.endswith(".pdf")])

    if not pdf_files:
        return  # Если в папке нет PDF, ничего не делаем

    merged_pdf_path = os.path.join(deliverer_path, f"{deliverer_name}.pdf")
    pdf_merger = PdfMerger()

    for pdf in pdf_files:
        pdf_merger.append(os.path.join(deliverer_path, pdf))

    pdf_merger.write(merged_pdf_path)
    pdf_merger.close()

    # Удаляем исходные PDF после объединения
    for pdf in pdf_files:
        os.remove(os.path.join(deliverer_path, pdf))

    print(f"Объединенный PDF создан: {merged_pdf_path}")


def merge_pdfs_in_subfolders(base_folder, num_threads=2):
    """Проходит по папкам с доставщиками и объединяет их PDF в один файл, используя многопоточность."""
    tasks = []

    for city in os.listdir(base_folder):
        city_path = os.path.join(base_folder, city)
        if not os.path.isdir(city_path):
            continue

        for deliverer in os.listdir(city_path):
            deliverer_path = os.path.join(city_path, deliverer)
            if not os.path.isdir(deliverer_path):
                continue

            tasks.append((deliverer_path, deliverer))

    # Используем ThreadPoolExecutor для запуска задач параллельно
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        executor.map(lambda args: merge_pdfs_for_deliverer(*args), tasks)


# Пример вызова
merge_pdfs_in_subfolders("pdf", num_threads=4)
