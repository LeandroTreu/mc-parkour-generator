#!/bin/sh
pyinstaller --noconfirm MPG.py
cp mpg_icon_256.png dist/MPG/
cp ../README.md dist/MPG/
cp ../SETTINGS.md dist/MPG/
cp ../LICENSE dist/MPG/