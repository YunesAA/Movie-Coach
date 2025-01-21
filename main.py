import sqlite3
import requests
import time

apiKey='INSERT API KEY'
base_url='http://www.omdbapi.com/'
conn = sqlite3.connect('data.db')
cur = conn.cursor()
user=''
user_id=''


def Log_In():
    global user
    global user_id
    print('\n=====Log_In=====')
    username=input('Enter username ')
    try:
        cur.execute("SELECT Username FROM User WHERE Username=?", (username,))
        user=cur.fetchone()[0]
        #print('user', user)
    except Exception:
        print("Thats not an account \nGoing to SignUp page")
        Sign_Up()

    if user:    
        password=input("Enter password ")
        cur.execute("SELECT Password FROM User WHERE Username=?", (username,))
        p = cur.fetchone()
        #print('pass: ',p[0])
        
        if password==p[0]:
            print(f"Welcome {user}!")
            time.sleep(0.5)
            cur.execute("SELECT User_ID FROM User WHERE Username=?", (username,))
            user_id=cur.fetchone()[0]
            # print('user_id',user_id )
            menu()
        else:
            print("wrong password")
            Log_In()
    else:
        print("incorrect username")
        Log_In()




def Sign_Up():
    global user
    global user_id

    print('\n=====Sign_Up=====')
    user=input("Create username: ")
    Password=input("Create password: ")

    cur.execute(f"INSERT INTO User (Username, Password) VALUES ('{user}','{Password}')")
    conn.commit()

    cur.execute("SELECT User_ID FROM User WHERE Username=?", (user,))
    user_id=cur.fetchone()[0]
    
    print(f"Welcome {user}!")
    menu()


def Main():
    print("======LogIn/SignUp======")
    print("1. LogIn")
    print("2. SignUp")
    print("0. Exit")
    choice= input("\n Select an option (0-2): ")

    if choice == "1":
        Log_In()
    elif choice == "2":
        Sign_Up()
    elif choice == "0":
        exit()
    else: 
        print("pick a valid value (0-2): ")
        Main()


def menu():
    print('\n')
    print("\n=====MAIN MENU=====")
    print('1. Search for a Movie')
    print('2. Manage Watchlist')
    print('3. View Recommendations')
    print('4. Follow/Unfollow Users')
    print('0. Exit')

    choice=input('\n Select an option (0-4): ')
    if choice == "1":
        Movie()
    elif choice == "2":
        Watchlist()
    elif choice == "3":
        Recommendations()
    elif choice == "4":
        Follow_Unfollow()
    elif choice == "0":
        print("Exiting...")
        exit()
    else:
        print("Error: Exiting...")


def Movie():
    print("\n=====MOVIE SEARCH=====")
    movie_search =input('Search movie: ')
    url = f"{base_url}?apikey={apiKey}&s={movie_search}"    
    #print(f"Requesting URL: {url}")
    response = requests.get(url)
    data=response.json()

    print("\n=========Movies=========")
    i=1
    if 'Search' in data:
        for movies in data['Search']:
            print(i,'-', movies['Title'])
            i=i+1
    else:
        print("Something went wrong, try again...")
        print("(try putting a space between the words and the numbers if you have any)")
        Movie()

    print("VIEW MORE by typing the movie's number on the list or go back to menu by typing 0")
    choice=input('Select an option (0-10): ')
    index=int(choice)-1

    if choice == '0':
        print("Going to Menu...")
        menu()

    
    elif 0 <= index and index <= 10:
        if index <= len(data['Search']):
            movie_id = data['Search'][index]['imdbID']

            #url
            url_details = f"{base_url}?apikey={apiKey}&i={movie_id}"
            response = requests.get(url_details)
            movie_details = response.json()

            if 'Title' in movie_details:
                try:
                    #add to movie seach history
                    cur.execute('INSERT INTO Movie (Movie_ID, Title, Genre, Release_Date, Director) VALUES (?,?,?,?,?)', 
                                (movie_details['imdbID'], movie_details['Title'], movie_details['Genre'], movie_details['Released'],movie_details['Director']))
                    conn.commit()
                except Exception:
                    cur.execute('SELECT Movie_ID, Title, Genre, Release_Date, Director FROM Movie WHERE Movie_ID = ?',(movie_details['imdbID'],))


                print("\n=====Movie Details=====")
                print(f"Title:       {movie_details['Title']}")
                print(f"Year:        {movie_details['Year']}")
                print(f"Genre:       {movie_details['Genre']}")
                print(f"Director:    {movie_details['Director']}")
                print(f"Actors:      {movie_details['Actors']}")
                print(f"IMDb rating: {movie_details['imdbRating']}")

                #add to watchlist?
                add_to_watchlist = input("\nWould you like to add this movie to your watchlist? (type 'yes' or 'no'): ")
                if add_to_watchlist.lower()=='yes':
                    add_watchlist(movie_id)
                    print("Movie added to your watchlist!")
                else:
                    print("Movie not added \nGoing to movie search...")
                    Movie()
        else:
            print("Error: Going back to movie search...")
            Movie()

    else:
        print("Error: Going back to movie search...")
        Movie()


