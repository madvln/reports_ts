import os
import pandas as pd
from docxtpl import DocxTemplate
from docx2pdf import convert

# Пути к папкам
DATA_DIR = "data"
TEMPLATES_DIR = "template"
PDF_DIR = "pdf"

# Создаем папку для PDF, если ее нет
os.makedirs(PDF_DIR, exist_ok=True)


# Функция для извлечения города из имени файла
def get_city_from_filename(filename):
    # Убираем расширение и префикс "data_"
    return filename.replace("data_", "").replace(".xlsx", "")


# Получаем список всех файлов Excel в папке data
excel_files = [f for f in os.listdir(DATA_DIR) if f.endswith(".xlsx")]

# Обрабатываем каждый файл Excel
for excel_file in excel_files:
    # Получаем название города из имени файла
    city = get_city_from_filename(excel_file)

    # Путь к файлу Excel
    excel_path = os.path.join(DATA_DIR, excel_file)

    # Загружаем данные из Excel
    df = pd.read_excel(excel_path)

    # Путь к шаблону для города
    template_path = os.path.join(TEMPLATES_DIR, f"{city}.docx")

    # Проверяем, существует ли шаблон для города
    if not os.path.exists(template_path):
        print(f"Шаблон для города {city} не найден. Пропускаем.")
        continue

    # Загружаем шаблон
    doc = DocxTemplate(template_path)

    # Создаем папку для города в PDF, если ее нет
    city_pdf_dir = os.path.join(PDF_DIR, city)
    os.makedirs(city_pdf_dir, exist_ok=True)

    # Обрабатываем каждую строку в таблице
    for index, row in df.iterrows():
        # Получаем данные из строки
        login = row[0]
        password = row[1]
        address = row[3]  # Столбец с адресом

        # Создаем контекст для замены ключей
        context = {
            "key_1": login,
            "key_2": password,
            "key_4": address,
        }

        # Заполняем шаблон данными
        doc.render(context)

        # Сохраняем временный Word-файл
        temp_docx_path = os.path.join(city_pdf_dir, f"{login}.docx")
        doc.save(temp_docx_path)

        # Конвертируем Word в PDF
        pdf_path = os.path.join(city_pdf_dir, f"{login}.pdf")
        convert(temp_docx_path, pdf_path)

        # Удаляем временный Word-файл
        os.remove(temp_docx_path)

        print(f"Создан PDF для {login} в папке {city_pdf_dir}")
