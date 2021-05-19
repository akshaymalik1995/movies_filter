# import libraries
import streamlit as st
import pandas as pd
import numpy as np


df = pd.read_excel("cleaned_movies_data.xlsx")




genres = st.sidebar.multiselect("Select Genres", ["Action" , "Adventure", "Animation" , "Comedy", "Crime" , "Drama" ,  "Documentary" ,  "Science Fiction",  "Family", "History", "Horror" ,"Fantasy", "Mystery" ,"Romance" ,"Thriller" ,"War" ,"Western"])

years_list = ["All"]    
for x in range(2021, 1929, -1):
    years_list.append(x)
    
year = st.sidebar.selectbox("Select Year", years_list)


rating_list = ["All"]
rating_list.extend(["9+","8+","7+","6+","5+","4+","3+","2+","1+","0+"])
rating = st.sidebar.selectbox("Select Rating", rating_list)

filtered_df = df.copy()



if genres:
    for genre in genres:
        filtered_df = filtered_df[filtered_df['genre'].str.contains(genre) == True]


if year != "All":
    filtered_df = filtered_df[filtered_df['year'] == year]

if rating != "All":
    filtered_df = filtered_df[filtered_df['rating'] >= float(rating[:-1])]
    
show_all = st.button("Show All")
if not filtered_df.empty:
    show_df = filtered_df[['name', 'rating', 'year', 'genre']].sort_values(by=['year'], ascending=False)
    st.table(show_df.head(1000).reset_index(drop=True))
else:
    st.write("No Movies Available!")