def add_watchlist(id):
    cur.execute('SELECT * FROM Recommended WHERE User_ID = ? AND Movie_ID = ?', (user_id, id))

    if cur.fetchone() is None:  #If no matching row is found, insert a new movie
        print('\n adding movie to watchlist...')
        cur.execute('INSERT INTO Watchlist (User_ID, Movie_ID, Watchlist_ID) VALUES (?,?,?)', (user_id, id, user))
        conn.commit()
        Watchlist()

    else:
        print("Already in watchlist")
        Watchlist()


def Watchlist():
    print("\nWatchlist function")
    cur.execute('SELECT User_ID, Movie_ID FROM watchlist WHERE User_ID = ?', (user_id,))
    movies = cur.fetchall()
    i=1
    
    if movies:
        print("\nYour Watchlist:")
        print("\nSelect movie number to see more info")
        titles=[]
        Years=[]
        Genres=[]
        Directors=[]
        Actors=[]
        movie_ids = []
    
        for m in movies:
            movie_id = m[1] # movie ID
            # print('movie[0]', m[0]) # user name
            # print('movie[1]', m[1]) # movie ID
            url = f"{base_url}?apikey={apiKey}&i={movie_id}"    
            response = requests.get(url)
            data = response.json()

            if 'Title' in data:
                titles.append(data['Title'])
                Years.append(data['Year'])
                Genres.append(data['Genre'])
                Directors.append(data['Director'])
                Actors.append(data['Actors'])
                movie_ids.append(movie_id)

                print(f"{i} - ({data['Year']}) {data['Title']}")
                i=i+1

    print("\nSelect a movie number to see more info or type '0' to go back to the menu:")
    choice = input("Enter movie number: ")


    choice = int(choice)
    if choice == 0:
        print("Going to the main menu...")
        menu()

    elif 1 <= choice and choice <= len(titles):
        index = choice-1

        print("\n=====Movie Details=====")
        print(f"Title:      {titles[index]}")
        print(f"Year:       {Years[index]}")
        print(f"Genre:      {Genres[index]}")
        print(f"Director:   {Directors[index]}")
        print(f"Actors:     {Actors[index]}")

        #display existing comments
        cur.execute('SELECT User_ID, Comment_Text, Stars FROM Rating WHERE Movie_ID = ?', (movie_ids[index],))
        comments = cur.fetchall()
        print("\n=====User Comments=====")

        if comments:
            for info in comments:
                cur.execute('SELECT Username FROM User WHERE User_ID = ?',(info[0],))
                username=cur.fetchone()
                print(f"\n{username[0]}:      \nRating={info[2]} \nComment: {info[1]}")

        else:
            print("No comments available for this movie")

        #add a comment
        c = input("\nWould you like to add a comment? (type 'yes' or 'no'): ")
        if c.lower() == 'yes':
            rating(movie_ids[index])
        else:
            print("Going to menu...")
            time.sleep(1)
            menu()
    else:
        print("Error: Please choose a number between 1 and ",{len(titles)})
        Watchlist()


def rating(movie_id):
    print("\nRate a Movie")
    stars = int(input("Enter your rating (0-10): "))

    if 0 <= stars and stars<= 10:
        comment = input("Enter your comment: ")

        try:
            cur.execute('INSERT INTO Rating (User_ID, Movie_ID, Comment_Text, Stars) VALUES (?, ?, ?, ?)',
                        (user_id, movie_id, comment, stars))
            conn.commit()
            print("\ncomment saved")
            time.sleep(1)
            menu()

        except Exception:
            print("Error: Something went wrong while saving your comment")
            pass

    else:
        print("Error: rating must be between 0 and 10")
        rating(movie_id)



