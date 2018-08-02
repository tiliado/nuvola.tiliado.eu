from typing import List, Dict, Any
import os
import shutil

from fxwebgen.pages import MarkdownPage, HtmlPage
from . import Templater


class Generator:
    distributions: List[Dict[str, Any]]
    apps: List[Dict[str, Any]]
    output_dir: str
    static_dirs: List[str]
    templater: Templater

    def __init__(self, distributions: List[Dict[str, Any]], apps: List[Dict[str, Any]], team: Dict[str, Any],
                 output_dir: str, static_dirs: List[str], templater: Templater, pages_dir: str = None):
        self.static_dirs = static_dirs
        self.templater = templater
        self.output_dir = output_dir
        self.distributions = distributions
        self.apps = apps
        self.team = team
        self.pages_dir = pages_dir
        maintainers = {}
        for app in apps:
            maintainer_name = app['maintainer']
            try:
                maintainer = maintainers[maintainer_name]
            except KeyError:
                maintainer = {
                    'name': maintainer_name,
                    'link': app['maintainer_link'],
                    'apps': [],
                }
                maintainers[maintainer_name] = maintainer
            maintainer['apps'].append({
                'name': app['name'],
                'link': f'/app/{app["id"]}/',
            })
        team['maintainers'] = [maintainers[key] for key in sorted(maintainers)]
        for maintainer in team['maintainers']:
            maintainer['apps'].sort(key=lambda item: item['name'])

    def purge(self):
        if os.path.isdir(self.output_dir):
            shutil.rmtree(self.output_dir, ignore_errors=True)

    def build(self):
        self.build_index()
        self.build_apps()
        self.build_nuvola()
        self.build_flatpak_refs()
        self.build_team()
        self.build_pages()
        self.copy_static_files()

    def build_index(self):
        self.build_index_for_distro(None, None)

        for distro in self.distributions:
            releases = distro.get("releases")
            if releases:
                for release in releases:
                    self.build_index_for_distro(distro, release)
            else:
                self.build_index_for_distro(distro, None)

    def build_index_for_distro(self, distro: Dict[str, Any] = None, release: Dict[str, Any] = None):
        if not distro:
            distro_spec = ""
            distro_name = None
        elif not release:
            distro_spec = "/%s" % distro["id"]
            distro_name = distro["name"] if not "releses" not in distro else None
        else:
            distro_spec = "/%s/%s" % (distro["id"], release["id"])
            if release["name"].startswith(distro["name"]):
                distro_name = release["name"]
            else:
                distro_name = "%s %s" % (distro["name"], release["name"])

        canonical_path = "/index/"
        target = os.path.join(
            self.output_dir,
            "index%s/index.html" % distro_spec if distro_spec else "index/index.html")
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, "wt") as f:
            f.write(self.templater.render("index.html", {
                'navbar_tab': 'install',
                "distributions": self.distributions,
                "distro_name": distro_name,
                "apps": self.apps,
                "distro_spec": distro_spec,
                "canonical_path": canonical_path
            }))

    def build_apps(self):
        self.build_apps_for_distro(None, None)
        for distro in self.distributions:
            self.build_apps_for_distro(distro, None)
            for release in distro.get("releases", []):
                self.build_apps_for_distro(distro, release)

    def build_apps_for_distro(self, distro: Dict[str, Any] = None, release: Dict[str, Any] = None):
        for app in self.apps:
            self.build_app_for_distro(app, distro, release)

    def build_app_for_distro(self, app, distro: Dict[str, Any] = None, release: Dict[str, Any] = None):
        templates = ["app.html"]
        if not distro:
            target = ""
            distro = self.distributions[0]
            releases = distro.get("releases")
        else:
            releases = distro.get("releases")
            if not release:
                if releases:
                    release = releases[0]
                target = "/%s" % distro["id"]
            else:
                target = "/%s/%s" % (distro["id"], release["id"])

        if not release and releases:
            release = releases[0]

        templates.insert(0, "app_%s.html" % distro["id"])
        if not release:
            distro_spec = "/%s" % distro["id"]
        else:
            distro_spec = "/%s/%s" % (distro["id"], release["id"])
            templates.insert(0, "app_%s_%s.html" % (distro["id"], release["id"]))

        canonical_path = "/app/%s%s/" % (app["id"], distro_spec)
        target = os.path.join(self.output_dir, "app/%s%s/index.html" % (app["id"], target))
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, "wt") as f:
            f.write(self.templater.render(templates, {
                'navbar_tab': 'install',
                "tab_target": "/app/" + app["id"],
                "apps": self.apps,
                "app": app,
                "distributions": self.distributions,
                "distro": distro,
                "releases": distro.get("releases"),
                "release": release,
                "distro_spec": distro_spec,
                "canonical_path": canonical_path
            }))

    def build_nuvola(self):
        self.build_nuvola_for_distro(None, None)
        for distro in self.distributions:
            self.build_nuvola_for_distro(distro, None)
            for release in distro.get("releases", []):
                self.build_nuvola_for_distro(distro, release)

    def build_nuvola_for_distro(self, distro: Dict[str, Any] = None, release: Dict[str, Any] = None):
        if not distro:
            target = ""
            distro = self.distributions[0]
            releases = distro.get("releases")
        else:
            releases = distro.get("releases")
            if not release:
                if releases:
                    release = releases[0]
                target = "/%s" % distro["id"]
            else:
                target = "/%s/%s" % (distro["id"], release["id"])

        if not release and releases:
            release = releases[0]

        templates = []
        if not release:
            distro_spec = "/%s" % distro["id"]
        else:
            distro_spec = "/%s/%s" % (distro["id"], release["id"])
            templates.append("nuvola_%s_%s.html" % (distro["id"], release["id"]))
        templates.append("nuvola_%s.html" % distro["id"])
        templates.append("nuvola.html")

        canonical_path = "/nuvola%s/" % distro_spec
        target = os.path.join(self.output_dir, "nuvola%s/index.html" % target)
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, "wt") as f:
            f.write(self.templater.render(templates, {
                'navbar_tab': 'install',
                "tab_target": "/nuvola",
                "distributions": self.distributions,
                "apps": self.apps,
                "distro": distro,
                "releases": releases,
                "release": release,
                "distro_spec": distro_spec,
                "canonical_path": canonical_path
            }))

    def build_flatpak_refs(self):
        self.build_flatpak_ref(self.templater.env.globals["nuvola"]["uid"], "nuvola")
        for app in self.apps:
            self.build_flatpak_ref(app["uid"], "app", app=app)

    def build_flatpak_ref(self, uid, template, **data):
        target = os.path.join(self.output_dir, "%s.flatpakref" % uid)
        with open(target, "wt") as f:
            f.write(self.templater.render(template + ".flatpakref", data))

    def build_team(self):
        canonical_path = "/team/"
        target = os.path.join(self.output_dir, "team/index.html")
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, "wt") as f:
            f.write(self.templater.render(['team.html'], {
                'navbar_tab': 'team',
                "team": self.team,
                "canonical_path": canonical_path
            }))

    def build_pages(self):
        if self.pages_dir:
            for root, dirs, files in os.walk(self.pages_dir):
                for path in files:
                    if path.endswith(('.md', '.html', '.html')):
                        path = os.path.join(root, path)
                        target = path[len(self.pages_dir):]
                        self.build_page(path, target)

    def build_page(self, source: str, path: str):
        page = MarkdownPage(source) if path.endswith('.md') else HtmlPage(source)
        page.process()
        meta = page.metadata
        meta.setdefault('title', os.path.splitext(os.path.basename(source))[0])
        meta.setdefault('template', 'page')
        path = meta.get('path', path)
        if not path.startswith('/'):
            path = '/' + path
        if not path.endswith(('/', '.html', '.htm')):
            path += '/'
        meta['path'] = meta['canonical_path'] = path
        target = self.output_dir + (path + 'index.html' if path.endswith('/') else path)
        template = meta['template']

        variables = {}
        variables.update(meta)

        variables['datasets'] = datasets = {}
        for name in meta.get('datasets', '').split(','):
            name = name.strip()
            if name:
                name = name.lower().replace(' ', '_').replace('-', '_')
                datasets[name] = getattr(self, name) if name in ('apps', 'distributions') else None

        snippets = {}
        for ogiginal_name in meta.get('snippets', '').split(','):
            original_name = ogiginal_name.strip()
            normalized_name = original_name.lower().replace(' ', '_').replace('-', '_')
            if original_name and normalized_name not in snippets:
                snippets[original_name] = snippets[normalized_name] = self.templater.render(
                    [f'snippets/{normalized_name}.html'], variables)
        body = page.body
        for name, content in snippets.items():
            body = body.replace(f'[Snippet: {name}]', content)
            body = body.replace(f'[snippet: {name}]', content)

        os.makedirs(os.path.dirname(target), exist_ok=True)
        variables['body'] = body
        with open(target, "wt") as f:
            f.write(self.templater.render([template + '.html'], variables))

    def copy_static_files(self):
        for static_dir in self.static_dirs:
            target = os.path.join(self.output_dir, os.path.basename(static_dir))
            if os.path.isdir(target):
                shutil.rmtree(target)
            shutil.copytree(static_dir, target)
