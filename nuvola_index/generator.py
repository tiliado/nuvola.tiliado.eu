from typing import List, Dict, Any
import os
import shutil

from . import Templater


class Generator:
    distributions: List[Dict[str, Any]]
    apps: List[Dict[str, Any]]
    output_dir: str
    static_dir: str
    templater: Templater

    def __init__(self, distributions: List[Dict[str, Any]], apps: List[Dict[str, Any]], output_dir: str,
                 static_dir: str, templater: Templater):
        self.static_dir = static_dir
        self.templater = templater
        self.output_dir = output_dir
        self.distributions = distributions
        self.apps = apps

    def purge(self):
        if os.path.isdir(self.output_dir):
            shutil.rmtree(self.output_dir, ignore_errors=True)

    def build(self):
        self.build_index()
        self.build_apps()
        self.build_nuvola()
        self.build_flatpak_refs()
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
        elif not release:
            distro_spec = "/%s" % distro["id"]
        else:
            distro_spec = "/%s/%s" % (distro["id"], release["id"])

        canonical_path = "/"
        target = os.path.join(self.output_dir, "index%s/index.html" % distro_spec if distro_spec else "index.html")
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, "wt") as f:
            f.write(self.templater.render("index.html", {
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

        if not release:
            distro_spec = "/%s" % distro["id"]
            template = "nuvola_%s.html" % distro["id"]
        else:
            distro_spec = "/%s/%s" % (distro["id"], release["id"])
            template = "nuvola_%s_%s.html" % (distro["id"], release["id"])

        canonical_path = "/nuvola%s/" % distro_spec
        target = os.path.join(self.output_dir, "nuvola%s/index.html" % target)
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, "wt") as f:
            f.write(self.templater.render([template, "nuvola.html"], {
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

    def copy_static_files(self):
        target = os.path.join(self.output_dir, os.path.basename(self.static_dir))
        if os.path.isdir(target):
            shutil.rmtree(target)
        shutil.copytree(self.static_dir, target)
