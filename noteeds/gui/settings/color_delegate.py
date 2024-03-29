import logging

import PySide6
from PySide6.QtCore import QModelIndex, Qt, QAbstractItemModel
from PySide6.QtGui import QColor
from PySide6.QtGui import QPixmap, QIcon, QPainter
from PySide6.QtWidgets import QStyledItemDelegate, QWidget, QStyleOptionViewItem, QStyle

from noteeds.gui.settings import ColorEditWidget
from noteeds.util.geometry import adjust_size

logger = logging.getLogger(__name__)


class ColorDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)

    #########
    # Paint #
    #########

    def initStyleOption(self, option: QStyleOptionViewItem, index: QModelIndex):
        super().initStyleOption(option, index)

        if index.siblingAtRow(index.row() + 1).isValid():
            # If we have a color, show it as decoration. Otherwise, show a cross.
            pixmap = QPixmap(option.decorationSize)
            color = index.data(Qt.DecorationRole)
            if color:
                pixmap.fill(color)
            else:
                pixmap.fill(Qt.transparent)
                painter = QPainter(pixmap)
                painter.drawLine(0, 0, pixmap.width()-1, pixmap.height()-1)
                painter.drawLine(0, pixmap.height()-1, pixmap.width()-1, 0)
                painter.end()
            option.icon = QIcon(pixmap)

            # Always show the decoration
            option.features |= QStyleOptionViewItem.HasDecoration

        else:
            option.features &= ~QStyleOptionViewItem.HasDecoration

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex):
        # Draw the item regularly first, and then redraw it as if it was not
        # selected. That way, we get the selection highlight, but it does
        # not affect the color of the decoration.
        super().paint(painter, option, index)
        option.state = option.state & ~QStyle.State_Selected
        super().paint(painter, option, index)

    ########
    # Edit #
    ########

    def createEditor(self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex) -> QWidget:
        color = index.data(Qt.DecorationRole)
        if not color or isinstance(color, QColor):
            editor = ColorEditWidget(parent)
            editor.color_picked.connect(self.color_picked)
            return editor
        else:
            logger.warning("ColorDelegate invoked on non-color")
            return super().createEditor(parent, option, index)

    def updateEditorGeometry(self, editor: QWidget, option: QStyleOptionViewItem, index: QModelIndex):
        geometry = option.rect

        # If the rectangle is to small for the minimum size of the editor,
        # enlarge it
        dw = editor.minimumSizeHint().width() - geometry.width()
        if dw > 0:
            adjust_size(geometry, dw, 0, editor.layoutDirection())

        editor.setGeometry(geometry)

    def setEditorData(self, editor: QWidget, index: PySide6.QtCore.QModelIndex):
        editor: ColorEditWidget
        color = index.data(Qt.DecorationRole)
        editor.set_color(color)

    def setModelData(self, editor: QWidget, model: QAbstractItemModel, index: QModelIndex):
        editor: ColorEditWidget
        model.setData(index, editor.get_color(), Qt.DecorationRole)

    def color_picked(self):
        self.commitData.emit(self.sender())
        self.closeEditor.emit(self.sender())
