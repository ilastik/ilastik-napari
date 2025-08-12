# ilastik-napari

[Napari][napari] plugin for interactive pixel classification.
Designed to be similar to the pixel classification workflow in [classic ilastik][ilastik].

## Installation

This plugin requires you to use a _conda_ environment. The environment manager conda comes in a few different forms.
If you haven't used conda before, you can find more information in the [conda user guide][conda-user-guide].
You can use whichever variant you prefer, as the resulting environment should be the same, but we recommend the [_mambaforge_][mambaforge] variant as it is usually the fastest.
When using mambaforge, the `mamba` command usually replaces the `conda` command one would otherwise use.

Once you have installed mambaforge, set up a conda environment with napari and the _fastfilters_ package, and then use pip to install _ilastik-napari_:
```shell
conda create -y -c ilastik-forge -c conda-forge -n my-napari-env napari pyqt=5.15 fastfilters sparse qtpy scikit-learn
conda activate my-napari-env
pip install ilastik-napari
```

Finally, run napari:
```shell
napari
```
That's it! You should be able to find the ilastik-napari plugin in the Plugins menu.

If you prefer to __install napari using pip__ instead of conda:
Make sure to install `napari[all]`.
Unless you want to [choose a PyQt implementation other than _PyQt5_][napari-pyqt], in which case you should leave out the `[all]` extra.

## Usage

As a prerequisite, make sure you understand the [napari basics][napari-quickstart].

1. Open your image, or use a sample in _File - Open Sample_.

   ![Use a sample image](https://ilastik.org/assets/ilastik-napari/image-sample.png "Use a sample image")

2. Activate the plugin in the _Plugins_ menu.

   ![Activate the plugin](https://ilastik.org/assets/ilastik-napari/activation.png "Activate the plugin")

3. In _layer list_, create a new _Labels_ layer.

   ![Labels layer](https://ilastik.org/assets/ilastik-napari/labels-layer.png "Labels layer")

4. In _layers control_, switch to the _paint_ action.

   ![Paint action](https://ilastik.org/assets/ilastik-napari/paint-action.png "Paint action")

5. Draw your background labels.

   ![Paint the background](https://ilastik.org/assets/ilastik-napari/draw-background.png "Paint the background")

6. Switch to a new label.

   ![Switch label](https://ilastik.org/assets/ilastik-napari/new-label.png "Switch label")

7. Draw your foreground labels.

   ![Paint cells](https://ilastik.org/assets/ilastik-napari/draw-cells.png "Paint cells")

8. Select output types you need, and click _Run_.

   ![Plugin interface](https://ilastik.org/assets/ilastik-napari/interface.png "Plugin interface")

9. The plugin will create one layer for each output type, which you save as normal napari layers.

   ![Example output](https://ilastik.org/assets/ilastik-napari/example.png "Example output")

## Development

Create a development environment:
```
conda create -y -n ilastik-napari-dev -c ilastik-forge fastfilters pyqt=5.15 fastfilters sparse qtpy scikit-learn setuptools-scm conda-build anaconda-client
conda activate napari-ilastik-dev
pip install -e .
```

Build conda package:
```
conda activate napari-ilastik-dev
conda build -c ilastik-forge conda-recipe
anaconda upload /path/to/the/new/package.tar.bz2
```

Build wheel and sdist packages:
```
conda activate napari-ilastik-dev
pip install build twine
python -m build
python -m twine upload --repository testpypi dist/*
```

[napari]: https://napari.org/
[ilastik]: https://www.ilastik.org/
[conda-user-guide]: https://docs.conda.io/projects/conda/en/latest/user-guide/index.html
[miniconda]: https://docs.conda.io/en/latest/miniconda.html
[mambaforge]: https://github.com/conda-forge/miniforge#mambaforge
[napari-quickstart]: https://napari.org/tutorials/fundamentals/quick_start.html
[napari-pyqt]: https://napari.org/stable/plugins/best_practices.html#don-t-include-pyside2-or-pyqt5-in-your-plugin-s-dependencies
