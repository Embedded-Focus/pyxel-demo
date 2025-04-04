app2html: package
	pyxel app2html build.pyxapp
	mv build.html shoot.html

.PHONY: package
package:
	rm -rf build
	mkdir -p build
	cp main.py build
	pyxel package build build/main.py

.PHONY: clean
clean:
	-rm build.pyxapp shoot.pyxapp build.html
	-rm -rf build
