from jinja2 import Environment, FileSystemLoader
from config import TEMPLATES_DIR


def render_html(template_name, data_list):  # принимает список данных
    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
    template = env.get_template(template_name)
    # Рендерит HTML для каждого набора данных и объединяет результаты
    return [template.render(data) for data in data_list]
