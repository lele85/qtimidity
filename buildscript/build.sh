#!/bin/bash
pyuic4 -d ../ui/qtimidity.ui -o ../qtimidityUi.py -x
pyuic4 ../ui/configWizard.ui -o ../configWizardUi.py -x
pyrcc4 ../icons/icons.qrc -o ../icons_rc.py

