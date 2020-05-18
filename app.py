import os
from flask import Flask, render_template  # , redirect, request, url_for
from flask_pymongo import PyMongo
# from bson import ObjectId


app = Flask(__name__)

app.config["MONGO_DBNAME"] = 'bake'
app.config["MONGO_URI"] = os.environ.get('MONGO_URI')


mongo = PyMongo(app)


@app.route('/')
@app.route('/get_tasks')
def get_tasks():
    return render_template("recipe-db.html",
                            recipe=mongo.db.recipe.find())


@app.route('/new_recipe')
def new_recipe():
    return render_template("recipe-new.html",
                            recipe_type=mongo.db.recipe_type.find(),
                            recipe_diff=mongo.db.recipe_diff.find(),
                            recipe=mongo.db.recipe.find(),
                            ingredient_units=mongo.db.ingredient_units.find())


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
