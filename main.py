from whoosh.index import open_dir
from whoosh.query import Query
from whoosh.qparser import QueryParser
import streamlit as st
import pandas as pd
from time import time

st.title("Search App")
query = st.text_input("Enter your query")
num_results = st.slider("Number of results", 1, 100)

# index is cache
@st.cache_resource()
def search(query, num_results):
    ix = open_dir("Index")
    parser = QueryParser("content", ix.schema)
    searcher = ix.searcher()
    result = searcher.search(parser.parse(query), limit=num_results)
    return result

        


if st.button("Search"):
    result = search(query, num_results=num_results)
    title = list(map(lambda x: x["title"], result))
    content = list(map(lambda x: x["content"], result))
    df = pd.DataFrame({"Title": title,"Content": content})
    st.write(df)
