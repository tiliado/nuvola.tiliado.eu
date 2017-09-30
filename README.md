Nuvola Apps Repository Index
============================

Tool to generate [Nuvola Apps Repository Index](https://nuvola.tiliado.eu).

Usage
-----

### Requirements

  * Python 3.6
  * Jinja2: `python3.6 -m pip install -U Jinja2`
  * PyYAML: `python3.6 -m pip install PyYAML`
  * css-html-js-minify: `python3.6 -m pip install css-html-js-minify`

### Development

```sh
python3.6 -m nuvola_index -f 'http://127.0.0.1:8000/'
cd build; python3 -m http.server &
cd ..
python3.6 -m nuvola_index 'http://127.0.0.1:8000/'

```

### Deployment

```sh
cd ~/dev/projects/nuvolaplayer3/nuvola-apps-repository-index
python3.6 ./update_apps.py \
    -l ~/dev/projects/nuvolaplayer3/flatpak/recipes.yaml \
    -d ~/dev/projects/nuvolaplayer3/apps
git status
git add data/apps.json && git commit -m "Update apps.json"
python3.6 -m nuvola_index -f 'https://nuvola.tiliado.eu/'
python3.6 /usr/local/bin/css-html-js-minify.py --overwrite build
cd ~/dev/projects/fxdepl
./fxdepl.py push -s v2.tiliado.eu -p nuvola.tiliado.eu -R
./fxdepl.py push -s v2.tiliado.eu.vscht -p nuvola.tiliado.eu -R
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
   - [nuvola.html](./templates/nuvola.html): Installation instructions for Flatpak and Nuvola Apps Runtime.
   - [nuvola_DISTRO.html](./templates/nuvola_debian.html): Overrides `nuvola.html` with instructions for `DISTRO`
     distribution.
   - [nuvola_DISTRO_RELEASE.html](./templates/nuvola_debian_jessie.html): Overrides `nuvola.html` with instructions 
     for `RELEASE` release of `DISTRO` distribution.
   - [app.html](./templates/app.html): Installation instructions for individual web app scripts.
   - [nuvola_DISTRO.html](./templates/app_ubuntu.html): Overrides `app.html` with instructions for `DISTRO`
     distribution.
   - app_DISTRO_RELEASE.html: Overrides `app.html` with instructions 
     for `RELEASE` release of `DISTRO` distribution.
