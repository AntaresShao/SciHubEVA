# Building

## macOS

1. Create a python environment.

   ```bash
   conda create -n python37 python=3.7
   conda activate python37
   ```

2. Install requirements.

   ```bash
   pip install -r requirements.txt
   ```

3. Update the translations. Install Qt first and make sure you can run `lupdate` and `lrelease` commands.

   ```bash
   # Generate translations source of QML files
   lupdate SciHubEVA.pro

   # Generate translations source of Python files
   pyside2-lupdate scihubeva/*.py -ts translations/SciHubEVA_zh_CN.ts

   # Do translations with Qt Linguist
   # ......

   # Traditional Chinese translation was done by opencc
   opencc -c s2twp -i translations/SciHubEVA_zh_CN.ts -o translations/SciHubEVA_zh_TW.ts
   opencc -c s2hk -i translations/SciHubEVA_zh_CN.ts -o translations/SciHubEVA_zh_HK.ts

   # Generate translations target
   lrelease translations/SciHubEVA_zh_CN.ts
   lrelease translations/SciHubEVA_zh_TW.ts
   lrelease translations/SciHubEVA_zh_HK.ts
   ```

   Complied translations will be in `translations` end with `.qm`.

4. Build with `PyInstaller`.

   ```bash
   # Install the latest develop version of PyInstaller

   # You may need rebuild the bootloader of PyInstaller against 10.14 SDK to fully support dark theme
   # See: https://pyinstaller.readthedocs.io/en/latest/bootloader-building.html

   rm -rf build
   rm -rf dist
   rm -f SciHubEVA.spec

   pyside2-rcc SciHubEVA.qrc -o scihubeva/resources.py

   pyinstaller -w app.py \
      --hidden-import "socks" \
      --hidden-import "PIL" \
      --add-data "LICENSE:." \
      --add-data "conf/SciHubEVA.conf:conf" \
      --add-data "conf/qtquickcontrols2.conf:conf" \
      --add-data "images/SciHubEVA-icon.png:images" \
      --add-data "translations/*.qm:translations" \
      --name "SciHubEVA" \
      --icon "images/SciHubEVA.icns" \
      --noupx

   cp building/macOS/Info.plist dist/SciHubEVA.app/Contents

   # Remove useless libraries
   cd dist/SciHubEVA.app/Contents/MacOS
   rm -f Qt3D* QtBluetooth QtBodymovin QtCharts QtDataVisualization QtGamepad QtLocation QtMultimedia QtMultimediaQuick QtNfc QtPositioning QtPositioningQuick QtPurchasing QtQuick3D* QtQuickTest QtRemoteObjects QtScxml QtSensors QtSql QtTest QtVirtualKeyboard QtWeb*
   rm -f libopenblas*
   cd PySide2/qml
   rm -rf Qt3D* QtAudioEngine QtBluetooth QtCharts QtDataVisualization QtGamepad QtLocation QtMultimedia QtNfc QtPositioning QtPurchasing QtQuick3D* QtRemoteObjects QtScxml QtSensors QtTest QtWeb*
   cd ../../../Resources
   rm -rf PyInstaller
   cd ../../../..
   ```

   `SciHubEVA.app` will be in `dist`.

5. Package with `appdmg`. Install [Node.js](https://nodejs.org) first, then run the following commands:

   ```bash
   npm install -g appdmg

   appdmg building/macOS/SciHubEVA.dmg.json dist/SciHubEVA.dmg
   ```

   `SciHubEVA.dmg` will be in `dist `.

## Windows

1. See setcion 1 in [macOS](#macOS).
2. See setcion 2 in [macOS](#macOS).
3. See setcion 3 in [macOS](#macOS).
4. Build with `PyInstaller`.

   ```powershell
   :: Install the latest develop version of PyInstaller

   rd /s /Q build
   rd /s /Q dist
   del /F /S /Q SciHubEVA.spec

   pyside2-rcc SciHubEVA.qrc -o scihubeva/resources.py

   pyinstaller -w app.py ^
      --hidden-import "socks" ^
      --hidden-import "PIL" ^
      --add-data "LICENSE;." ^
      --add-data "conf/SciHubEVA.conf;conf" ^
      --add-data "conf/qtquickcontrols2.conf;conf" ^
      --add-data "images/SciHubEVA-icon.png;images" ^
      --add-data "translations/*.qm;translations" ^
      --name "SciHubEVA" ^
      --icon "images/SciHubEVA.ico" ^
      --version-file "building/Windows/SciHubEVA.win.version" ^
      --noupx

   :: Remove useless libraries
   cd dist/SciHubEVA
   del /F /S /Q Qt53D* Qt5Bluetooth.dll Qt5Bodymovin.dll Qt5Charts.dll Qt5DataVisualization.dll Qt5Gamepad.dll Qt5Location.dll Qt5Multimedia.dll Qt5MultimediaQuick.dll Qt5Nfc.dll Qt5Positioning.dll Qt5PositioningQuick.dll Qt5Purchasing.dll Qt5Quick3D*.dll Qt5QuickTest.dll Qt5RemoteObjects.dll Qt5Scxml.dll Qt5Sensors.dll Qt5Sql.dll Qt5Test.dll Qt5VirtualKeyboard.dll Qt5Web*
   cd PySide2/qml
   del /F /S /Q Qt3D QtAudioEngine QtBluetooth QtCharts QtDataVisualization QtGamepad QtLocation QtMultimedia QtNfc QtPositioning QtPurchasing QtQuick3D QtRemoteObjects QtScxml QtSensors QtTest QtWebChannel QtWebEngine QtWebSockets QtWebView QtWinExtras
   cd ../../../..
   ```

   All compiled files will be in `dist\SciHubEVA`.


5. Package with Inno Setup. Install [Inno Setup 6](http://www.jrsoftware.org/isinfo.php) first and add installation directory to PATH. Download Chinese (Simplified) and Chinese (Traditional) translations from [here](http://www.jrsoftware.org/files/istrans/), and copy them to `INNO_SETUP_ROOT\Languages`.

   ```powershell
   ISCC.exe building/Windows/SciHubEVA.iss
   ```

   `SciHubEVA.exe` installer will be in the `dist`.

6. If you need a x86 version, please make sure you have a x86 version python environment, and modify the `SciHubEVA.iss` accordingly.

   ```text
   DefaultDirName={autopf64}\{#MyAppName} -> DefaultDirName={autopf32}\{#MyAppName}
   OutputBaseFilename=SciHubEVA-x64 -> OutputBaseFilename=SciHubEVA-x86
   ```
