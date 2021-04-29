import collections.abc
from typing import Iterable, Mapping, Sequence, Set, Tuple

from qtpy.QtCore import Qt
from qtpy.QtGui import QStandardItem, QStandardItemModel
from qtpy.QtWidgets import QDialog, QDialogButtonBox, QTableView, QVBoxLayout


def rc_pairs(nrows: int, ncolumns: int) -> Iterable[Tuple[int, int]]:
    """Yield pairs of (row, column) indices."""
    yield from ((r, c) for r in range(nrows) for c in range(ncolumns))


class ModelDict(collections.abc.MutableMapping):
    source: QStandardItemModel

    def __init__(self, rows: Iterable[str], columns: Iterable[str], parent=None):
        self.source = QStandardItemModel(parent)
        self.source.setVerticalHeaderLabels(rows)
        self.source.setHorizontalHeaderLabels(columns)
        for k in rc_pairs(self.source.rowCount(), self.source.columnCount()):
            item = QStandardItem()
            item.setFlags(Qt.NoItemFlags)
            self.source.setItem(*k, item)

    def __getitem__(self, key: Tuple[int, int]) -> bool:
        item = self.source.item(*key)
        if item.isEnabled():
            return item.checkState() == Qt.Checked
        raise KeyError(key)

    def __setitem__(self, key: Tuple[int, int], value: bool) -> None:
        item = self.source.item(*key)
        item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsUserCheckable)
        item.setCheckState(Qt.Checked if value else Qt.Unchecked)

    def __delitem__(self, key: Tuple[int, int]) -> None:
        self.source.item(*key).setFlags(Qt.NoItemFlags)

    def __iter__(self, *, row=None, column=None) -> Iterable[Tuple[int, int]]:
        rows = range(self.source.rowCount()) if row is None else (row,)
        columns = range(self.source.columnCount()) if column is None else (column,)
        yield from (
            (r, c) for r in rows for c in columns if self.source.item(r, c).isEnabled()
        )

    def __len__(self) -> int:
        return sum(1 for _k in self)


class CheckboxTableDialog(QDialog):
    selected: Set[Tuple[int, int]]

    def __init__(
        self,
        parent=None,
        *,
        rows: Sequence[str],
        cols: Sequence[str],
        state: Mapping[Tuple[int, int], bool],
    ):
        if not (rows and cols and state):
            raise ValueError("rows, cols, and state should be non-empty")

        super().__init__(parent)

        model = ModelDict(rows, cols, parent)
        model.update(state)

        table = QTableView()
        table.setModel(model.source)
        table.resizeRowsToContents()
        table.resizeColumnsToContents()
        table.clicked.connect(lambda _index: self._update_widgets())

        vheader = table.verticalHeader()
        vheader.setSectionsClickable(True)
        vheader.sectionClicked.connect(lambda index: self._handle_header(row=index))

        hheader = table.horizontalHeader()
        hheader.setSectionsClickable(True)
        hheader.sectionClicked.connect(lambda index: self._handle_header(column=index))

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        select_all = buttons.addButton("Select All", QDialogButtonBox.ActionRole)
        select_all.clicked.connect(lambda: self._handle_select(True))

        deselect_all = buttons.addButton("Deselect All", QDialogButtonBox.ActionRole)
        deselect_all.clicked.connect(lambda: self._handle_select(False))

        layout = QVBoxLayout()
        layout.addWidget(table)
        layout.addWidget(buttons)
        self.setLayout(layout)

        self._model = model
        self._ok_button = buttons.button(QDialogButtonBox.Ok)
        self.selected = set(k for k, v in self._model.items() if v)
        self._update_widgets()

    def accept(self):
        self.selected = set(k for k, v in self._model.items() if v)
        super().accept()

    def _update_widgets(self):
        self._ok_button.setEnabled(any(self._model.values()))

    def _handle_header(self, row=None, column=None):
        value = not all(
            self._model[k] for k in self._model.__iter__(row=row, column=column)
        )
        for k in self._model.__iter__(row=row, column=column):
            self._model[k] = value
        self._update_widgets()

    def _handle_select(self, value):
        for k in self._model:
            self._model[k] = value
        self._update_widgets()
