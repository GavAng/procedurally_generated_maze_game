import random
from flask import Flask, render_template, request, redirect, url_for

import mazeGenerator
  
app = Flask(__name__)





#adjusts string time from webpage into numerical value
def timeCorrector(time):

    time = time.replace(" ","")

    return float(time)





#adds an entry to the leaderboard text file
def leaderboardEntryAdder(username,time,moves):

    entry = f"{username},{time},{moves}\n"


    with open("static/leaderboard.txt","a") as appendFile:

        appendFile.write(entry)





#reads all values from leaderboard text file
def leaderboardReader():

    try:
        leaderboard = []


        with open("static/leaderboard.txt","r") as readFile:

            for line in readFile:

                line = line.strip()
                line = line.split(",")

                leaderboardEntry = {
                    "username": line[0],
                    "time": line[1],
                    "moves": line[2]
                }

                leaderboard.append(leaderboardEntry)


        if len(leaderboard) == 0:
            raise ValueError


    except:
        leaderboard = [{
            "username":"No entries",
            "time":"",
            "moves":""
        }]


    return leaderboard





#bubble sorts leaderboard by fastest time first
def leaderboardSort(leaderboard):

    sortLength = len(leaderboard)
    swapped = True


    while swapped == True and sortLength > 1:

        swapped = False


        for index in range(sortLength - 1):

            if float(leaderboard[index]["time"]) > float(leaderboard[index + 1]["time"]):

                temporary = leaderboard[index]
                leaderboard[index] = leaderboard[index + 1]
                leaderboard[index + 1] = temporary

                swapped = True

        sortLength -= 1
        

    return leaderboard





#gets just the names from the leaderboard
def takenUsernames():

    leaderboard = leaderboardReader()
    takenUsernames = []


    for entry in leaderboard:

        takenUsernames.append(entry["username"])


    return (",").join(takenUsernames)





@app.route('/', methods = ["POST","GET"])
@app.route('/index', methods = ["POST","GET"])
@app.route('/home', methods = ["POST","GET"])
def home():

    if request.method == 'POST':

        if request.form["saveResults"] == "yes":

            username = request.form["username"]
            finalTime = request.form["finalTime"]
            finalMoves = request.form["finalMoves"]

            leaderboardEntryAdder(username,finalTime,finalMoves)


    return render_template("homePage.html")





@app.route('/game', methods=["POST","GET"])
def renderGame():

    if request.method == "POST": #if a game has just been played
        
        gameForm = request.form

        timeTaken = timeCorrector(gameForm["time"])
        totalTime = float(gameForm["totalTime"])
        totalTime += timeTaken

        totalMoves = int(gameForm["movementCount"])
        
        gamesPlayedCount = int(gameForm["levelNumber"])
        
    else:
        gamesPlayedCount = 0
        totalTime = 0
        totalMoves = 0


    if gamesPlayedCount < 5:

        finalMaze = mazeGenerator.mazeRandomizer()
        routesList = mazeGenerator.routesListMaker(finalMaze)
        randomCorner = random.choice(finalMaze.getCorners())

        return render_template("mazeDisplay.html", directions=routesList, finishPosition=randomCorner, levelNumber=gamesPlayedCount + 1, totalTime=totalTime, totalMoves=totalMoves)
    else:
        return redirect(url_for('finishForm', time=round(float(totalTime),1), moves=totalMoves))





@app.route('/finish?<time>&<moves>')
def finishForm(time, moves, takenUsernames=takenUsernames):
    
    return render_template("finishForm.html", finalTime=time, finalMoves=moves, takenUsernames=takenUsernames())





@app.route('/leaderboard')
def leaderboard(leaderboardReader=leaderboardReader, leaderboardSort=leaderboardSort):

    leaderboard = leaderboardReader()
    leaderboard = leaderboardSort(leaderboard)

    
    return render_template("leaderboard.html", leaderboard=leaderboard)


    


@app.route('/test')
def test():
    return redirect(url_for('finishForm', time=28.6, moves=153))



if __name__ == "__main__":  
    app.run(host="localhost", port=8080, debug=True)