import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId


app = Flask(__name__)

app.config["MONGO_DBNAME"] = 'bake'
app.config["MONGO_URI"] = os.environ.get('MONGO_URI')


mongo = PyMongo(app)


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/recipe_db')
def recipe_db():
    return render_template("recipe-db.html",
                            recipe=mongo.db.recipe.find(),
                            recipe_type=mongo.db.recipe_type.find(),
                            recipe_diff=mongo.db.recipe_diff.find())


@app.route('/recipe_db<type_id>')
def recipe_db_type(type_id):
    recipes = mongo.db.recipe.find()
    the_type = mongo.db.recipe_type.find_one({"_id": ObjectId(type_id)})
    recipe_diffs = mongo.db.recipe_diff.find()
    return render_template("recipe-db.html",
                            rtype=the_type,
                            recipe=recipes,
                            recipe_diff=recipe_diffs)


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
    return redirect(url_for('recipe_db'))


@app.route('/update_recipe/<recipe_id>')
def update_recipe(recipe_id):
    the_recipe = mongo.db.recipe.find_one({"_id": ObjectId(recipe_id)})
    all_types = mongo.db.recipe_type.find()
    all_diffs = mongo.db.recipe_diff.find()
    return render_template('recipe-update.html',
                            recipe=the_recipe,
                            recipe_type=all_types,
                            recipe_diff=all_diffs)


@app.route('/send_update/<recipe_id>', methods=['POST'])
def send_update(recipe_id):
    recipe = mongo.db.recipe
    recipe.update( {'_id': ObjectId(recipe_id)},
        {
            'rec_name': request.form.get('rec_name'),
            'rec_aut': request.form.get('rec_aut'),
            'rec_type': request.form.get('rec_type'),
            'rec_diff': request.form.get('rec_diff'),
            'time_h': request.form.get('time_h'),
            'time_m': request.form.get('time_m'),
            'equip_name': request.form.get('equip_name'),
            'equip_aff': request.form.get('equip_aff'),
            'equip_desc': request.form.get('equip_desc'),
            'ing_name': request.form.get('ing_name'),
            'ing_amount': request.form.get('ing_amount'),
            'ing_unit': request.form.get('ing_unit'),
            'step_num': request.form.get('step_num'),
            'step_desc': request.form.get('step_desc'),
            'rec_pic': request.form.get('rec_pic')
        }
    )
    return redirect(url_for('recipe_db'))


@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    mongo.db.recipe.remove({'_id': ObjectId(recipe_id)})
    return redirect(url_for('recipe_db'))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
