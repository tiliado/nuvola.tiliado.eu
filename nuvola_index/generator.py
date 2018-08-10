from typing import List, Dict, Any
import os

from fxwebgen.context import Context
from fxwebgen.postprocessor import PostProcessor
from fxwebgen.templater import Templater
from fxwebgen import generator


class Generator(generator.Generator):
    distributions: List[Dict[str, Any]]
    apps: List[Dict[str, Any]]
    team: Dict[str, Any]

    def __init__(self, distributions: List[Dict[str, Any]], apps: List[Dict[str, Any]], team: Dict[str, Any],
                 output_dir: str, static_dirs: List[str], templater: Templater, pages_dir: str = None):
        ctx = Context(templater, output_dir,
                      pages_dir=pages_dir,
                      static_dirs=static_dirs,
                      interlinks=None,
                      datasets={'distributions': distributions, 'apps': apps, 'team': team})
        super().__init__(ctx, post_processor=PostProcessor())
        self.distributions = distributions
        self.apps = apps
        self.team = team
        self.repo_pages_kind = self.resources.add_kind('repo_pages')
        self.flatpakrefs_kind = self.resources.add_kind('flatpakrefs')
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

    def before_building_pages(self) -> None:
        self.resources.remove_by_kind(self.repo_pages_kind)
        self.build_index()
        self.build_apps()
        self.build_nuvola()
        self.build_team()
        self.resources.remove_by_kind(self.flatpakrefs_kind)
        self.build_flatpak_refs()

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
        print(f'Index: {distro["id"] if distro else None} {release["id"] if release else None}')
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
            self.ctx.output_dir,
            "index%s/index.html" % distro_spec if distro_spec else "index/index.html")
        os.makedirs(os.path.dirname(target), exist_ok=True)
        self.resources.add(self.repo_pages_kind, None, target)
        with open(target, "wt") as f:
            f.write(self.ctx.templater.render("index.html", {
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
        print(f'App: {app["id"]} {distro["id"] if distro else None} {release["id"] if release else None}')
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
        target = os.path.join(self.ctx.output_dir, "app/%s%s/index.html" % (app["id"], target))
        os.makedirs(os.path.dirname(target), exist_ok=True)
        self.resources.add(self.repo_pages_kind, None, target)
        with open(target, "wt") as f:
            f.write(self.ctx.templater.render(templates, {
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
        print(f'Nuvola: {distro["id"] if distro else None} {release["id"] if release else None}')
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
        target = os.path.join(self.ctx.output_dir, "nuvola%s/index.html" % target)
        self.resources.add(self.repo_pages_kind, None, target)
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, "wt") as f:
            f.write(self.ctx.templater.render(templates, {
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
        self.build_flatpak_ref(self.ctx.templater.env.globals["nuvola"]["uid"], "nuvola")
        for app in self.apps:
            self.build_flatpak_ref(app["uid"], "app", app=app)

    def build_flatpak_ref(self, uid, template, **data):
        print(f'Flatpakref: {uid}')
        target = os.path.join(self.ctx.output_dir, "%s.flatpakref" % uid)
        self.resources.add(self.flatpakrefs_kind, None, target)
        with open(target, "wt") as f:
            f.write(self.ctx.templater.render(template + ".flatpakref", data))

    def build_team(self):
        canonical_path = "/team/"
        target = os.path.join(self.ctx.output_dir, "team/index.html")
        os.makedirs(os.path.dirname(target), exist_ok=True)
        self.resources.add(self.repo_pages_kind, None, target)
        with open(target, "wt") as f:
            f.write(self.ctx.templater.render(['team.html'], {
                'navbar_tab': 'team',
                "team": self.team,
                "canonical_path": canonical_path
            }))
