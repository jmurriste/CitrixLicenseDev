import os
from flask import Flask
from flask_pymongo import PyMongo




app = Flask(__name__)
app.config["MONGO_DBNAME"] = "Citrix"
app.config["MONGO_URI"] = "mongodb://7.188.0.80:37777/Citrix"
mongo = PyMongo(app)

app.config['SECRET_KEY'] = 'mysecretkey'




# NOTE! These imports need to come after you've defined db, otherwise you will
# get errors in your models.py files.
## Grab the blueprints from the other views.py files for each "app"
from CitrixSDW.appliances.views import appliances_blueprint

app.register_blueprint(appliances_blueprint,url_prefix="/appliances")

