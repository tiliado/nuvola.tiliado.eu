Nuvola Player Website
=====================

Tool to generate [Nuvola Player Website](https://nuvola.tiliado.eu).

Usage
-----

### Requirements

  * Python 3.6
  * [fxwebgen](https://github.com/tiliado/fxwebgen)

### Development

```sh
./serve.sh
```

### Deployment

```sh
cd ~/dev/repo/nuvola.tiliado.eu
make update
make publish
```

Architecture
------------

 * [Data](./data)
   - [globals.json](./data/globals.json): Global data for Jinja2 templates.
   - [distributions.json](./data/distributions.json): A list of supported distributions.
   - [apps.json](./data/apps.json): Metadata of available web app scripts.
 * [Static](./static) - static files copies as is.
 * [Templates](./templates) - Jinja2 templates
   - [snippets.html](./templates/snippets.html): Snippets used in other templates.
   - [index.html](./templates/index.html): List of apps.
   - [nuvola.html](./templates/nuvola.html): Installation instructions for Flatpak and Nuvola Player.
   - [nuvola_DISTRO.html](./templates/nuvola_debian.html): Overrides `nuvola.html` with instructions for `DISTRO`
     distribution.
   - [nuvola_DISTRO_RELEASE.html](./templates/nuvola_debian_jessie.html): Overrides `nuvola.html` with instructions 
     for `RELEASE` release of `DISTRO` distribution.
   - [app.html](./templates/app.html): Installation instructions for individual web app scripts.
   - [nuvola_DISTRO.html](./templates/app_ubuntu.html): Overrides `app.html` with instructions for `DISTRO`
     distribution.
   - app_DISTRO_RELEASE.html: Overrides `app.html` with instructions 
     for `RELEASE` release of `DISTRO` distribution.
