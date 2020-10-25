import numpy as np
from sklearn import model_selection, feature_extraction, pipeline, naive_bayes, metrics
from sklearn.ensemble import AdaBoostClassifier
from sklearn.svm import SVC


def split_train_test(df):
    df_train, df_test = model_selection.train_test_split(df, test_size=0.3)
    return df_train, df_test


def create_vectorizer(feature_count=10000, ngram_range=(1, 2)):
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
    classifier = None
    if alg == "nb":
        classifier = naive_bayes.MultinomialNB()
    if alg == "ab":
        classifier = AdaBoostClassifier()
    if alg == "svc":
        classifier = SVC(probability=True)
    model = pipeline.Pipeline([("vectorizer", vectorizer),
                               ("classifier", classifier)])
    return model


def train_model(model, feature_matrix, train_values):
    model["classifier"].fit(feature_matrix, train_values)
    return model


def test_model(model, test_review_values):
    predicted = model.predict(test_review_values)
    predicted_prob = model.predict_proba(test_review_values)
    return predicted, predicted_prob


def get_common_metrics(test_values, predicted):
    accuracy = metrics.accuracy_score(test_values, predicted)
    precision = metrics.precision_score(test_values, predicted)
    recall = metrics.recall_score(test_values, predicted)
    return accuracy, precision, recall


def get_auc(test_values, predicted):
    auc = metrics.roc_auc_score(test_values, predicted,
                                multi_class="ovr")
    return round(auc, 2)
