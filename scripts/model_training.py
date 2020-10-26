from data.database import *
from data.mlearning import *

# Split dataset into test and train
labeled_reviews = db_to_df(5000)
df_train, df_test = split_train_test(labeled_reviews)

# Get sentiment values
train_values = df_train['Sentiment'].values
test_values = df_test['Sentiment'].values
c = test_values.squeeze()
# Create feature matrix
vectorizer = create_vectorizer()
feature_matrix = vectorizer.fit_transform(df_train['Review'])

# Train model
model = build_model(vectorizer, alg="ada")
# Train classifier
model = train_model(model, feature_matrix, train_values)
# Test classifier
predicted, predicted_prob = test_model(model, df_test["Review"].values)

# # Metrics
# classes = np.unique(test_values)
# y_test_array = pd.get_dummies(test_values, drop_first=False).values
#
# accuracy, precision, recall = get_common_metrics(test_values, predicted)
# auc = get_auc(test_values, predicted)
# print(f"Accuracy: {accuracy}| Precision: {precision}| Recall: {recall}")
# print(f"AUC: {auc}")
