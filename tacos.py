from __future__ import print_function
import time,requests, bs4, smtplib, schedule

# using python

# function that takes in a format of W10-5 or L7-6 and returns the correct score
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

# this will convert a format of Wed, Apr 12 into 04/12/2017
def date_format(textDate):
    strday = ""
    for x in range (9,len(textDate)):
        strday += textDate[x]
    if(len(strday) == 1):
        strday = "0" + strday
    strmon = ""
    for x in range(5,8):
        strmon += textDate[x]
    if(strmon == "Jan"):
        strmon = "01"
    elif(strmon == "Feb"):
        strmon = "02"
    elif(strmon == "Mar"):
        strmon = "03"
    elif(strmon == "Apr"):
        strmon = "04"
    elif(strmon == "May"):
        strmon = "05"
    elif(strmon == "Jun"):
        strmon = "06"
    elif(strmon == "Jul"):
        strmon = "07"
    elif(strmon == "Aug"):
        strmon = "08"
    elif(strmon == "Sep"):
        strmon = "09"
    elif(strmon == "Oct"):
        strmon = "10"
    elif(strmon == "Nov"):
        strmon = "11"
    elif(strmon == "Dec"):
        strmon = "12"
    stryear = time.strftime("%Y")
    return strmon + '/' + strday + '/' + stryear

# will take in a str 04/14/2017 and see if that was yesterdays date
def yesterdays_game(textDate):
    day = int(textDate[3] + textDate[4])
    if(day == 1):
        # gotta check last day of last month...
        # do this by an if statement with many or clauses
        pass
    else:
        one = ""
        two = ""
        nextDay = day+1
        tmp = str(nextDay)
        for x in range(0, 2):
            one += textDate[x]
        for x in range(6,len(textDate)):
            two += textDate[x]
        tmp = one + '/' + tmp + '/' + two
        if(tmp == time.strftime("%m/%d/%Y")):
            return 1
        else:
            return 0

def check():
    # create the "soup"
    result = requests.get("http://www.espn.com/mlb/team/schedule/_/name/col")
    result.raise_for_status()
    soup = bs4.BeautifulSoup(result.text, "lxml")

    # parse the raw HTML for the list entries with class=score and store in array
    scores = soup.find_all("li", class_="score")

    # loop through scores and build the array of W/L + score and dates
    datearr = []
    wlscorearr = []
    for score in scores:
        wlscorearr.append(score.parent.getText())
        tmp = score.parent.parent.parent.findChildren()
        datearr.append(tmp[0].getText())

    # checks if the last game played was yesterday
    if(yesterdays_game(date_format(datearr[-1]))):
        # checks if the rockies scored 7 or more points
        if(rockies_score(wlscorearr[-1]) >= 7):
            # send email
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login("rockytacos44@gmail.com", "default123")
            msg = "AYYY, YOU JUST GOT CHEAP TACOS"
            server.sendmail("rockytacos44@gmail.com", "jonah.jacobsen@colorado.edu", msg)
            server.quit()
        else:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login("rockytacos44@gmail.com", "default123")
            msg = "the rockies only scored " + str(rockies_score(wlscorearr[-1])) + " points"
            server.sendmail("rockytacos44@gmail.com", "jonah.jacobsen@colorado.edu", msg)
            server.quit()

check()

schedule.every().day.at("10:00").do(check)

while(1):
    schedule.run_pending()
    time.sleep(1)
