"""
@author: Jonathan
@credit: http://www.davidsbatista.net/blog/2018/02/23/model_optimization/
https://www.kaggle.com/baghern/a-deep-dive-into-sklearn-pipelines
"""

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline, FeatureUnion


def make_features_pipeline(TextTransformer, text_selector_key, custom_features=True):
    text = Pipeline([
        ('selector', TextSelector(key=text_selector_key)),
        ('text', TextTransformer)
    ])

    HP_links = Pipeline([
        ('selector', NumberSelector(key='HP_links_count'))
    ])

    nonHP_links = Pipeline([
        ('selector', NumberSelector(key='nonHP_links_count'))
    ])

    if custom_features:
        feats = FeatureUnion([
            ('text', text),
            ('HP_links', HP_links),
            ('nonHP_links', nonHP_links)
        ])
    else:
        feats = FeatureUnion([
            ('text', text)
        ])

    return feats


class TextSelector(BaseEstimator, TransformerMixin):
    """
    Transformer to select a single column from the data frame to perform additional transformations on
    Use on text columns in the data
    """

    def __init__(self, key):
        self.key = key

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X[self.key]


class NumberSelector(BaseEstimator, TransformerMixin):
    """
    Transformer to select a single column from the data frame to perform additional transformations on
    Use on numeric columns in the data
    """

    def __init__(self, key):
        self.key = key

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X[[self.key]]