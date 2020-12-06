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

from noteeds.gui.settings import ReposTreeWidget
from noteeds.gui.settings import KeySequenceEdit


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

        self.clearHotkeyButton = QPushButton(self.groupBox_2)
        self.clearHotkeyButton.setObjectName(u"clearHotkeyButton")

        self.gridLayout_2.addWidget(self.clearHotkeyButton, 1, 2, 1, 1)

        self.hotkeyInput = KeySequenceEdit(self.groupBox_2)
        self.hotkeyInput.setObjectName(u"hotkeyInput")

        self.gridLayout_2.addWidget(self.hotkeyInput, 1, 1, 1, 1)

        self.systrayCheckbox = QCheckBox(self.groupBox_2)
        self.systrayCheckbox.setObjectName(u"systrayCheckbox")

        self.gridLayout_2.addWidget(self.systrayCheckbox, 0, 0, 1, 3)

        self.label = QLabel(self.groupBox_2)
        self.label.setObjectName(u"label")

        self.gridLayout_2.addWidget(self.label, 2, 0, 1, 1)

        self.externalEditorInput = QLineEdit(self.groupBox_2)
        self.externalEditorInput.setObjectName(u"externalEditorInput")

        self.gridLayout_2.addWidget(self.externalEditorInput, 2, 1, 1, 2)

        self.hotkeyInput.raise_()
        self.hotkeyCheckbox.raise_()
        self.systrayCheckbox.raise_()
        self.clearHotkeyButton.raise_()
        self.label.raise_()
        self.externalEditorInput.raise_()

        self.verticalLayout.addWidget(self.groupBox_2)

        self.groupBox = QGroupBox(SettingsDialog)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout = QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(u"gridLayout")
        self.reposTree = ReposTreeWidget(self.groupBox)
        self.reposTree.setObjectName(u"reposTree")
        self.reposTree.setDragEnabled(True)
        self.reposTree.setDragDropMode(QAbstractItemView.InternalMove)
        self.reposTree.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.reposTree.setRootIsDecorated(False)
        self.reposTree.setColumnCount(3)

        self.gridLayout.addWidget(self.reposTree, 0, 0, 2, 1)


        self.verticalLayout.addWidget(self.groupBox)

        self.buttonBox = QDialogButtonBox(SettingsDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)

#if QT_CONFIG(shortcut)
        self.label.setBuddy(self.externalEditorInput)
#endif // QT_CONFIG(shortcut)
        QWidget.setTabOrder(self.systrayCheckbox, self.hotkeyCheckbox)
        QWidget.setTabOrder(self.hotkeyCheckbox, self.hotkeyInput)
        QWidget.setTabOrder(self.hotkeyInput, self.clearHotkeyButton)
        QWidget.setTabOrder(self.clearHotkeyButton, self.externalEditorInput)
        QWidget.setTabOrder(self.externalEditorInput, self.reposTree)

        self.retranslateUi(SettingsDialog)
        self.buttonBox.accepted.connect(SettingsDialog.accept)
        self.buttonBox.rejected.connect(SettingsDialog.reject)

        QMetaObject.connectSlotsByName(SettingsDialog)
    # setupUi

    def retranslateUi(self, SettingsDialog):
        SettingsDialog.setWindowTitle(QCoreApplication.translate("SettingsDialog", u"Settings", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("SettingsDialog", u"GUI", None))
#if QT_CONFIG(tooltip)
        self.hotkeyCheckbox.setToolTip(QCoreApplication.translate("SettingsDialog", u"Global hotkey to minimize to and restore from system tray", None))
#endif // QT_CONFIG(tooltip)
        self.hotkeyCheckbox.setText(QCoreApplication.translate("SettingsDialog", u"Global &hotkey:", None))
        self.clearHotkeyButton.setText(QCoreApplication.translate("SettingsDialog", u"&Clear", None))
#if QT_CONFIG(tooltip)
        self.systrayCheckbox.setToolTip(QCoreApplication.translate("SettingsDialog", u"Minimize to system tray when closed, instead of exiting the application", None))
#endif // QT_CONFIG(tooltip)
        self.systrayCheckbox.setText(QCoreApplication.translate("SettingsDialog", u"Close to &system tray", None))
        self.label.setText(QCoreApplication.translate("SettingsDialog", u"External &editor:", None))
#if QT_CONFIG(tooltip)
        self.externalEditorInput.setToolTip(QCoreApplication.translate("SettingsDialog", u"<html><head/><body><p>If the command isn't an absolute path, the PATH environment variable will be used.</p><p>Optionally, you can use {file} and/or {search_term}. If you don't use {file}, the file name will be appended.</p><p>Examples:</p><ul style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;\"><li style=\" margin-top:12px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">notepad</li><li style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">notepad.exe</li><li style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">c:\\windows\\system32\\notepad.exe</li><li style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">notepad {file}</li><li style=\" margin-top:0px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0"
                        "; text-indent:0px;\">gvim +/{search_term}</li></ul></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox.setTitle(QCoreApplication.translate("SettingsDialog", u"&Repositories", None))
        ___qtreewidgetitem = self.reposTree.headerItem()
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("SettingsDialog", u"Path", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("SettingsDialog", u"Color", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("SettingsDialog", u"Name", None));
    # retranslateUi

