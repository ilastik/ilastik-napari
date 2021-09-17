# napari-ilastik

[Napari][napari] plugin for interactive pixel classification.
Designed to be similar to pixel classification workflow in [classic ilastik][ilastik].

## Installation

1. Download and install [miniconda][miniconda].

2. Create a new conda environment:
   * Windows:
     ```shell
     conda create --name napari-ilastik --file conda-win-64.lock
     ```
   * Linux:
     ```shell
     conda create --name napari-ilastik --file conda-linux-64.lock
     ```
   * macOS:
     ```shell
     conda create --name napari-ilastik --file conda-osx-64.lock
     ```

3. Activate the environment:
   ```shell
   conda activate napari-ilastik
   ```

4. Install napari and this plugin into the active environment:
   ```shell
   python -m pip install --editable .
   ```

5. Start napari, and select this plugin in the _Plugins_ menu:
   ```shell
   napari
   ```
   Alternatively, try an interactive example:
   ```shell
   python examples/simple_labeling.py
   ```

[napari]: https://napari.org/
[ilastik]: https://www.ilastik.org/
[miniconda]: https://docs.conda.io/en/latest/miniconda.html
