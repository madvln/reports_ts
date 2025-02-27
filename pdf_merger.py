import os
from PyPDF2 import PdfMerger


def merge_pdfs_in_subfolders(base_folder):
    """Проходит по всем папкам с доставщиками и объединяет их PDF в один файл."""

    for city in os.listdir(base_folder):
        city_path = os.path.join(base_folder, city)
        if not os.path.isdir(city_path):
            continue  # Пропускаем, если это не папка

        for deliverer in os.listdir(city_path):
            deliverer_path = os.path.join(city_path, deliverer)
            if not os.path.isdir(deliverer_path):
                continue  # Пропускаем, если это не папка

            pdf_files = sorted(
                [f for f in os.listdir(deliverer_path) if f.endswith(".pdf")]
            )  # Получаем список PDF и сортируем

            if not pdf_files:
                continue  # Пропускаем, если в папке нет PDF

            merged_pdf_path = os.path.join(deliverer_path, f"{deliverer}.pdf")
            pdf_merger = PdfMerger()

            for pdf in pdf_files:
                pdf_merger.append(os.path.join(deliverer_path, pdf))

            pdf_merger.write(merged_pdf_path)  # Сохраняем объединенный PDF
            pdf_merger.close()

            # Удаляем исходные PDF после объединения
            for pdf in pdf_files:
                os.remove(os.path.join(deliverer_path, pdf))

            print(f"Объединенный PDF создан: {merged_pdf_path}")


# Пример вызова
merge_pdfs_in_subfolders("pdf")
