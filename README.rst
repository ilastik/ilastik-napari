napari-ilastik
==============

Development Setup
-----------------

::

    conda create -y -n napari-ilastik \
        -c ilastik-forge -c conda-forge \
        'python=3.7' fastfilters
    conda activate napari-ilastik
    pip install -e .[dev,test]