def Recommendations():
    print("\n Recommendations function")

    #variables
    i=0 #counter
    movie_info=[]

    #taking info from watchlist
    cur.execute(f'SELECT User_ID, Movie_ID FROM watchlist WHERE User_ID= ? ',(user_id,))
    watchlist = cur.fetchall()

    #taking info from rating
    cur.execute('SELECT User_ID, Movie_ID, Stars FROM Rating WHERE User_ID= ? ',(user_id,))
    rating= cur.fetchall()

    #taking info from user's ratings above 9 stars
    cur.execute('SELECT User_ID, Movie_ID, Stars FROM Rating WHERE Stars >= 9')
    high_rating = cur.fetchall()

    print("\n======RECOMMENDED======")
    if watchlist:  #recommendations based on watchlist
        for watchlist_items in watchlist:
            movie_id=watchlist_items[1]

            #url request
            url = f"{base_url}?apikey={apiKey}&I={movie_id}"    
            response = requests.get(url)
            data=response.json()

            if i!=len(watchlist):
                i=i+1
                print(f"{i} - {data['Title']}")
                movie_info.append(data)

        j=i-1


        
        x=0

        for movie in movie_info: # adding into Recommended table
            genre = movie.get('Genre', 'Unknown')  #Unknown if Genre is missing
            rating = movie.get('Ratings', [{'Value': 'N/A'}])[0].get('Value', 'N/A') #N/A if Value is missing
            cur.execute('SELECT * FROM Recommended WHERE User_ID = ? AND Movie_ID = ?', (user_id, movie['imdbID']))

            if cur.fetchone() is None:  #If no matching row is found, insert a new movie
                cur.execute('INSERT INTO Recommended (User_ID, Movie_ID, Title, Genre ,Stars) VALUES (?,?,?,?,?) ', 
                            (user_id,  movie['imdbID'], movie['Title'], genre, rating))
                conn.commit()
                x=x+1


    if high_rating:
        print("\nBest Movies (over 9 stars)")

        for movie in high_rating:
            movie_id = movie[1]
            url=f"{base_url}?apikey={apiKey}&i={movie_id}"
            response = requests.get(url)
            data=response.json()

            print(f"more recommmendations - {data['Title']}")


    print("\nend of recommmendations \nreturning to menu...")
    time.sleep(0.5)
    menu()


def Follow_Unfollow():
    print("\n Follower/Following function")
    print("What would you like to see:")
    print("1. Followers")
    print("2. Following")
    print("3. Follow a user (shows user list)")
    print("0. Menu")
    choice=input("Select an option (0-3): ")


    if choice=='1':
        Followers()
    elif choice=='2':
        Following()
    elif choice=='3':
        Follow()
    elif choice=='0':
        menu()
    else:
        Follow_Unfollow()
    

def Followers():
    cur.execute(f"SELECT * FROM Follower WHERE Follower_ID='{user_id}'") #who is following this user shd say admin and user
    followers=cur.fetchall() 
    #print("followers: ",followers)
    print(f'\nFollowers of {user}:')
    for x in followers:
        cur.execute(f"SELECT * FROM User WHERE User_ID='{x[1]}'")
        #print(x)
        followers_name=cur.fetchall() 
        for y in followers_name:
            print(y[1])

    time.sleep(1)
    Follow_Unfollow()


def Following():
    cur.execute(f"SELECT * FROM Follower WHERE Following_ID='{user_id}'") #who is this user following
    following=cur.fetchall() 
    #print("following: ",following)
    print(f"\nYou '{user}' are Following:")
    for x in following:
        cur.execute(f"SELECT * FROM User WHERE User_ID='{x[0]}'")
        following_name=cur.fetchall() 
        for y in following_name:
            print(y[1])
    
    time.sleep(1)
    Follow_Unfollow()

def Follow():
    cur.execute('SELECT Username FROM User')
    follow=cur.fetchall()   
    print("\nFollow: ") 
    for x in follow:
        print(x[0])
    adding=input("Who would you like to add (type in their username) ")
    

    cur.execute(f'SELECT User_ID FROM User WHERE Username="{adding}"')
    adding= cur.fetchone()

    if adding:
        #print('adding',adding[0])
        try: 
            cur.execute(f"INSERT INTO Follower (Follower_ID, Following_ID) VALUES ('{adding[0]}','{user_id}')")
            conn.commit()
            Following()
        except Exception:
            print("You are already follwing this user")
    else:
        print("The username does not exist. Please try again.")
        Follow()

    Follow_Unfollow()

# Main
Main()

