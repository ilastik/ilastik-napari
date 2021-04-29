from sklearn.base import (
    BaseEstimator,
    ClassifierMixin,
    MetaEstimatorMixin,
    TransformerMixin,
)


def _fit_with(func, X, y, **kwargs):
    return func(X[tuple(y.coords)], y.data, **kwargs)


def _predict_with(func, X):
    return func(X.reshape((-1, X.shape[-1]))).reshape(X.shape[:-1])


class NDSparseClassifier(
    BaseEstimator, MetaEstimatorMixin, ClassifierMixin, TransformerMixin
):
    def __init__(self, estimator):
        self.estimator = estimator

    def fit(self, X, y, **kwargs):
        return _fit_with(self.estimator.fit, X, y, **kwargs)

    def partial_fit(self, X, y, **kwargs):
        return _fit_with(self.estimator.partial_fit, X, y, **kwargs)

    def predict(self, X):
        return _predict_with(self.estimator.predict, X)

    def predict_proba(self, X):
        return _predict_with(self.estimator.predict_proba, X)

    def predict_log_proba(self, X):
        return _predict_with(self.estimator.predict_log_proba, X)

    def transform(self, X):
        return _predict_with(self.estimator.transform, X)

    def fit_predict(self, X, y, **kwargs):
        return self.fit(X, y, **kwargs).predict(X)
