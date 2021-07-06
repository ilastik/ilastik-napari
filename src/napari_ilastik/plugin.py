from typing import Any

import numpy
import sparse
from napari import Viewer
from napari._qt.containers import QtLayerList
from napari.layers import Image, Labels, Layer
from napari.qt.threading import thread_worker
from napari_plugin_engine import napari_hook_implementation
from qtpy.QtCore import QModelIndex, QSortFilterProxyModel, Qt
from qtpy.QtWidgets import QComboBox, QFormLayout, QProgressBar, QPushButton, QWidget
from sklearn.ensemble import RandomForestClassifier

from napari_ilastik import filters
from napari_ilastik.classifier import NDSparseClassifier
from napari_ilastik.filters import FilterSet
from napari_ilastik.gui import CheckboxTableDialog, rc_pairs


@thread_worker
def _pixel_classification(image, labels, features):
    feature_map = features.transform(numpy.asarray(image.data))
    sparse_labels = sparse.COO.from_numpy(numpy.asarray(labels.data))
    clf = NDSparseClassifier(RandomForestClassifier())
    clf.fit(feature_map, sparse_labels)
    return clf.predict(feature_map)


filter_names = {
    filters.Gaussian: "Gaussian Smoothing",
    filters.LaplacianOfGaussian: "Laplacian of Gaussian",
    filters.GaussianGradientMagnitude: "Gaussian Gradient Magnitude",
    filters.DifferenceOfGaussians: "Difference of Gaussians",
    filters.StructureTensorEigenvalues: "Structure Tensor Eigenvalues",
    filters.HessianOfGaussianEigenvalues: "Hessian of Gaussian Eigenvalues",
}
filter_list = (
    filters.Gaussian,
    filters.LaplacianOfGaussian,
    filters.GaussianGradientMagnitude,
    filters.DifferenceOfGaussians,
    filters.StructureTensorEigenvalues,
    filters.HessianOfGaussianEigenvalues,
)
scale_list = (0.3, 0.7, 1.0, 1.6, 3.5, 5.0, 10.0)


class LayerModel(QSortFilterProxyModel):
    def __init__(self, layers: QtLayerList, parent=None):
        super().__init__(parent)
        self.setSourceModel(layers)

    def filterAcceptsRow(self, row: int, parent: QModelIndex) -> bool:
        model = self.sourceModel()
        index = model.index(row, self.filterKeyColumn(), parent)
        layer = model.data(index, Qt.UserRole)
        return self.should_accept_layer(layer)

    def should_accept_layer(self, layer: Layer) -> bool:
        return True

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole) -> Any:
        if role in (Qt.DisplayRole, Qt.DecorationRole, Qt.UserRole):
            return super().data(index, role)
        return None


class ImageLayerModel(LayerModel):
    def should_accept_layer(self, layer: Layer) -> bool:
        return isinstance(layer, Image) and not isinstance(layer, Labels)


class LabelsLayerModel(LayerModel):
    def should_accept_layer(self, layer: Layer) -> bool:
        return isinstance(layer, Labels)


class PixelClassificationWidget(QWidget):
    OUTPUT_LAYER_PARAMS = dict(name="ilastik segmentation", opacity=0.75)

    def __init__(self, napari_viewer: Viewer, parent=None):
        super().__init__(parent)

        layer_model = napari_viewer.window.qt_viewer.layers.model()

        image_combo = QComboBox()
        image_combo.setModel(ImageLayerModel(layer_model, self))
        image_combo.currentIndexChanged.connect(lambda _index: self._update_widgets())

        labels_combo = QComboBox()
        labels_combo.setModel(LabelsLayerModel(layer_model, self))
        labels_combo.currentIndexChanged.connect(lambda _index: self._update_widgets())

        features_state = dict.fromkeys(
            rc_pairs(len(filter_list), len(scale_list)), True
        )
        for s in range(1, len(filter_list)):
            del features_state[s, 0]
        features_dialog = CheckboxTableDialog(
            self,
            rows=list(map(filter_names.__getitem__, filter_list)),
            cols=list(map(str, scale_list)),
            state=features_state,
        )
        features_dialog.setWindowTitle("Select Features")

        # FIXME: Find a reliable way to fit dialog's size to it's contents.
        features_dialog.setMinimumSize(500, 200)

        features_button = QPushButton("&Features")
        features_button.clicked.connect(features_dialog.open)

        run_button = QPushButton("&Run")
        run_button.setEnabled(False)
        run_button.clicked.connect(self._on_run_clicked)

        progress_bar = QProgressBar()
        progress_bar.setVisible(False)
        progress_bar.setMinimum(0)
        progress_bar.setMaximum(0)

        layout = QFormLayout()
        layout.addRow("&Image:", image_combo)
        layout.addRow("&Labels:", labels_combo)
        layout.addRow(features_button)
        layout.addRow(run_button)
        layout.addRow(progress_bar)
        self.setLayout(layout)

        self._viewer = napari_viewer
        self._image_combo = image_combo
        self._labels_combo = labels_combo
        self._features_dialog = features_dialog
        self._run_button = run_button
        self._progress_bar = progress_bar
        self._labels_seed = None
        self._update_widgets()

    def _update_widgets(self):
        combos = self._image_combo, self._labels_combo
        self._run_button.setEnabled(all(c.currentData() for c in combos))

    def _on_run_clicked(self):
        self._set_enabled(False)

        image_layer: Image = self._image_combo.currentData()
        labels_layer: Labels = self._labels_combo.currentData()

        features = FilterSet(
            filters=tuple(
                filter_list[row](scale_list[col])
                for row, col in sorted(self._features_dialog.selected)
            )
        )

        self._labels_seed = labels_layer.seed

        worker = _pixel_classification(image_layer.data, labels_layer.data, features)
        worker.finished.connect(lambda: self._set_enabled(True))
        worker.returned.connect(self._update_output_layer)
        worker.start()

    def _set_enabled(self, value):
        self._run_button.setEnabled(value)
        self._progress_bar.setVisible(not value)

    def _update_output_layer(self, data):
        try:
            layer = self._viewer.layers[self.OUTPUT_LAYER_PARAMS["name"]]
            layer.data = data
            layer.seed = self._labels_seed
        except KeyError:
            layer = self._viewer.add_labels(
                data, seed=self._labels_seed, **self.OUTPUT_LAYER_PARAMS
            )
            layer.color_mode = "AUTO"
            layer.editable = False
        finally:
            self._labels_seed = None


@napari_hook_implementation
def napari_experimental_provide_dock_widget():
    return PixelClassificationWidget, {"name": "ilastik Pixel Classification"}
