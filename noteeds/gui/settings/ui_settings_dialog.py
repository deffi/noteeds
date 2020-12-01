# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settings_dialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from noteeds.gui.widgets import TreeWidget


class Ui_SettingsDialog(object):
    def setupUi(self, SettingsDialog):
        if not SettingsDialog.objectName():
            SettingsDialog.setObjectName(u"SettingsDialog")
        SettingsDialog.resize(570, 388)
        SettingsDialog.setToolTipDuration(-19)
        self.verticalLayout = QVBoxLayout(SettingsDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox_2 = QGroupBox(SettingsDialog)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.gridLayout_2 = QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.hotkeyCheckbox = QCheckBox(self.groupBox_2)
        self.hotkeyCheckbox.setObjectName(u"hotkeyCheckbox")

        self.gridLayout_2.addWidget(self.hotkeyCheckbox, 1, 0, 1, 1)

        self.hotkeyInput = QKeySequenceEdit(self.groupBox_2)
        self.hotkeyInput.setObjectName(u"hotkeyInput")

        self.gridLayout_2.addWidget(self.hotkeyInput, 1, 1, 1, 1)

        self.clearHotkeyButton = QPushButton(self.groupBox_2)
        self.clearHotkeyButton.setObjectName(u"clearHotkeyButton")

        self.gridLayout_2.addWidget(self.clearHotkeyButton, 1, 2, 1, 1)

        self.systrayCheckbox = QCheckBox(self.groupBox_2)
        self.systrayCheckbox.setObjectName(u"systrayCheckbox")

        self.gridLayout_2.addWidget(self.systrayCheckbox, 0, 0, 1, 3)

        self.hotkeyInput.raise_()
        self.hotkeyCheckbox.raise_()
        self.systrayCheckbox.raise_()
        self.clearHotkeyButton.raise_()

        self.verticalLayout.addWidget(self.groupBox_2)

        self.groupBox = QGroupBox(SettingsDialog)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout = QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(u"gridLayout")
        self.addReposButton = QPushButton(self.groupBox)
        self.addReposButton.setObjectName(u"addReposButton")

        self.gridLayout.addWidget(self.addReposButton, 0, 1, 1, 1)

        self.removeReposButton = QPushButton(self.groupBox)
        self.removeReposButton.setObjectName(u"removeReposButton")

        self.gridLayout.addWidget(self.removeReposButton, 1, 1, 1, 1)

        self.reposTree = TreeWidget(self.groupBox)
        self.reposTree.setObjectName(u"reposTree")
        self.reposTree.setDragEnabled(True)
        self.reposTree.setDragDropMode(QAbstractItemView.InternalMove)
        self.reposTree.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.reposTree.setRootIsDecorated(False)
        self.reposTree.setColumnCount(3)

        self.gridLayout.addWidget(self.reposTree, 0, 0, 3, 1)

        self.verticalSpacer = QSpacerItem(20, 119, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 2, 1, 1, 1)


        self.verticalLayout.addWidget(self.groupBox)

        self.buttonBox = QDialogButtonBox(SettingsDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)

        QWidget.setTabOrder(self.systrayCheckbox, self.hotkeyCheckbox)
        QWidget.setTabOrder(self.hotkeyCheckbox, self.hotkeyInput)
        QWidget.setTabOrder(self.hotkeyInput, self.clearHotkeyButton)
        QWidget.setTabOrder(self.clearHotkeyButton, self.reposTree)
        QWidget.setTabOrder(self.reposTree, self.addReposButton)
        QWidget.setTabOrder(self.addReposButton, self.removeReposButton)

        self.retranslateUi(SettingsDialog)
        self.buttonBox.accepted.connect(SettingsDialog.accept)
        self.buttonBox.rejected.connect(SettingsDialog.reject)

        QMetaObject.connectSlotsByName(SettingsDialog)
    # setupUi

    def retranslateUi(self, SettingsDialog):
        SettingsDialog.setWindowTitle(QCoreApplication.translate("SettingsDialog", u"Settings", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("SettingsDialog", u"GUI", None))
        self.hotkeyCheckbox.setText(QCoreApplication.translate("SettingsDialog", u"Global &hotkey:", None))
        self.clearHotkeyButton.setText(QCoreApplication.translate("SettingsDialog", u"&Clear", None))
        self.systrayCheckbox.setText(QCoreApplication.translate("SettingsDialog", u"Minimize to &system tray", None))
        self.groupBox.setTitle(QCoreApplication.translate("SettingsDialog", u"&Repositories", None))
        self.addReposButton.setText(QCoreApplication.translate("SettingsDialog", u"&Add", None))
        self.removeReposButton.setText(QCoreApplication.translate("SettingsDialog", u"Re&move", None))
        ___qtreewidgetitem = self.reposTree.headerItem()
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("SettingsDialog", u"Path", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("SettingsDialog", u"Color", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("SettingsDialog", u"Name", None));
    # retranslateUi

