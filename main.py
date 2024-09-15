import sqlite3
import cv2
import os

Conn = sqlite3.connect("Level_DB.sqlite")
Cur = Conn.cursor()
Cur.execute("DROP TABLE IF EXISTS Levels")
Cur.execute("CREATE TABLE IF NOT EXISTS Levels (LevelName TEXT, Answer TEXT)")

path = r"C:\Users\Fixie\PycharmProjects\LevelResultGenerator\Levels"
image_files = [path+r"\\"+i for i in os.listdir(path)]
Dict = {"[255 255 255]": "empty",
        "[183 173 155]": "empty",
        "[225 110  90]": "sadness",
        "[ 53 242 251]": "happiness",
        "[0 0 0]": "fear"}

Names = list()
AnswerKey = list()
heightSquare = 8
widthSquare = 8
Count = 0
for i in image_files:

    LevelName = i.split("\\")[-1].split(".")[0]
    img = cv2.imread(i)

    width, height, _ = img.shape

    HeightSquareCount = 0
    Answer = ""
    for j in range(round((height / heightSquare)/2), height, round(height / heightSquare)):
        widthSquareCount = 0
        for k in range(round((width / widthSquare)/2), width, round(width / widthSquare)):
            pixel = img[j-1, k-1]
            Answer += Dict[f"{pixel}"] + " "
            widthSquareCount += 1
        HeightSquareCount += 1

    Answer = Answer.strip(" ")
    Names.append(LevelName)
    AnswerKey.append(Answer)

for i in range(len(AnswerKey)):
    Cur.execute("INSERT INTO Levels (LevelName, Answer) VALUES (?,?)", (Names[i], AnswerKey[i]))
Conn.commit()
Conn.close()