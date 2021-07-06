import napari
import numpy
import skimage


def main():
    source = skimage.data.binary_blobs(seed=42)
    viewer = napari.view_image(source, name="source")

    labels_layer = viewer.add_labels(numpy.zeros_like(source, dtype=int), name="labels")
    labels_layer.brush_size = 5
    for y in range(100, 200):
        labels_layer.paint((400, y), new_label=1, refresh=False)
    for y in range(200, 300):
        labels_layer.paint((100, y), new_label=2, refresh=False)
    labels_layer.refresh()

    viewer.window.add_plugin_dock_widget("napari-ilastik")
    napari.run()


if __name__ == "__main__":
    main()
