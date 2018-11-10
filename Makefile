MODULE := tools

info:
	cat Makefile
test:
	python3.6 -m nuvola_index -f 'http://127.0.0.1:8000/'
	cd build && python3 -m http.server
update:
	python3.6 ./update_apps.py \
    -l ~/dev/projects/nuvolaplayer3/flatpak/recipes.yaml \
    -d ~/dev/projects/nuvolaplayer3/apps
	git add data/apps.json && git commit -m "Update apps.json"

generate:
	python3.6 -m nuvola_index -f 'https://nuvola.tiliado.eu/'
publish: generate
	cd ~/dev/projects/fxdepl && ./fxdepl.py push -s server3.tiliado.eu -p nuvola.tiliado.eu -R

check: flake8 pylint

flake8:
	flake8 $(MODULE)

pylint:
	pylint --rcfile .pylintrc $(MODULE)

venv: requirements.txt requirements-devel.txt
	python3 -m venv venv
	venv/bin/python3 -m pip install --upgrade pip
	venv/bin/python3 -m pip install --upgrade -r requirements.txt
	venv/bin/python3 -m pip install --upgrade -r requirements-devel.txt
	touch venv

distclean:
	rm -rf venv
