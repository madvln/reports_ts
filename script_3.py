from docx import Document
import openpyxl
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors

import os
import time

DATA_DIR = "data/source"
TEMPLATES_DIR = "template/source"
PDF_DIR = "pdf/creating_new_pdf"

# Создаем папку для PDF, если ее нет
os.makedirs(PDF_DIR, exist_ok=True)


def create_pdf(filename, content):
    """Создает PDF файл с заданным содержимым."""

    # 1. Регистрируем шрифт (если он еще не зарегистрирован)
    pdfmetrics.registerFont(
        TTFont("ArialUnicode", "template/fonts/Arial Unicode MS.ttf")
    )  # Замените 'Arial Unicode.ttf' на путь к вашему файлу шрифта

    c = canvas.Canvas(filename, pagesize=letter)
    c.setFont("ArialUnicode", 12)  # Устанавливаем шрифт и размер

    textobject = c.beginText()
    textobject.setTextOrigin(10, 730)  # Отступ от левого нижнего угла
    textobject.setFillColor(colors.black)  # Задаем цвет текста

    for line in content.splitlines():
        textobject.textLine(line)

    c.drawText(textobject)
    c.save()


def process_files(docx_file, excel_file):
    """
    Обрабатывает файлы Word и Excel для создания PDF файлов.

    Args:
        docx_file (str): Путь к файлу Word (.docx).
        excel_file (str): Путь к файлу Excel (.xlsx).
    """

    # 1. Чтение данных из Word файла
    try:
        doc = Document(docx_file)
        word_content = ""
        for paragraph in doc.paragraphs:
            word_content += paragraph.text
        print(f"Содержимое Word: {word_content}")  # Для отладки
    except FileNotFoundError:
        print(f"Ошибка: Файл Word не найден: {docx_file}")
        return
    except Exception as e:
        print(f"Ошибка при чтении Word файла: {e}")
        return

    # 2. Чтение данных из Excel файла
    try:
        workbook = openpyxl.load_workbook(excel_file)
        sheet = workbook.active  # Получаем активный лист
        data = []
        for row in sheet.iter_rows(
            min_row=2, values_only=True
        ):  # Начинаем со второй строки (после заголовков)
            data.append(row)
        print(f"Данные Excel: {data}")  # Для отладки
    except FileNotFoundError:
        print(f"Ошибка: Файл Excel не найден: {excel_file}")
        return
    except Exception as e:
        print(f"Ошибка при чтении Excel файла: {e}")
        return

    # 3. Создание PDF файлов на основе данных из Word и Excel
    for row in data:
        номер = row[0]  # Первый столбец - номер
        сообщение = row[1]  # Второй столбец - сообщение

        # Подставляем значения из Excel в шаблон из Word
        pdf_content = word_content.replace("key_1", сообщение).replace("key_2", номер)

        # Создаем имя файла PDF
        pdf_filename = f"output_{номер}.pdf"

        # Создаем PDF файл
        create_pdf(os.path.join(PDF_DIR, pdf_filename), pdf_content)
        print(f"Создан PDF файл: {pdf_filename}")


# Пример использования
if __name__ == "__main__":
    start = time.time()
    word_file = os.path.join(TEMPLATES_DIR, "word_1.docx")
    excel_file = os.path.join(DATA_DIR, "excel_1.xlsx")
    process_files(word_file, excel_file)
    end = time.time()
    print(round(end - start, 2))
