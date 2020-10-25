###
# This file will change frequently until all the modules have been written, for testing purposes
###
from data.mlearning import *
from data.database import *

# Split dataset into test and train
labeled_reviews = db_to_df(600000)
df_train, df_test = split_train_test(labeled_reviews)

# Get sentiment values
train_values = df_train['Sentiment'].values
test_values = df_test['Sentiment'].values
c = test_values.squeeze()
# Create feature matrix
vectorizer = create_vectorizer()
corpus = df_train['Review']
feature_matrix = vectorizer.fit_transform(corpus)


# Train model
model = build_model(vectorizer)
# Train classifier
model = train_model(model, feature_matrix, train_values)
# Test classifier
predicted, predicted_prob = test_model(model, df_test["Review"].values)



