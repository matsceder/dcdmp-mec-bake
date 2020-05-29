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
    rec_name = the_recipe["rec_name"]
    the_ing = mongo.db.ingredients.find_one({"rec_name": rec_name})
    return render_template('recipe-view.html',
                            recipe=the_recipe,
                            r_name=rec_name,
                            r_ing=the_ing)


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
    recipe.insert_one(
        {
            "rec_name": request.form['rec_name'],
            "rec_aut": request.form['rec_aut'],
            "rec_type": request.form['rec_type'],
            "rec_diff": request.form['rec_diff'],
            "rec_time": {"rec_time_h": request.form['time_h'], "rec_time_m": request.form['time_m']},
            "rec_pic": request.form['rec_pic'],
            "rec_ing": {"i1": request.form['in1'], "i2": request.form['in2'], "i3": request.form['in3'], "i4": request.form['in4'], "i5": request.form['in5'], "i6": request.form['in6'], "i7": request.form['in7'], "i8": request.form['in8'], "i9": request.form['in9'], "i10": request.form['in10'], "i11": request.form['in11'], "i12": request.form['in12']},
            "amount": {"a1": request.form['ia1'], "a2": request.form['ia2'], "a3": request.form['ia3'], "a4": request.form['ia4'], "a5": request.form['ia5'], "a6": request.form['ia6'], "a7": request.form['ia7'], "a8": request.form['ia8'], "a9": request.form['ia9'], "a10": request.form['ia10'], "a11": request.form['ia11'], "a12": request.form['ia12']},
            "unit": { "u1": request.form['iu1'], "u2": request.form['iu2'], "u3": request.form['iu3'], "u4": request.form['iu4'], "u5": request.form['iu5'], "u6": request.form['iu6'], "u7": request.form['iu7'], "u8": request.form['iu8'], "u9": request.form['iu9'], "u10": request.form['iu10'], "u11": request.form['iu11'], "u12": request.form['iu12']},
            "step": {"s1": request.form['sn1'], "s2": request.form['sn2'], "s3": request.form['sn3'], "s4": request.form['sn4'], "s5": request.form['sn5'], "s6": request.form['sn6'], "s7": request.form['sn7'], "s8": request.form['sn8'], "s9": request.form['sn9'], "s10": request.form['sn10'], "s11": request.form['sn11'], "s12": request.form['sn12']}
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
