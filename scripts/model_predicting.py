import os

from config import ROOT_DIR
from data.database import *
from data.file_util import read_pickled_object
from data.mlearning import *

if __name__ == '__main__':
    """
    This script retrieves labeled data and uses trained models to thoroughly test the models. Uncomment
    the algorithm variable to select your desired model.
    """
    # Split dataset into test and train
    print("Splitting dataset...\n")
    labeled_reviews = db_to_df(600000)
    df_train, df_test = split_train_test(labeled_reviews)

    # Get sentiment values
    print("Retrieving sentiment values...\n")
    test_labels = df_test['Sentiment'].values

    # Select model
    # Uncomment the algorithm variable of choice to predict with different models!
    # nb: Naive Bayes | ada: AdaBoost | rforest: Random Forest
    # algorithm = "nb"
    # algorithm = "ada"
    algorithm = "rforest"
    filepath = os.path.join(ROOT_DIR, f"static/{algorithm}.pickle")
    print(f'Reading "{algorithm}" model from file...\n')
    model = read_pickled_object(filepath)

    # Test classifier
    print("Calculating model metrics...\n")
    predicted, predicted_prob = test_model(model, df_test["Review"].values)
    accuracy, precision, recall = get_common_metrics(test_labels, predicted)
    f1 = get_f1_score(precision, recall)
    auc = get_auc(test_labels, predicted)
    plot_confusion_matrix(test_labels, predicted)
    plot_roc_curve(test_labels, predicted)
    print(f"Accuracy: {accuracy} | Precision: {precision} | Recall: {recall}")
    print(f"F1 score: {f1}")
    print(f"AUC: {auc}")
