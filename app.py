import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson import ObjectId


app = Flask(__name__)

app.config["MONGO_DBNAME"] = 'bake'
app.config["MONGO_URI"] = os.environ.get('MONGO_URI')


mongo = PyMongo(app)


@app.route('/')
@app.route('/get_recipes')
def get_recipes():
    return render_template("recipe-db.html",
                            recipe=mongo.db.recipe.find())


@app.route('/recipe_view')
def recipe_view():
    return render_template("recipe-view.html",
                            recipe=mongo.db.recipe.find())


@app.route('/recipe_new')
def recipe_new():
    return render_template("recipe-new.html",
                            recipe_type=mongo.db.recipe_type.find(),
                            recipe_diff=mongo.db.recipe_diff.find(),
                            recipe=mongo.db.recipe.find(),
                            ingredient_units=mongo.db.ingredient_units.find())


@app.route('/send_new', methods=['POST'])
def send_new():
    recipe = mongo.db.recipe
    recipe.insert_one(request.form.to_dict())
    return redirect(url_for('get_recipes'))


@app.route('/recipe_update')
def recipe_update():
    return render_template("recipe-update.html",
                            recipe_type=mongo.db.recipe_type.find(),
                            recipe_diff=mongo.db.recipe_diff.find(),
                            recipe=mongo.db.recipe.find(),
                            ingredient_units=mongo.db.ingredient_units.find())


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
