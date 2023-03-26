# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'color_widget.ui'
##
## Created by: Qt User Interface Compiler version 6.4.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QPushButton, QSizePolicy,
    QWidget)

class Ui_ColorWidget(object):
    def setupUi(self, ColorWidget):
        if not ColorWidget.objectName():
            ColorWidget.setObjectName(u"ColorWidget")
        ColorWidget.resize(186, 107)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ColorWidget.sizePolicy().hasHeightForWidth())
        ColorWidget.setSizePolicy(sizePolicy)
        ColorWidget.setAutoFillBackground(True)
        self.horizontalLayout = QHBoxLayout(ColorWidget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.colorButton = QPushButton(ColorWidget)
        self.colorButton.setObjectName(u"colorButton")
        self.colorButton.setAutoFillBackground(True)
        self.colorButton.setFlat(True)

        self.horizontalLayout.addWidget(self.colorButton)

        self.clearButton = QPushButton(ColorWidget)
        self.clearButton.setObjectName(u"clearButton")

        self.horizontalLayout.addWidget(self.clearButton)


        self.retranslateUi(ColorWidget)

        QMetaObject.connectSlotsByName(ColorWidget)
    # setupUi

    def retranslateUi(self, ColorWidget):
        ColorWidget.setWindowTitle(QCoreApplication.translate("ColorWidget", u"Form", None))
        self.colorButton.setText("")
        self.clearButton.setText(QCoreApplication.translate("ColorWidget", u"X", None))
    # retranslateUi

