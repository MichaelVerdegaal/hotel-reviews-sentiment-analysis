import numpy as np
from sklearn import model_selection, feature_extraction, pipeline, naive_bayes, metrics
from sklearn.ensemble import AdaBoostClassifier
from sklearn.svm import SVC


def split_train_test(df):
    """
    Splits a dataframe into a training and test dataframe
    :param df: dataframe to split
    :return: training dataframe, test dataframe
    """
    df_train, df_test = model_selection.train_test_split(df, test_size=0.3)
    return df_train, df_test


def create_vectorizer(feature_count=10000, ngram_range=(1, 2)):
    """
    Create vectorizer object
    :param feature_count: maximum amount of features
    :param ngram_range: tuple describing what type of ngrams to use
    :return: vectorizer
    """
    vec = feature_extraction.text.TfidfVectorizer(max_features=feature_count, ngram_range=ngram_range)
    return vec


def get_top_ngrams(vectorizer, top_n=5):
    """
    Get highest ranking ngrams of a feature matrix
    :param vectorizer: vectorizer object
    :param top_n: amount of top n-grams to return
    :return: top n-grams
    """
    indices = np.argsort(vectorizer.idf_)[::-1]
    features = vectorizer.get_feature_names()
    top_features = [features[i] for i in indices[:top_n]]
    return top_features


def build_model(vectorizer, alg="nb"):
    """
    Build a classifier model
    :param vectorizer: vectorizer object
    :param alg: what classifier algorithm to use
    :return: classifier model
    """
    # Naive bayes
    if alg == "nb":
        classifier = naive_bayes.MultinomialNB()
    # ADA boost
    elif alg == "ada":
        classifier = AdaBoostClassifier()
    # Support vector machine
    elif alg == "svc":
        classifier = SVC(probability=True)
    else:
        raise
    model = pipeline.Pipeline([("vectorizer", vectorizer),
                               ("classifier", classifier)])
    return model


def train_model(model, feature_matrix, train_values):
    """
    Train classifier model
    :param model: classifier model
    :param feature_matrix: feature matrix
    :param train_values: values to train the model on
    :return: trained model
    """
    model["classifier"].fit(feature_matrix, train_values)
    return model


def test_model(model, test_review_values):
    """
    Get predicted values from test set
    :param model: classifier model
    :param test_review_values: values to test with
    :return: predicted values (binary), predicted values (probability)
    """
    predicted = model.predict(test_review_values)
    predicted_prob = model.predict_proba(test_review_values)
    return predicted, predicted_prob


def get_common_metrics(test_values, predicted):
    """
    Return some common classifier metrics
    :param test_values: values to test with
    :param predicted: predicted values
    :return: accuracy, precision and recall value
    """
    accuracy = metrics.accuracy_score(test_values, predicted)
    precision = metrics.precision_score(test_values, predicted)
    recall = metrics.recall_score(test_values, predicted)
    return accuracy, precision, recall


def get_auc(test_values, predicted):
    """
    Get area under the curve value
    :param test_values: values to test with
    :param predicted: predicted values
    :return: auc value
    """
    auc = metrics.roc_auc_score(test_values, predicted,
                                multi_class="ovr")
    return round(auc, 2)
