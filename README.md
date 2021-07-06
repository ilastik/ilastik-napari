# napari-ilastik

## Development Setup

In the project root directory:

```shell
conda create --yes \
    --name napari-ilastik \
    --strict-channel-priority \
    --channel ilastik-forge \
    --channel conda-forge \
    --channel nodefaults \
    'python=3.7' fastfilters
conda activate napari-ilastik
pip install --editable .[dev,test]
```

## Run Example Script

In the project root directory:

```shell
conda activate napari-ilastik
python examples/simple_labeling.py
```
