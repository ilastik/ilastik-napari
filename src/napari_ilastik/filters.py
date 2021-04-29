import math
from typing import Sequence

import fastfilters
import numpy
from sklearn.base import BaseEstimator, TransformerMixin


class Filter(BaseEstimator, TransformerMixin):
    def fit(self, X=None, y=None, **kwargs):
        return self

    def transform(self, X):
        raise NotImplementedError

    @property
    def kernel_size(self):
        raise NotImplementedError

    def _more_tags(self):
        return {"requires_fit": False, "stateless": True}


class SingleFilter(Filter):
    def __init__(self, scale):
        self.scale = scale

    def __init_subclass__(cls, order, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.order = order

    @property
    def kernel_size(self):
        # TODO: Make sure that the kernel size formula is pixel-perfect.
        return math.ceil((3 + self.order / 2) * self.scale) + 1

    _required_parameters = ("scale",)


class Gaussian(SingleFilter, order=0):
    def transform(self, X):
        return fastfilters.gaussianSmoothing(X, sigma=self.scale)


class DifferenceOfGaussians(SingleFilter, order=0):
    def __init__(self, scale, *, inner_k=0.5):
        super().__init__(scale)
        self.inner_k = inner_k

    def transform(self, X):
        outer = fastfilters.gaussianSmoothing(X, sigma=self.scale)
        inner = fastfilters.gaussianSmoothing(X, sigma=self.inner_k * self.scale)
        return outer - inner


class GaussianGradientMagnitude(SingleFilter, order=1):
    def transform(self, X):
        return fastfilters.gaussianGradientMagnitude(X, sigma=self.scale)


class LaplacianOfGaussian(SingleFilter, order=2):
    def transform(self, X):
        return fastfilters.laplacianOfGaussian(X, scale=self.scale)


class StructureTensorEigenvalues(SingleFilter, order=1):
    def __init__(self, scale, *, inner_k=0.5):
        super().__init__(scale)
        self.inner_k = inner_k

    def transform(self, X):
        return fastfilters.structureTensorEigenvalues(
            X, innerScale=self.inner_k * self.scale, outerScale=self.scale
        )


class HessianOfGaussianEigenvalues(SingleFilter, order=2):
    def transform(self, X):
        return fastfilters.hessianOfGaussianEigenvalues(X, scale=self.scale)


class FilterSet(Filter):
    def __init__(self, *, filters: Sequence[Filter]):
        self.filters = filters

    def transform(self, X):
        # TODO: Optimize feature computations by sharing intermediate results.
        ys = [f.transform(X).reshape((*X.shape, -1)) for f in self.filters]
        return numpy.concatenate(ys, axis=-1)

    @property
    def kernel_size(self):
        return max(f.kernel_size for f in self.filters)
