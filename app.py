# import libraries
import streamlit as st
import pandas as pd
import numpy as np

# READING THE DATASET
df = pd.read_excel("cleaned_movies_data.xlsx")

# There is some issue with the ratings. It is showing with four decimals
# Converting rating into out of 100
df['rating'] = df['rating'] * 10

# Removing the year from the "name" column
def map_name(x):
    x = x[:-4]
    x = x.strip()
    return x
df['name'] = df['name'].map(map_name)

# SELECT WEBSITE OPTIONS

tab = st.sidebar.selectbox("Choose what you want to do:", ['Explore movies','Find Similar movies', 'Search movies'])





################### MOVIE RECOMMENDATION MODEL STARTS ###########################



# FUNCTION TO RECOMMEND MOVIES
def recommend_movie_model(id , data):
    
    matrix = np.empty(data.shape[0])
    
    for y in data.index:
        score = 0
        # Add rating score
        score  += 20 - abs( data.iloc[id]['rating'] - df.iloc[y]['rating'])
        # Adding genre score
        x_genre_list = set(data.iloc[id]['genre'].split())
        
        y_genre_list = set(data.iloc[y]['genre'].split())
        genre_inter = x_genre_list.intersection(y_genre_list)
        score += len(genre_inter) * 20
        
        # Add actor score
        x_actor_list = set(data.iloc[id]['actors'].split())
        y_actor_list = set(data.iloc[y]['actors'].split())
        actor_inter = x_actor_list.intersection(y_actor_list)
        score += len(actor_inter) * 20
        
        matrix[y] = score
       
 
    
    scores =  list(enumerate(matrix))
    sorted_scores = sorted(scores, key = lambda x : x[1], reverse=True)
    
    count = 0
    index_list = []
    for item in sorted_scores:
        index_list.append(item[0])
        count += 1
        if count > 1000:
            break
    
    return df.iloc[index_list]




################### MOVIE RECOMMENDATION MODEL ENDS ###########################

######################## SEARCH SECTION STARTS HERE #############################

if tab == "Search movies":
    st.header("Search movies")
    search_title = st.text_input("Enter the movie name")
    if search_title:
        df_search = df[df['name'].str.startswith(search_title) == True]
        st.table(df_search[['name', 'rating', 'year', 'actors', 'genre']].reset_index(drop=True))


# A COPY OF DATASET

if tab == "Find Similar movies":
    st.header("Find Similar movies")
    st.write("Be patient. It takes 30 seconds to find similar movies")
    movie_title = st.text_input("Enter the title of the movie")
    movie_title = movie_title.strip()
    if movie_title:
        id_list = df.index[df['name'] == movie_title].to_list()
        if id_list:
            id = id_list[0]
            df_recommend = recommend_movie_model(id, df)
            st.table(df_recommend[['name', 'rating', 'year', 'genre']].reset_index(drop=True))
        else:
            st.write("This movies does not exist. Enter the correct title of the movie.")




# FILTERING GENRES
if tab == "Explore movies":
    # INPUT FOR SELECTING THE GENRE
    st.header("Explore Movies")
    filtered_df = df.copy()
    genres = st.sidebar.multiselect("Select Genres", ["Action" , "Adventure", "Animation" , "Comedy", "Crime" , "Drama" ,  "Documentary" ,  "Science Fiction",  "Family", "History", "Horror" ,"Fantasy", "Mystery" ,"Romance" ,"Thriller" ,"War" ,"Western"])

    # Creating selector for the Years
    years_list = ["All"]    
    for x in range(2021, 1929, -1):
        years_list.append(x)
        
    year = st.sidebar.selectbox("Select Year", years_list)

    # CREATE SELECTORS FOR RATING
    rating_list = ["All"]
    rating_list.extend(["90+","80+","70+","60+","50+","40+","30+","20+","10+","00+"])
    rating = st.sidebar.selectbox("Select Rating", rating_list)
    if genres:
        genre_df = pd.DataFrame({
                
                "name": [],
                "year": [],
                "rating":[],
                "actors" : [],
                "genre" : [],
                "duration" : []
        })
        for genre in genres:
            genre_df = pd.concat([genre_df, filtered_df[filtered_df['genre'].str.contains(genre) == True]], ignore_index=True)
        filtered_df = genre_df.drop_duplicates()
        

    # FILTER YEARS
    if year != "All":
        filtered_df = filtered_df[filtered_df['year'] == year]

    if rating != "All":
        filtered_df = filtered_df[filtered_df['rating'] >= float(rating[:-1])]


    # SORTING DATABASE 
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



