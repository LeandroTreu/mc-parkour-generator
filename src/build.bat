cls
ECHO OFF
pyinstaller --noconfirm -i mpg_icon_256.png MPG.py
copy /v /y mpg_icon_256.png dist\MPG\
copy /v /y ..\README.md dist\MPG\
copy /v /y ..\SETTINGS.md dist\MPG\
copy /v /y ..\LICENSE dist\MPG\