from flask import Flask
from flask import render_template
from flask import jsonify
from flask import request

from dotenv import load_dotenv

from db import MindKG


load_dotenv('./.flaskenv')

app = Flask(__name__)

mindkg = MindKG("bolt://localhost:7687", "neo4j", "88888888")


@app.route('/')
def index():
    #newsList = models.News.get()

    #if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
    #    return jsonify(newsList)

    return render_template('index.html')


@app.route('/get-news', methods=['POST'])
def getNews():
    # print(request)
    # print(request.get_json())
    userID = request.get_json()
    mindkg.connect()
    newsList = mindkg.getNews(userID)
    mindkg.close()
    return jsonify(newsList)
    

@app.route('/read-news', methods=['POST'])
def readNews():
    jsonObj = request.get_json()
    print(jsonObj)
    newsID = jsonObj['newsID']
    userID = jsonObj['userID']
    time = jsonObj['time']
    mindkg.connect()
    result = mindkg.readNews(userID, newsID, time)
    mindkg.close()
    return result

@app.route('/get-users', methods=['POST'])
def getUsers():
    newsID = request.get_json()
    mindkg.connect()
    usersList = mindkg.getUsers(newsID)
    mindkg.close()
    return jsonify(usersList)
    

@app.route('/get-read-by-user', methods=['POST'])
def getReadByUser():
    userID = request.get_json()
    mindkg.connect()
    newsList = mindkg.getReadByUser(userID)
    mindkg.close()
    return jsonify(newsList)

@app.route('/create-user', methods=['POST'])
def createUser():
    userID = request.get_json()
    print(userID)
    mindkg.connect()
    result = mindkg.createUser(userID)
    mindkg.close()
    return result

@app.route('/get-random-news', methods=['POST'])
def getRandomNews():
    mindkg.connect()
    newsList = mindkg.getRandomNews()
    mindkg.close()
    return jsonify(newsList)
    


if __name__ == '__main__':
    app.run()