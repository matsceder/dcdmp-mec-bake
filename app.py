import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from helper_folder.helper_file import clean_update


app = Flask(__name__)

app.config["MONGO_DBNAME"] = 'bake'
app.config["MONGO_URI"] = os.environ.get('MONGO_URI')


mongo = PyMongo(app)


# Page index/home template
@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


# Database template with all recipes displayed
@app.route('/recipe_db/0/0')
def recipe_db():
    return render_template("recipe-db.html",
                           recipe=mongo.db.recipe.find(),
                           recipe_type=mongo.db.recipe_type.find(),
                           recipe_diff=mongo.db.recipe_diff.find())


# Database template with specified recipes displayed
""" Here I could have used a solution like find({'rec_type': 'type_r'})
and pass in only recipes with specified type into the route, making less
mess. Because right now I've worked with a lot of for loops using Jinja2,
and even though it felt like I learned something from that too, it just
is not as practical and makes it harder for someone else to read and
work with the code. """


@app.route('/recipe_db/<type_r>/<diff_r>')
def recipe_db_t_d(type_r, diff_r):
    recipes = mongo.db.recipe.find()
    the_type = mongo.db.recipe_type.find_one({"rec_type": type_r})
    recipe_types = mongo.db.recipe_type.find()
    the_diff = mongo.db.recipe_diff.find_one({"rec_diff": diff_r})
    recipe_diffs = mongo.db.recipe_diff.find()
    return render_template("recipe-db.html",
                           recipe=recipes,
                           rtype=the_type,
                           recipe_type=recipe_types,
                           rdiff=the_diff,
                           recipe_diff=recipe_diffs)


# Template for viewing specific recipe
@app.route('/recipe_view/<recipe_id>')
def recipe_view(recipe_id):
    the_recipe = mongo.db.recipe.find_one({"_id": ObjectId(recipe_id)})
    return render_template('recipe-view.html',
                           recipe=the_recipe)


# Template for making a new recipe
@app.route('/recipe_new')
def recipe_new():
    return render_template("recipe-new.html",
                           recipe_type=mongo.db.recipe_type.find(),
                           recipe_diff=mongo.db.recipe_diff.find(),
                           recipe=mongo.db.recipe.find())


# Sending in form for new recipe
@app.route('/send_new', methods=['POST'])
def send_new():
    recipe = mongo.db.recipe
    recipe.insert_one(request.form.to_dict())
    return redirect(url_for('recipe_db'))


# Recipe update template
@app.route('/update_recipe/<recipe_id>')
def update_recipe(recipe_id):
    the_recipe = mongo.db.recipe.find_one({"_id": ObjectId(recipe_id)})
    all_types = mongo.db.recipe_type.find()
    all_diffs = mongo.db.recipe_diff.find()
    ing_units = mongo.db.ingredient_units.find()
    return render_template('recipe-update.html',
                           recipe=the_recipe,
                           recipe_type=all_types,
                           recipe_diff=all_diffs,
                           all_units=ing_units)


# Posting update function
@app.route('/send_update/<recipe_id>', methods=['POST'])
def send_update(recipe_id):
    recipe = mongo.db.recipe
    clean_data = clean_update(request.form)
    recipe.update({'_id': ObjectId(recipe_id)}, clean_data)
    return redirect(url_for('recipe_db'))


# Deleting recipe function
@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    mongo.db.recipe.remove({'_id': ObjectId(recipe_id)})
    return redirect(url_for('recipe_db'))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=False)
