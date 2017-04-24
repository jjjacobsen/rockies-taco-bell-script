import time, requests, bs4, smtplib

# using python3

# function that takes in a format of W10-5 or L7-6 and returns the rockies score
def rockies_score(wlscore):
    if(wlscore[0] == "W"):
        tmpstr = ""
        tmpint = 1
        while(wlscore[tmpint] != '-'):
            tmpstr += wlscore[tmpint]
            tmpint += 1
        return int(tmpstr)
    else:
        tmpstr = ""
        tmpint = 1
        while(wlscore[tmpint] != '-'):
            tmpint += 1
        for x in range(tmpint+1,len(wlscore)):
            tmpstr += wlscore[x]
        return int(tmpstr)

# given input of Mon, Apr 5 will return 1 if that was yesterday, 0 if not
def yesterdays_game(gameDate):
    # bs4 encodes as unicode so I have to cast to str here
    words = str(gameDate).split()
    gameday = int(words[2])
    currday = int(time.strftime("%d"))
    strmon = words[1]
    # handle end of month case
    if(currday == gameday+1):
        return 1
    else:
        if(currday == 1):
            # handle end of month case
            if(strmon == "Feb"):
                # 28 day month unless leap year
                intyear = time.strftime("%Y")
                if(intyear % 4 == 0):
                    # leap year
                    # this is not a perfect solution, there is a small error
                    # but the next time an exception happens is on the year 2100
                    if(gameday == 29):
                        return 1
                else:
                    if(gameday == 28):
                        return 1
            elif(strmon == "Apr" or strmon == "Jun" or strmon == "Sep" or strmon == "Nov"):
                # 30 day month
                if(gameday == 30):
                    return 1
            else:
                # 31 day month
                if(gameday == 31):
                    return 1
        return 0

# sends email to me, rockytacos44 is a throwaway email account so no worries
def send_email(score):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("rockytacos44@gmail.com", "default123")
    msg = "AYYY, TODAY YOU GET CHEAP TACOS"
    server.sendmail("rockytacos44@gmail.com", "jonah.jacobsen@colorado.edu", msg)
    server.quit()

def check():
    # create the "soup"
    result = requests.get("http://www.espn.com/mlb/team/schedule/_/name/col")
    result.raise_for_status()
    soup = bs4.BeautifulSoup(result.text, "lxml")

    # parse the raw HTML for the list entries with class=score and store in array
    scores = soup.find_all("li", class_="score")

    # run functions to get the score from rockies last game as int
    score = rockies_score(scores[-1].parent.getText())

    # run functions to get date of last rockies game
    date = scores[-1].parent.parent.parent.findChildren()[0].getText()

    # check to see if rockies played yesterday
    if(yesterdays_game(date)):
        # if score is higher than seven, then send me an email)
        if(score >= 7):
            send_email(score)

check()

# want to implement CRON scheduler so that I don't busy wait on CPU
