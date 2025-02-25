import re


def sanitize_filename(filename):
    """Удаляет запрещенные символы и заменяет пробелы на подчеркивания"""
    filename = re.sub(r'[<>:"/\\|?*]', "", filename)  # Убираем запрещенные символы
    filename = filename.replace("!", "")  # Убираем восклицательный знак
    filename = filename.strip().replace(" ", "_")  # Заменяем пробелы на подчеркивания
    return filename
