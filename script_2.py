import comtypes.client
import os
from docx import Document
import openpyxl
import time


def convert_word_to_pdf(word_file, pdf_file):
    """Конвертирует Word файл в PDF, используя comtypes."""
    try:
        word = comtypes.client.CreateObject("Word.Application")
        word.Visible = (
            False  # Сделать Word невидимым (можете установить True для отладки)
        )
        doc = word.Documents.Open(
            os.path.abspath(word_file)
        )  # Используем абсолютный путь
        doc.SaveAs(pdf_file, FileFormat=17)  # 17 соответствует PDF
        doc.Close()
        word.Quit()
        print(f"Файл {word_file} успешно конвертирован в {pdf_file}")
    except Exception as e:
        print(f"Ошибка при конвертации {word_file} в PDF: {e}")


def process_files(docx_file, excel_file):
    """
    Обрабатывает файлы Word и Excel для создания PDF файлов, сохраняя форматирование.

    Args:
        docx_file (str): Путь к файлу Word (.docx).
        excel_file (str): Путь к файлу Excel (.xlsx).
    """

    # 1. Чтение данных из Excel файла
    try:
        workbook = openpyxl.load_workbook(excel_file)
        sheet = workbook.active  # Получаем активный лист
        data = []
        for row in sheet.iter_rows(
            min_row=2, values_only=True
        ):  # Начинаем со второй строки (после заголовков)
            data.append(row)
        # print(f"Данные Excel: {data}") # Для отладки
    except FileNotFoundError:
        print(f"Ошибка: Файл Excel не найден: {excel_file}")
        return
    except Exception as e:
        print(f"Ошибка при чтении Excel файла: {e}")
        return

    # 2. Для каждой строки из Excel создаем PDF
    for row in data:
        номер = row[0]  # Первый столбец - номер
        сообщение = row[1]  # Второй столбец - сообщение

        # 3. Создаем временный Word файл с подставленными значениями
        pdf_filename = f"output_{номер}.pdf"
        temp_docx_file = f"temp_{номер}.docx"

        try:
            doc = Document(docx_file)
            for paragraph in doc.paragraphs:
                # Заменяем значения в параграфах
                paragraph.text = paragraph.text.replace(
                    "key_1", str(сообщение)
                ).replace(
                    "key_2", str(номер)
                )  # Явно преобразуем в строку

            doc.save(temp_docx_file)
            # Генерируем абсолютный путь к PDF файлу
            pdf_filename = os.path.abspath(pdf_filename)  # <---- ВАЖНОЕ ИЗМЕНЕНИЕ
            # 4. Конвертируем временный Word файл в PDF
            convert_word_to_pdf(temp_docx_file, pdf_filename)

        except FileNotFoundError:
            print(f"Ошибка: Файл Word не найден: {docx_file}")
            return
        except Exception as e:
            print(f"Ошибка при обработке Word файла: {e}")
            return

        finally:
            # 5. Удаляем временный Word файл (если он был создан)
            try:
                os.remove(temp_docx_file)
            except OSError:
                pass  # Файл мог не быть создан, ничего страшного


# Пример использования
if __name__ == "__main__":
    start = time.time()
    word_file = "word_1.docx"
    excel_file = "excel_1.xlsx"
    process_files(word_file, excel_file)
    end = time.time()
    print(round(end - start, 2))
