import requests, bs4

# using python3

# create the "soup"
result = requests.get("http://www.espn.com/mlb/team/schedule/_/name/col")
result.raise_for_status()
soup = bs4.BeautifulSoup(result.text, "lxml")

# parse the raw HTML for the list entries with class score and store in array
scores = soup.find_all("li", class_="score")

# loop through and get important text data for each game
for score in scores:
    tmpstr = score.getText()
    print(tmpstr)

'''
TO DO:
1. figure out from the scores which one is the rockies
2. make sure this code will update as espn updates their page
3. on any game where the rockies have 7 or more points check the date
4. if the game date is yesterday then send an email notifying me
5. somehow setup script to execute every morning at 8:00a.m.
6. ???
7. profit (tacos)
'''
