from PySide2.QtCore import QAbstractItemModel, QModelIndex, Qt

from noteeds.engine import SearchResult, FileEntry

class SearchResultModel(QAbstractItemModel):
    def __init__(self, parent):
        super().__init__(parent)

        self._name_prefix          = None
        self._name_anywhere        = None
        self._contents_word        = None
        self._contents_word_prefix = None
        self._contents_anywhere    = None
        self._lists = []
        self._list_descriptions = None

    def set_result(self, result: SearchResult):
        self.beginResetModel()
        self._name_prefix          = list(sorted(result.name_prefix))
        self._name_anywhere        = list(sorted(result.name_anywhere))
        self._contents_word        = list(sorted(result.contents_word))
        self._contents_word_prefix = list(sorted(result.contents_word_prefix))
        self._contents_anywhere    = list(sorted(result.contents_anywhere))
        
        self._lists = [
            self._name_prefix,
            self._name_anywhere,
            self._contents_word,
            self._contents_word_prefix,
            self._contents_anywhere,
            ]
        
        self._list_descriptions = [
            "Name prefix",
            "Name anywhere",
            "Contents word",
            "Contents word prefix",
            "Contents anywhere",                 
            ]

        self.endResetModel()


    ############
    ## Access ##
    ############

    def is_file(self, index):
        return index.isValid() and index.internalPointer() is not None
    
    def file_entry(self, index) -> FileEntry:
        if self.is_file(index):
            return index.internalPointer()[index.row()]
        else:
            return None

    ################################
    ## QAbstractItemModel methods ##
    ################################

    # (root)
    # |- name_prefix     -> _lists
    # |  |- ...            -> the list
    # |  '- ...
    # |- name_anywhere
    # |  '- ...
    # '- ...
    
    def columnCount(self, index = QModelIndex()):
        if not index.isValid():
            # Root item
            return 1
        elif index.internalPointer() is None:
            # A list, internalPointer is None
            the_list = self._lists[index.row()]
            return 1
        elif index.internalPointer() in self._lists:
            # A file, internalPointer is the list
            the_list = index.internalPointer()
            the_file = the_list[index.row()]
            return 1
        else:
            # Unknown
            print("Unknown model index %s with internalPointer %s" % (str(index), str(index.internalPointer())))
            return 0
    
    def rowCount(self, index=QModelIndex()):
        if not index.isValid():
            # Root item
            return len(self._lists)
        elif index.internalPointer() is None:
            # A list, internalPointer is None
            the_list = self._lists[index.row()]
            return len(the_list)
        elif index.internalPointer() in self._lists:
            # A file, internalPointer is the list
            the_list = index.internalPointer()
            the_file = the_list[index.row()]
            return 0
        else:
            # Unknown
            print("Unknown model index %s with internalPointer %s" % (str(index), str(index.internalPointer())))
            return 0
        
    def index(self, row, column, index = QModelIndex()):
        if column != 0:
            print("Column is %s" % column)
            return QModelIndex()

        if not index.isValid():
            # Root item
            return self.createIndex(row, column, None)
        elif index.internalPointer() is None:
            # A list, internalPointer is None
            the_list = self._lists[index.row()]
            return self.createIndex(row, column, the_list)
        elif index.internalPointer() in self._lists:
            # A file, internalPointer is the list
            the_list = index.internalPointer()
            the_file = the_list[index.row()]
            print("index() called for file entry")
            return QModelIndex()
        else:
            # Unknown
            print("Unknown model index %s with internalPointer %s" % (str(index), str(index.internalPointer())))
            return 0

    def parent(self, index):
        if not index.isValid():
            # Root item
            return QModelIndex()
        elif index.internalPointer() is None:
            # A list, internalPointer is None
            the_list = self._lists[index.row()]
            return QModelIndex()
        elif index.internalPointer() in self._lists:
            # A file, internalPointer is the list
            the_list = index.internalPointer()
            the_file = the_list[index.row()]
            return self.createIndex(self._lists.index(the_list), 0, None)
        else:
            # Unknown
            print("Unknown model index %s with internalPointer %s" % (str(index), str(index.internalPointer())))
            return 0

    def data(self, index, role=Qt.DisplayRole):
        # index.internalPointer()
        if role == Qt.DisplayRole:
            if not index.isValid():
                # Root item
                return "root"
            elif index.internalPointer() is None:
                # A list, internalPointer is None
                the_list = self._lists[index.row()]
                return self._list_descriptions[index.row()]
            elif index.internalPointer() in self._lists:
                # A file, internalPointer is the list
                the_list = index.internalPointer()
                the_file = the_list[index.row()]
                return the_file.absolute_path.name
            else:
                # Unknown
                print("Unknown model index %s with internalPointer %s" % (str(index), str(index.internalPointer())))
                return "unknown"

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            if section == 0:
                return "File"
