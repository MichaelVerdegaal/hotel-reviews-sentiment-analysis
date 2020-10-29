import os

from config import ROOT_DIR
from data.database import *
from data.file_util import read_pickled_object
from data.mlearning import *

# Split dataset into test and train
print("Splitting dataset...\n")
labeled_reviews = db_to_df(600000)
df_train, df_test = split_train_test(labeled_reviews)


# Get sentiment values
print("Retrieving sentiment values...\n")
train_values = df_train['Sentiment'].values
test_values = df_test['Sentiment'].values


# Select model
# Uncomment the algorithm variable of choice to train different models!
# nb: Naive Bayes | ada: AdaBoost | svc: Support Vector Machine

algorithm = "nb"
# algorithm = "ada"
# algorithm = "rforest"
filepath = os.path.join(ROOT_DIR, f"static/{algorithm}.pickle")
print(f'Reading "{algorithm}" model from file...\n')
model = read_pickled_object(filepath)


# Test classifier
print("Calculating model metrics...\n")
predicted, predicted_prob = test_model(model, df_test["Review"].values)
accuracy, precision, recall = get_common_metrics(test_values, predicted)
f1 = get_f1_score(precision, recall)
auc = get_auc(test_values, predicted)
plot_confusion_matrix(test_values, predicted)
plot_roc_curve(test_values, predicted)
print(f"Accuracy: {accuracy} | Precision: {precision} | Recall: {recall}")
print(f"F1 score: {f1}")
print(f"AUC: {auc}")
