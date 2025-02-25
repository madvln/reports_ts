import os
import pdfkit

# Определяем корневую директорию проекта
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Пути к папкам
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
DATA_DIR = os.path.join(BASE_DIR, "data", "source")
OUTPUT_DIR = os.path.join(BASE_DIR, "pdf")

# Определяем путь к wkhtmltopdf.exe внутри проекта
PATH_TO_WKHTMLTOPDF = os.path.join(
    BASE_DIR, "tools", "wkhtmltox", "bin", "wkhtmltopdf.exe"
)

# Настройка pdfkit
CONFIG = pdfkit.configuration(wkhtmltopdf=PATH_TO_WKHTMLTOPDF)

# Количество строк для одновременной обработки
BATCH_SIZE = 4
