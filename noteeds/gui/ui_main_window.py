# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 5.15.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(810, 622)
        MainWindow.setAcceptDrops(True)
        self.exitAction = QAction(MainWindow)
        self.exitAction.setObjectName(u"exitAction")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.rootLabel = QLabel(self.centralwidget)
        self.rootLabel.setObjectName(u"rootLabel")

        self.gridLayout.addWidget(self.rootLabel, 0, 0, 1, 1)

        self.widget_2 = QWidget(self.centralwidget)
        self.widget_2.setObjectName(u"widget_2")
        self.horizontalLayout = QHBoxLayout(self.widget_2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.widget_2)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.textInput = QLineEdit(self.widget_2)
        self.textInput.setObjectName(u"textInput")

        self.horizontalLayout.addWidget(self.textInput)


        self.gridLayout.addWidget(self.widget_2, 1, 0, 1, 1)

        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.resultsTree = QTreeView(self.splitter)
        self.resultsTree.setObjectName(u"resultsTree")
        self.resultsTree.setUniformRowHeights(True)
        self.splitter.addWidget(self.resultsTree)
        self.resultsTree.header().setVisible(False)
        self.textView = QPlainTextEdit(self.splitter)
        self.textView.setObjectName(u"textView")
        self.textView.setTabChangesFocus(True)
        self.textView.setReadOnly(True)
        self.splitter.addWidget(self.textView)

        self.gridLayout.addWidget(self.splitter, 2, 0, 1, 1)

        self.gridLayout.setRowStretch(2, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 810, 26))
        self.fileMenu = QMenu(self.menubar)
        self.fileMenu.setObjectName(u"fileMenu")
        self.viewMenu = QMenu(self.menubar)
        self.viewMenu.setObjectName(u"viewMenu")
        MainWindow.setMenuBar(self.menubar)
        self.dock = QDockWidget(MainWindow)
        self.dock.setObjectName(u"dock")
        self.dockWidgetContents = QWidget()
        self.dockWidgetContents.setObjectName(u"dockWidgetContents")
        self.verticalLayout = QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.logTable = QTreeView(self.dockWidgetContents)
        self.logTable.setObjectName(u"logTable")
        self.logTable.setRootIsDecorated(False)
        self.logTable.setUniformRowHeights(True)

        self.verticalLayout.addWidget(self.logTable)

        self.dock.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(Qt.BottomDockWidgetArea, self.dock)
#if QT_CONFIG(shortcut)
        self.label.setBuddy(self.textInput)
#endif // QT_CONFIG(shortcut)
        QWidget.setTabOrder(self.resultsTree, self.textView)

        self.menubar.addAction(self.fileMenu.menuAction())
        self.menubar.addAction(self.viewMenu.menuAction())
        self.fileMenu.addAction(self.exitAction)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Noteeds", None))
        self.exitAction.setText(QCoreApplication.translate("MainWindow", u"E&xit", None))
#if QT_CONFIG(shortcut)
        self.exitAction.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Q", None))
#endif // QT_CONFIG(shortcut)
        self.rootLabel.setText(QCoreApplication.translate("MainWindow", u"Root:", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"&Search:", None))
        self.fileMenu.setTitle(QCoreApplication.translate("MainWindow", u"&File", None))
        self.viewMenu.setTitle(QCoreApplication.translate("MainWindow", u"&View", None))
        self.dock.setWindowTitle(QCoreApplication.translate("MainWindow", u"Log", None))
    # retranslateUi

