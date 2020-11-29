# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'color_edit_widget.ui'
##
## Created by: Qt User Interface Compiler version 5.15.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_ColorEditWidget(object):
    def setupUi(self, ColorEditWidget):
        if not ColorEditWidget.objectName():
            ColorEditWidget.setObjectName(u"ColorEditWidget")
        ColorEditWidget.resize(186, 107)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ColorEditWidget.sizePolicy().hasHeightForWidth())
        ColorEditWidget.setSizePolicy(sizePolicy)
        ColorEditWidget.setAutoFillBackground(True)
        self.horizontalLayout = QHBoxLayout(ColorEditWidget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.colorButton = QPushButton(ColorEditWidget)
        self.colorButton.setObjectName(u"colorButton")
        self.colorButton.setAutoFillBackground(True)
        self.colorButton.setFlat(True)

        self.horizontalLayout.addWidget(self.colorButton)

        self.clearButton = QPushButton(ColorEditWidget)
        self.clearButton.setObjectName(u"clearButton")

        self.horizontalLayout.addWidget(self.clearButton)


        self.retranslateUi(ColorEditWidget)

        QMetaObject.connectSlotsByName(ColorEditWidget)
    # setupUi

    def retranslateUi(self, ColorEditWidget):
        ColorEditWidget.setWindowTitle(QCoreApplication.translate("ColorEditWidget", u"Form", None))
        self.colorButton.setText("")
        self.clearButton.setText(QCoreApplication.translate("ColorEditWidget", u"X", None))
    # retranslateUi

