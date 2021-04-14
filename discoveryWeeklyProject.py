import json
import requests
from secrets import spotify_user_id, spotify_token, discover_playlist_id, refresh_token, base  # gets our token/usernmae from secrets file
from datetime import date


class discoverySongs:

    def __init__(self):
        self.user_id = spotify_user_id
        self.spotify_token = ""
        self.discover_weekly_id = discover_playlist_id
        self.tracks = ""


    # adds weekly discovery songs to a new playlists
    def find_songs(self):
        self.refresh()
        print('Finding Songs in discover weekly: ')
        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(discover_playlist_id)

        response = requests.get(query, headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(self.spotify_token)})

        response_json = response.json()
        #print(response_json)
        # print(response)

        for i in response_json["items"]:
            self.tracks += (i["track"]["uri"] + ",")
            
        self.tracks = self.tracks[:-1] # removes last comma
        print(self.tracks)
        self.add_to_playlist()


    # creates a new discovery playlist to hold our songs
    def create_playlist(self):

        print("Creating Playlist")
        today = date.today()
        todayFormat = today.strftime("%d/%m/%Y")
        query = "https://api.spotify.com/v1/users/{}/playlists".format(spotify_user_id)

        request_body = json.dumps({"name": todayFormat + " Discover weekly", "description": "Discover weekly spotify project ", "public" : True})

        response = requests.post(query, data=request_body, headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(self.spotify_token)})

        response_json = response.json()
        print(response)
        return response_json["id"]


    # adds songs to our discovery playlist
    def add_to_playlist(self):
        print("Adding to playlist")

        new_playlist_id = self.create_playlist()
        query = "https://api.spotify.com/v1/playlists/{}/tracks?uris={}".format(new_playlist_id,self.tracks)
        response = requests.post(query, headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(self.spotify_token)})

        print(response.json)


    # uses the "discovery holder" playlist we have created to add the songs into there
    def add_to_existing_playlist(self):
        self.refresh()
        print('Adding Songs to Discovery Holder: ')
        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(discover_playlist_id)

        response = requests.get(query, headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(self.spotify_token)})

        response_json = response.json()
        #print(response_json)
        # print(response)

        for i in response_json["items"]:
            self.tracks += (i["track"]["uri"] + ",")
            
        self.tracks = self.tracks[:-1] # removes last comma
        print(self.tracks)
        self.add_songs_holder()


    # adds our songs to our discovery holder playlist
    def add_songs_holder(self):
        playlist_id = "02cuESHslpgVWCIZMQ1FLb"
        print("Adding to playlist")
        query = "https://api.spotify.com/v1/playlists/{}/tracks?uris={}".format(playlist_id,self.tracks)
        response = requests.post(query, headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(self.spotify_token)})

        print(response.json)


    # retrieves a new api token as the api token expires
    def refresh(self):
        print("get new token")

        query = "https://accounts.spotify.com/api/token"
        response = requests.post(query, data={"grant_type": "refresh_token", "refresh_token": refresh_token}, headers={"Authorization": "Basic " + base})
        response = response.json()
        self.spotify_token = response["access_token"]



    # deletes duplicate songs in the playlist, useful for incase the program runs twice and adds duplicates
    def deleteDups(self):
        self.refresh()
        playlist_id = "02cuESHslpgVWCIZMQ1FLb"

        # retrieves our main playlist songs
        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(playlist_id)

        response_main_playlist = requests.get(query, headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(self.spotify_token)})

        response_main = response_main_playlist.json()

        songs_in_list = []
        for i in response_main["items"]:
            songs_in_list.append(str(i["track"]["uri"]))
        
        # retrieves songs in our discovery weekly playlist
        query_disc = "https://api.spotify.com/v1/playlists/{}/tracks".format(discover_playlist_id)

        response_disc = requests.get(query_disc, headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(self.spotify_token)})

        response_disc = response_disc.json()

        songs_in_disc = []
        for i in response_disc["items"]:
            songs_in_disc.append(str(i["track"]["uri"]))

        del_list = []
        count = 0
        # compares the songs to find duplicates
        for j in songs_in_disc:
            for n in songs_in_list:
                if(j == n):
                    del_list.append(j)
                    count += 1

        #print(del_list)
        # adds duplicates to an array
        final_del = []
        for i in del_list:
            value = {"uri":str(i)}
            final_del.append(value)
        print(final_del)

        #removes the duplicates
        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(playlist_id)
        response = requests.delete(query, headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(self.spotify_token)}, data={"tracks": final_del})  
        print(response)



def main(): 
    choice = input("Do you want to add weekly discovery to 'existing' holder or a 'new' playlist: ") # asks user if to create a new playlist or use existing
    a = discoverySongs()
    if(choice == 'new'):
        a.find_songs()
    elif(choice == 'existing'):
        a.add_to_existing_playlist()
        
main()
