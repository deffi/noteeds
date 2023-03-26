# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'path_browse_widget.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLineEdit, QPushButton,
    QSizePolicy, QWidget)

class Ui_PathBrowseWidget(object):
    def setupUi(self, PathBrowseWidget):
        if not PathBrowseWidget.objectName():
            PathBrowseWidget.setObjectName(u"PathBrowseWidget")
        PathBrowseWidget.resize(186, 107)
        PathBrowseWidget.setAutoFillBackground(True)
        self.horizontalLayout = QHBoxLayout(PathBrowseWidget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.pathInput = QLineEdit(PathBrowseWidget)
        self.pathInput.setObjectName(u"pathInput")

        self.horizontalLayout.addWidget(self.pathInput)

        self.browseButton = QPushButton(PathBrowseWidget)
        self.browseButton.setObjectName(u"browseButton")

        self.horizontalLayout.addWidget(self.browseButton)

        self.horizontalLayout.setStretch(0, 1)

        self.retranslateUi(PathBrowseWidget)

        QMetaObject.connectSlotsByName(PathBrowseWidget)
    # setupUi

    def retranslateUi(self, PathBrowseWidget):
        PathBrowseWidget.setWindowTitle(QCoreApplication.translate("PathBrowseWidget", u"Form", None))
        self.browseButton.setText(QCoreApplication.translate("PathBrowseWidget", u"...", None))
    # retranslateUi

