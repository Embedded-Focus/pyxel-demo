app2html: package
	pyxel app2html bin.pyxapp
	sed 's/\(gamepad:\s*"\)enabled"/\1disabled"/' <bin.html >shoot.html

.PHONY: run
run:
	pyxel run bin/demo.py

.PHONY: package
package:
	pyxel package bin bin/demo.py

.PHONY: clean
clean:
	-rm build.pyxapp shoot.pyxapp build.html
	-rm -rf build
