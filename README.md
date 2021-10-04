# napari-ilastik

[Napari][napari] plugin for interactive pixel classification.
Designed to be similar to the pixel classification workflow in [classic ilastik][ilastik].

## Installation

1. Install [miniconda][miniconda].

2. If you are unfamiliar with conda, read [the conda guide][conda-guide].

3. Make sure you are in your project environment.
   _Unless you are know what you are doing, do not install packages into the base environment!_

4. Install napari and this plugin into your environment.
   ```shell
   conda install -c ilastik-forge napari-ilastik
   ```

5. Launch napari and select this plugin in the _Plugins_ menu:
   ```shell
   napari
   ```
   Alternatively, try an interactive example:
   ```shell
   python examples/simple_labeling.py
   ```

## Development

### Public version update checklist

1. Update version string in  `__init__.py`.
2. Commit changes.
3. Create a new Git tag `v<VERSION>`.
3. Build conda package.
4. Upload conda package.
5. Update version string in `__init__.py` to `<NEXTVERSION>.dev0`
6. Commit changes.
7. Push branch and tags to Git remote.

`<VERSION>` format is usually either `MAJOR.MINOR` or `MAJOR.MINOR.PATCH`.
Consult [PEP 440][pep440] for additional information.

[napari]: https://napari.org/
[ilastik]: https://www.ilastik.org/
[miniconda]: https://docs.conda.io/en/latest/miniconda.html
[conda-guide]: https://docs.conda.io/projects/conda/en/latest/user-guide/getting-started.html
[pep440]: https://www.python.org/dev/peps/pep-0440/
