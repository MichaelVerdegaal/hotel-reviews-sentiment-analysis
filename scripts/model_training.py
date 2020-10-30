import os

from config import ROOT_DIR
from data.database import *
from data.file_util import pickle_object
from data.mlearning import *

if __name__ == '__main__':
    """
    This script retrieves labeled data from the database and uses it to train a machine learning model. Uncomment
    the algorithm variable to select your desired model.
    """
    # Split dataset into test and train
    print("Splitting dataset...\n")
    labeled_reviews = db_to_df(600000)
    df_train, df_test = split_train_test(labeled_reviews)

    # Get sentiment values
    print("Retrieving sentiment values...\n")
    train_values = df_train['Sentiment'].values
    test_values = df_test['Sentiment'].values

    # Create feature matrix
    print("Building feature matrix...\n")
    vectorizer = create_vectorizer()
    feature_matrix = vectorizer.fit_transform(df_train['Review'])

    # Select model
    # Uncomment the algorithm variable of choice to train different models!
    # nb: Naive Bayes | ada: AdaBoost | rforest: Random Forest

    algorithm = "nb"
    # algorithm = "ada"
    # algorithm = "rforest"
    filepath = os.path.join(ROOT_DIR, f"static/{algorithm}.pickle")
    print(f'Building "{algorithm}" model...\n')
    model = build_model(vectorizer, alg=f"{algorithm}")

    # Train model
    print(f'Training "{algorithm}" model...\n')
    model = train_model(model, feature_matrix, train_values)
    pickle_object(model, filepath)
    print("Model saved!")
