import pdfkit

# Пути к папкам
TEMPLATES_DIR = "templates"
DATA_DIR = r"data\source"
OUTPUT_DIR = "pdf"
PATH_TO_WKHTMLTOPDF = (
    r"C:\Users\tarakanchikoves\source\reports_ts\wkhtmltox\bin\wkhtmltopdf.exe"
)
CONFIG = pdfkit.configuration(wkhtmltopdf=PATH_TO_WKHTMLTOPDF)
BATCH_SIZE = 4  # Количество строк для одновременной обработки
