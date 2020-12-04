import logging

import PySide2
from PySide2.QtCore import QModelIndex, Qt, QAbstractItemModel, QTimer
from PySide2.QtWidgets import QStyledItemDelegate, QWidget, QStyleOptionViewItem

from noteeds.gui.settings import PathBrowseWidget
from noteeds.util.geometry import adjust_size

logger = logging.getLogger(__name__)


class PathBrowseDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._path_been_set = False

    ########
    # Edit #
    ########

    def createEditor(self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex) -> QWidget:
        editor = PathBrowseWidget(parent)
        editor.path_selected.connect(self.path_selected)
        self._path_been_set = False
        return editor

    def updateEditorGeometry(self, editor: QWidget, option: QStyleOptionViewItem, index: QModelIndex):
        geometry = option.rect

        # If the rectangle is to small for the minimum size of the editor,
        # enlarge it
        dw = editor.minimumSizeHint().width() - geometry.width()
        if dw > 0:
            adjust_size(geometry, dw, 0, editor.layoutDirection())

        editor.setGeometry(geometry)

    def setEditorData(self, editor: QWidget, index: PySide2.QtCore.QModelIndex):
        editor: PathBrowseWidget
        path = index.data(Qt.EditRole)
        editor.set_path(path)

        if not self._path_been_set:
            self._path_been_set = True
            if not path:
                editor.browse()

    def setModelData(self, editor: QWidget, model: QAbstractItemModel, index: QModelIndex):
        editor: PathBrowseWidget
        model.setData(index, editor.get_path(), Qt.EditRole)

    def path_selected(self):
        self.commitData.emit(self.sender())
        self.closeEditor.emit(self.sender())
