import pdfkit
from config import CONFIG


def convert_html_to_pdf(html_contents, output_paths):  # принимает списки html и путей
    # Преобразует каждый HTML-контент в PDF, используя соответствующий путь
    for html_content, output_path in zip(html_contents, output_paths):
        pdfkit.from_string(html_content, output_path, configuration=CONFIG)
