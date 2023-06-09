from pynytimes import NYTAPI
import streamlit as st
import pandas as pd

import requests
from io import BytesIO
from PIL import Image

st.set_page_config(layout="wide")


def main():

    api_key = "Frvpakmi7RzBNtGrwxKbcGNxwqBNvVEI"
    nyt = NYTAPI(api_key, parse_dates=True)
    review = []

    # saving the book keys in set for the dataframe
    book_keys = []
# Get fiction best sellers list
    books = nyt.best_sellers_list()
    dicts = books[0].keys()
    for dic in dicts:
        book_keys.append(dic)

    # storing the values of the books for dataframe
    book_val = []
    for book in books:
        book_val_temp = []
        for vals in book.values():
            book_val_temp.append(vals)
        book_val.append(book_val_temp)

    books_df = pd.DataFrame(book_val, columns=book_keys)
    books_df.drop(columns=['asterisk', 'dagger',
                  'primary_isbn13', 'price', 'contributor_note',
                           "age_group", "book_review_link", "first_chapter_link",
                           "sunday_review_link", "article_chapter_link", 'primary_isbn10', 'isbns', 'buy_links'], inplace=True)

    st.write(books_df)
    book_title = books_df.title.to_list()
    selected_books = st.multiselect("Books title interested", book_title)
    review = []
    for book in selected_books:
        rev_temp = nyt.book_reviews(title=book)
        review.append(rev_temp)
    book_info(selected_books, books_df, review)


def book_info(selected_books, books_df, review):

    select_books = books_df[books_df['title'].isin(selected_books)]
    books_url = select_books.book_image.to_list()

    # Grid Setting for images
    n_cols = int(st.number_input("Grid Size", 2, 8, 4))
    n_pics = len(books_url)
    n_rows = int(1+n_pics//n_cols)
    rows = [st.columns(n_cols) for _ in range(n_rows)]
    cols = [column for row in rows for column in row]
    for col, image_ur in zip(cols, books_url):
        response = requests.get(image_ur)
        img = Image.open(BytesIO(response.content))
        # image = Image.open(image_url[1])
        image = img.resize((400, 600))
        col.image(image)
    st.title("Book Information")
    col_list = list(books_df.columns)
    col_list.remove('title')
    st.write(select_books.reset_index())
    for rev in review:
        try:
            st.write(rev[0])
        except:
            st.write("No reviews")


if __name__ == "__main__":
    st.title('NY Time Books Review and Connections')
    main()
