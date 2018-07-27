import json
import os
from typing import Dict, Any, Union, List, Tuple

from jinja2 import Environment, FileSystemLoader, select_autoescape, Template, TemplateError


def todict(value, key):
    return {item[key]: item for item in value or []}


def create_templater(template_dir: str, global_vars: Dict[str, Any] = None) -> "Templater":
    env = Environment(
        loader=FileSystemLoader(template_dir),
        autoescape=select_autoescape(['html', 'xml'])
    )
    env.globals.update(global_vars)
    env.filters['todict'] = todict
    return Templater(template_dir, env)


class Templater:
    env: Environment
    templates: Dict[str, Tuple[Template, dict]]

    def __init__(self, template_dir: str, env: Environment):
        self.template_dir = template_dir
        self.env = env
        self.templates = {}

    def load_template_data(self, name: str) -> dict:
        path = os.path.join(self.template_dir, os.path.splitext(name)[0] + '.json')
        if os.path.isfile(path):
            with open(path) as fh:
                return json.load(fh)
        return {}

    def get_template(self, name: Union[str, List[str]]) -> Tuple[Template, dict]:
        if isinstance(name, str):
            try:
                return self.templates[name]
            except KeyError:
                template = self.env.get_template(name)
                data = self.load_template_data(name)
                result = template, data
                self.templates[name] = result
                return result
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
        template, data = self.get_template(name)
        variables.setdefault('data', data)
        return template.render(**variables)

