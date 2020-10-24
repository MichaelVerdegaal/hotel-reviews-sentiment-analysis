from data.database import df_to_db
from data.file_util import read_labeled_reviews

if __name__ == '__main__':
    """
    This script uploads a dataframe to a connected database, replacing it if there's already a table. Requires your
    connection to be valid.
    """
    reviews = read_labeled_reviews()
    df_to_db(reviews)
