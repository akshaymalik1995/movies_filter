import requests
from bs4 import BeautifulStoneSoup as bs
import pandas as pd
import numpy as np
import schedule
import time
# import the file



def crawler(x , y):
    for page in range(x, y):
        r = requests.get(f"https://lookmovie.io/?p={page}")
        soup = bs(r.content)
        if soup:
            print(page)
            # movies will have name and year
            movies = soup.select("div.mv-item-infor")
            for movie in movies:
                href = movie.a['href']
         

            # Now we will extract rating, genre and actors

                r1 = requests.get("https://lookmovie.io" + href)
                soup1 = bs(r1.content)
     
                if soup1:
            
                    temp = []

             #crawl Name
                    try:
                        title = soup1.select("div.watch-heading h1")[0]
                        if title:
                            temp.append(title.get_text())
                        else:
                            temp.append("None")
                    except:
                        temp.append("None")
                        print("Errow in crawling name")

            #Crawl Year
                    try:
                        year = soup1.select("div.watch-heading h1 span")[0]
                        if year:
                            temp.append(year.get_text())
                        else:
                            temp.append("None")
                    except:
                        temp.append("None")
                        print("Errow in crawling year")

            #Crawl Rating
                    try:
                        rating = soup1.select("div.rate p span")[0]
                        if rating:
                            temp.append(rating.get_text())
                        else:
                            temp.append("None")
                    except:
                        temp.append("None")
                        print("Errow in crawling rating")

            # Crawl Actors
                    try:
                        actors = soup1.select("p.actor__name")
                        actors_list = ""
                        for actor in actors:
                            actors_list = actors_list + actor.get_text().strip() + ","
                        if actors_list:
                            temp.append(actors_list)
                        else:
                            temp.append("None")
                    except:
                        temp.append("None")
                        print("Errow in crawling actors")
            
            # Crawl Genres
                    try:
                        genres = soup1.select("div.movie-description__header span")
                        if len(genres) == 2:
                            genre = genres[1].get_text().replace(",", "").strip()
                            if genre:
                                temp.append(genre)
                            else:
                                temp.append("None")
                        if len(genres) == 1:
                            genre = genres[0].get_text().replace(",", "").strip()
                            if genre:
                                temp.append(genre)
                            else:
                                temp.append("None")
                  
                    except:
                        temp.append("None")
                        print("Errow in crawling genre")

            # Crawl Duration
                    try:
                        duration = soup1.find("div", attrs={"class" : "movie-description__duration"})
                        if duration:
                            temp.append(duration.get_text().strip())
                        else:
                            temp.append("None")
                    except:
                        temp.append("None")
                        print("Errow in crawling duration")


                    if len(temp) == 6:
                        data["name"].append(temp[0])
                        data["year"].append(temp[1])
                        data["rating"].append(temp[2])
                        data["actors"].append(temp[3])
                        data["genre"].append(temp[4])
                        data["duration"].append(temp[5])

    return data

data = {
            
            "name": [],
            "year": [],
            "rating":[],
            "actors" : [],
            "genre" : [],
            "duration" : []
    }
# def run():
cleaned_dataset = pd.read_excel("cleaned_movies_data.xlsx")

df = pd.DataFrame(crawler(1, 2))
df = df.replace("None", np.nan)
df = df.dropna(how="any")
df = df.astype({'rating': "float64"})
df1 = pd.concat([df, cleaned_dataset], ignore_index=True)
df1 = df1.drop_duplicates(subset=['name'], keep='last')
df1 = df1[df1['rating'] != 0]
df1 = df1[df1['genre'].str.isnumeric() == False]
df1.to_excel("cleaned_movies_data.xlsx", index=False)


# schedule.every(30).minutes.do(run)


# while 1:
#     schedule.run_pending()
#     time.sleep(1)