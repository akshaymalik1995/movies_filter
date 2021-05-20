# import libraries
import streamlit as st
import pandas as pd
import numpy as np


df = pd.read_excel("cleaned_movies_data.xlsx")

df['rating'] = df['rating'] * 10
def map_name(x):
    x = x[:-4]
    x = x.strip()
    return x
df['name'] = df['name'].map(map_name)

genres = st.sidebar.multiselect("Select Genres", ["Action" , "Adventure", "Animation" , "Comedy", "Crime" , "Drama" ,  "Documentary" ,  "Science Fiction",  "Family", "History", "Horror" ,"Fantasy", "Mystery" ,"Romance" ,"Thriller" ,"War" ,"Western"])

years_list = ["All"]    
for x in range(2021, 1929, -1):
    years_list.append(x)
    
year = st.sidebar.selectbox("Select Year", years_list)


rating_list = ["All"]
rating_list.extend(["90+","80+","70+","60+","50+","40+","30+","20+","10+","00+"])
rating = st.sidebar.selectbox("Select Rating", rating_list)

filtered_df = df.copy()

genre_df = pd.DataFrame({
            
            "name": [],
            "year": [],
            "rating":[],
            "actors" : [],
            "genre" : [],
            "duration" : []
    })

# if genres:
#     for genre in genres:
#         filtered_df = filtered_df[filtered_df['genre'].str.contains(genre) == True]
if genres:
    for genre in genres:
        genre_df = pd.concat([genre_df, filtered_df[filtered_df['genre'].str.contains(genre) == True]], ignore_index=True)
    filtered_df = genre_df
    


if year != "All":
    filtered_df = filtered_df[filtered_df['year'] == year]

if rating != "All":
    filtered_df = filtered_df[filtered_df['rating'] >= float(rating[:-1])]
    
sort = st.sidebar.radio("Sort by", ["year","rating", "year + rating"])

sort_list = []
if sort == "year":
    sort_list = ['year']
if sort == "rating":
    sort_list = ['rating']
if sort == "year + rating":
    sort_list = ['year', 'rating']




if not filtered_df.empty:
    show_df = filtered_df[['name', 'rating', 'year', 'genre']].sort_values(by=sort_list, ascending=False)
    st.table(show_df.head(1000).reset_index(drop=True))
else:
    st.write("No Movies Available!")

