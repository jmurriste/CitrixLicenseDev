from flask import Flask
from flask_pymongo import PyMongo
from flask import render_template

app = Flask(__name__)
app.config["MONGO_DBNAME"] = "Citrix"
app.config["MONGO_URI"] = "mongodb://7.188.0.80:37777/Citrix"
mongo = PyMongo(app)




app.config['SECRET_KEY'] = 'mysecretkey'

@app.route("/add")
def add():
    user = mongo.db.users
    user.insert_one({'name':'jorge', 'code':'python'})
    user.insert_one({'name': 'martin', 'code': 'cc'})
    user.insert_one({'name': 'urriste', 'code': 'c'})
    user.insert_one({'name': 'Marcos', 'code': 'vb'})
    user.insert_one({'name': 'Maria', 'code': 'net'})
    return 'added user'

@app.route("/find")
def find():
    user = mongo.db.users
    cursor = user.find({})

    return cursor[1]['name']  +'       ' + cursor[2]['name']  +'       ' + cursor[3]['name']

@app.route("/findone")
def findone():
    user = mongo.db.users
    cursor = user.find_one({'name':'jorge'})

    return cursor['name'] +'       ' + cursor['code']



if __name__ == '__main__':
    app.run(debug=True)

