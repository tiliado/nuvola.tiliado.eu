from typing import Dict, Any, Union, List

from jinja2 import Environment, FileSystemLoader, select_autoescape, Template, TemplateError


def create_teplater(template_dir: str, global_vars: Dict[str, Any] = None) -> "Templater":
    env = Environment(
        loader=FileSystemLoader(template_dir),
        autoescape=select_autoescape(['html', 'xml'])
    )
    env.globals.update(global_vars)

    return Templater(env)


class Templater:
    env: Environment
    templates: Dict[str, Template]

    def __init__(self, env: Environment):
        self.env = env
        self.templates = {}

    def get_template(self, name: Union[str, List[str]]) -> Template:
        if isinstance(name, str):
            try:
                return self.templates[name]
            except KeyError:
                self.templates[name] = template = self.env.get_template(name)
                return template
        elif not name:
            raise ValueError("Template list must not be empty")
        else:
            error = None
            for item in name:
                try:
                    return self.get_template(item)
                except TemplateError as e:
                    error = e
            else:
                raise error

    def render(self, name: Union[str, List[str]], variables: Dict[str, Any]) -> str:
        return self.get_template(name).render(**variables)

