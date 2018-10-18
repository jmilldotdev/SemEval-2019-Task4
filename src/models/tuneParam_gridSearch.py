"""
@author: Negar
"""
import pandas
from sklearn.ensemble import GradientBoostingClassifier
import numpy as np
from sklearn import metrics
from sklearn.grid_search import GridSearchCV
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression


# grid search to find the best parameters for the best accuracy with 10-fold cross validation on training set
def grid_search(model, param_grid, X, y, scorer='accuracy', n_jobs=3, cv=10):
    grid = GridSearchCV(model, param_grid=param_grid, cv=cv, n_jobs=n_jobs,
                        scoring=scorer,
                        pre_dispatch=n_jobs)

    # keep fitted model for future use -- not using it now TODO
    fit_model = grid.fit(X, y)
    return grid.best_params_, grid.best_score_


# Tune parameters for models and print best parameters
# @credit: got parameters for Multinamial Naive Bayes and Gradient Boosting from https://github.com/Morgan243/CMSC516-SE-T8/blob/master/SemEvalEight/modeling/task1/task1_bag_of_words.py
def tune_param(model_list, X_train, y_train):
    model_dict = {
        'nb': 'Multinomial Naive Bayes',
        'lr': 'LogisticRegression',
        'gb': 'GradientBoostingClassifier'
    }

    for model_type in model_list:
        # grid search on Multinamial Naive Bayes
        if model_type == 'nb':
            nb_best_params, nb_best_score = grid_search(MultinomialNB(),
                                                        param_grid=dict(alpha=[10 ** a for a in range(-3, 4, 1)]),
                                                        X=X_train, y=y_train)
            print(nb_best_params)
            print(nb_best_score)

        # grid search on Logistic regression
        elif model_type == 'lr':
            lr_best_params, lr_best_score = grid_search(LogisticRegression(),
                                                        param_grid=dict(C=[0.001, 0.01, 0.1, 1, 10, 30, 100, 1000],
                                                                        solver=('newton-cg', 'sag', 'saga'),
                                                                        class_weight=('balanced', 'None')),
                                                        X=X_train, y=y_train)
            print(lr_best_params)
            print(lr_best_score)

        # grid search on Gradient Boosting
        elif model_type == 'gb':
            gb_best_params, gb_best_score = grid_search(GradientBoostingClassifier(),
                                                        param_grid=dict(
                                                            max_depth=list(range(3, 7, 1)),
                                                            max_leaf_nodes=[None],
                                                            min_samples_leaf=list(range(2, 4, 1)),
                                                            min_samples_split=list(range(2, 5, 2)),
                                                            learning_rate=np.arange(0.7, 1.5, 0.33)),
                                                        X=X_train, y=y_train)
            print(gb_best_params)
            print(gb_best_score)
        else:
            raise ValueError("No model type provided")

            # return nb_best_params, gb_best_params
