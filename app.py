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


# DB INDEX
@app.route('/recipe_db/0/0')
def recipe_db():
    return render_template("recipe-db.html",
                            recipe=mongo.db.recipe.find(),
                            times=mongo.db.recipe.rec_time.find(),
                            recipe_type=mongo.db.recipe_type.find(),
                            recipe_diff=mongo.db.recipe_diff.find())


# TYPE AND DIFF DEFINED
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


@app.route('/recipe_view/<recipe_id>')
def recipe_view(recipe_id):
    the_recipe = mongo.db.recipe.find_one({"_id": ObjectId(recipe_id)})
    rec_ing = the_recipe["rec_ing"]
    ing_names = the_recipe["rec_ing"]["ing_name"]
    all_types = mongo.db.recipe_type.find()
    all_diffs = mongo.db.recipe_diff.find()
    return render_template('recipe-view.html',
                            recipe=the_recipe,
                            recipe_type=all_types,
                            recipe_diff=all_diffs,
                            all_ing=rec_ing,
                            ing_name=ing_names)


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
    steps = mongo.db.steps
    ingredients = mongo.db.ingredients
    recipe.insert_one(
        { "rec_name" : request.form['rec_name'],
        "rec_aut" : request.form['rec_aut'],
        "rec_type" : request.form['rec_type'],
        "rec_diff" : request.form['rec_diff'],
        "rec_time_h" : request.form['time_h'],
        "rec_time_m" : request.form['ing_amount'],
        "rec_pic" : request.form['rec_pic']
        }
    )
    steps.insert_one(
        { "rec_name" : request.form['rec_name'],
        "rec_step_1" : request.form['rec_step_1'],
        "rec_step_2" : request.form['rec_step_2'],
        "rec_step_3" : request.form['rec_step_3'],
        "rec_step_4" : request.form['rec_step_4'],
        "rec_step_5" : request.form['rec_step_5'],
        "rec_step_6" : request.form['rec_step_6'],
        "rec_step_7" : request.form['rec_step_7'],
        "rec_step_8" : request.form['rec_step_8'],
        "rec_step_9" : request.form['rec_step_9'],
        "rec_step_10" : request.form['rec_step_10'],
        "rec_step_11" : request.form['rec_step_11'],
        "rec_step_12" : request.form['rec_step_12']
        }
    )
    ingredients.insert_one(
        { "rec_name" : request.form['rec_name'],
        "rec_ing_1" : request.form['rec_ing_1'],
        "rec_ing_2" : request.form['rec_ing_2'],
        "rec_ing_3" : request.form['rec_ing_3'],
        "rec_ing_4" : request.form['rec_ing_4'],
        "rec_ing_5" : request.form['rec_ing_5'],
        "rec_ing_6" : request.form['rec_ing_6'],
        "rec_ing_7" : request.form['rec_ing_7'],
        "rec_ing_8" : request.form['rec_ing_8'],
        "rec_ing_9" : request.form['rec_ing_9'],
        "rec_ing_10" : request.form['rec_ing_10'],
        "rec_ing_11" : request.form['rec_ing_11'],
        "rec_ing_12" : request.form['rec_ing_12']
        }
    )
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
