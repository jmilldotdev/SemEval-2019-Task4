import pandas
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
import numpy as np
from sklearn import metrics


def create_train_test_tfidf(trainFilePath, testFilePath):
    train = pandas.read_csv(trainFilePath)
    vectorizer = CountVectorizer()
    text = train.preprocessed_text.tolist()
    bag_of_words = vectorizer.fit(text)
    bag_of_words = vectorizer.transform(text)
    #tf and tfidf
    tfidf_transformer = TfidfTransformer()
    X_train_tfidf = tfidf_transformer.fit_transform(bag_of_words)
    y_train = train.hyperpartisan.tolist()
    #X_train_tfidf.shape
    #testing
    test = pandas.read_csv(testFilePath)
    testdata = test.preprocessed_text.tolist()
    #newbag = vectorizer.fit(testdata)
    testbag = vectorizer.transform(testdata)
    X_test_tfidf = tfidf_transformer.transform(testbag)
    y_test = test.hyperpartisan.tolist()
    return X_train_tfidf, X_test_tfidf, y_train, y_test

def run_models(model_list, X_train, X_test, y_train, y_test):
    
    model_dict ={
        'nb' : 'Multinomial Naive Bayes',
        'lr' : 'LogisticRegression',
        'gb' : 'GradientBoostingClassifier'
    } 
    
    for model_type in model_list:
        if model_type == 'nb':
            clf = MultinomialNB().fit(X_train, y_train)
        elif model_type == 'lr':
            clf = LogisticRegression(C=30.0, class_weight='balanced', solver='newton-cg', multi_class='multinomial', n_jobs=-1, random_state=40)
            clf.fit(X_train, y_train)
        elif model_type == 'gb':
            clf = GradientBoostingClassifier(n_estimators=170, max_depth=5, learning_rate=0.5, min_samples_leaf=3, min_samples_split=4).fit(X_train, y_train)
        else:
            raise ValueError("No model type provided")        
        predicted = clf.predict(X_test)
        print(model_dict[model_type])
        evaluate_model(predicted, y_test)

def evaluate_model(predicted, y_test):
    #rint(predicted)
    print(np.mean(predicted == y_test))
    print(metrics.classification_report(y_test, predicted))