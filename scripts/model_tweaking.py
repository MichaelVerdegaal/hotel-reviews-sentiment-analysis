import os

from config import ROOT_DIR
from data.database import *
from data.mlearning import *
from sklearn.model_selection import GridSearchCV

if __name__ == '__main__':
    """
    This script can help you tweak your models by finding the right hyperparameters to use. This is done by the use
    of grid search, which extensively tests a combination of parameters for you. If you don't like the numbers
    in the current grids, just change them to what you like.
    """
    # Split dataset into test and train
    print("Splitting dataset...\n")
    labeled_reviews = db_to_df(600000)
    df_train, df_test = split_train_test(labeled_reviews)

    # Get sentiment values
    print("Retrieving sentiment values...\n")
    train_labels = df_train['Sentiment'].values
    test_labels = df_test['Sentiment'].values

    # Create feature matrix
    print("Building feature matrix...\n")
    vectorizer = create_vectorizer()
    feature_matrix = vectorizer.fit_transform(df_train['Review'])

    # Select model
    # Uncomment the algorithm and grid variable of choice to tweak different models
    # nb: Naive Bayes | ada: AdaBoost | rforest: Random Forest

    # algorithm = "nb"
    # grid = {'classifier__alpha': [0.01, 0.25, 0.5, 0.75, 1.0]}

    # algorithm = "ada"
    # grid = {'classifier__n_estimators': [10, 25, 50, 100],
    #         'classifier__learning_rate': [0.01, 0.5, 1]}

    algorithm = "rforest"
    grid = {'classifier__max_depth': [25, 50, 100, 200],
            'classifier__min_samples_split': [2, 5, 10],
            'classifier__min_samples_leaf': [1, 2, 4]}

    filepath = os.path.join(ROOT_DIR, f"static/{algorithm}.pickle")
    print(f'Building "{algorithm}" model...\n')
    model = build_model(vectorizer, alg=f"{algorithm}")

    print("Grid searching...\n")
    # If you struggle running this script please lower the amount of n_jobs
    n_jobs = 6
    param_search = GridSearchCV(estimator=model, param_grid=grid, verbose=2, n_jobs=n_jobs)
    param_search.fit(df_train['Review'], train_labels)

    print("Printing best results...\n")
    print(param_search.best_params_)
