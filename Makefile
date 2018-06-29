test:
	python3.6 -m nuvola_index -f 'http://127.0.0.1:8000/'
	cd build && python3 -m http.server
update:
	python3.6 ./update_apps.py \
    -l ~/dev/projects/nuvolaplayer3/flatpak/recipes.yaml \
    -d ~/dev/projects/nuvolaplayer3/apps
	git add data/apps.json && git commit -m "Update apps.json"
publish:
	python3.6 -m nuvola_index -f 'https://nuvola.tiliado.eu/'
	if [ -z "${http_proxy}" ]; then \
		cd ~/dev/projects/fxdepl && ./fxdepl.py push -s v2.tiliado.eu -p nuvola.tiliado.eu -R; \
	else \
		cd ~/dev/projects/fxdepl && ./fxdepl.py push -s v2.tiliado.eu.vscht -p nuvola.tiliado.eu -R; \
	fi
