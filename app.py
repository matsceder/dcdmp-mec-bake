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
                            recipe=mongo.db.recipe.find())


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
    recipe.update({'_id': ObjectId(recipe_id)}, {
        "rec_name": request.form.get('rec_name'),
        "rec_aut": request.form.get('rec_aut'),
        "rec_type": request.form.get('rec_type'),
        "rec_diff": request.form.get('rec_diff'),
        "rec_time_h": request.form.get('rec_time_h'),
        "rec_time_m": request.form.get('rec_time_m'),
        "rec_serve": request.form.get('rec_serve'),
        "rec_ing_n1": request.form.get('rec_ing_n1'),
        "rec_ing_a1": request.form.get('rec_ing_a1'),
        "rec_ing_u1": request.form.get('rec_ing_u1'),
        "rec_ing_n2": request.form.get('rec_ing_n2'),
        "rec_ing_a2": request.form.get('rec_ing_a2'),
        "rec_ing_u2": request.form.get('rec_ing_u2'),
        "rec_ing_n3": request.form.get('rec_ing_n3'),
        "rec_ing_a3": request.form.get('rec_ing_a3'),
        "rec_ing_u3": request.form.get('rec_ing_u3'),
        "rec_ing_n4": request.form.get('rec_ing_n4'),
        "rec_ing_a4": request.form.get('rec_ing_a4'),
        "rec_ing_u4": request.form.get('rec_ing_u4'),
        "rec_ing_n5": request.form.get('rec_ing_n5'),
        "rec_ing_a5": request.form.get('rec_ing_a5'),
        "rec_ing_u5": request.form.get('rec_ing_u5'),
        "rec_ing_n6": request.form.get('rec_ing_n6'),
        "rec_ing_a6": request.form.get('rec_ing_a6'),
        "rec_ing_u6": request.form.get('rec_ing_u6'),
        "rec_ing_n7": request.form.get('rec_ing_n7'),
        "rec_ing_a7": request.form.get('rec_ing_a7'),
        "rec_ing_u7": request.form.get('rec_ing_u7'),
        "rec_ing_n8": request.form.get('rec_ing_n8'),
        "rec_ing_a8": request.form.get('rec_ing_a8'),
        "rec_ing_u8": request.form.get('rec_ing_u8'),
        "rec_ing_n9": request.form.get('rec_ing_n9'),
        "rec_ing_a9": request.form.get('rec_ing_a9'),
        "rec_ing_u9": request.form.get('rec_ing_u9'),
        "rec_ing_n10": request.form.get('rec_ing_n10'),
        "rec_ing_a10": request.form.get('rec_ing_a10'),
        "rec_ing_u10": request.form.get('rec_ing_u10'),
        "rec_ing_n11": request.form.get('rec_ing_n11'),
        "rec_ing_a11": request.form.get('rec_ing_a11'),
        "rec_ing_u11": request.form.get('rec_ing_u11'),
        "rec_ing_n12": request.form.get('rec_ing_n12'),
        "rec_ing_a12": request.form.get('rec_ing_a12'),
        "rec_ing_u12": request.form.get('rec_ing_u12'),
        "rec_step1": request.form.get('rec_step1'),
        "rec_step2": request.form.get('rec_step2'),
        "rec_step3": request.form.get('rec_step3'),
        "rec_step4": request.form.get('rec_step4'),
        "rec_step5": request.form.get('rec_step5'),
        "rec_step6": request.form.get('rec_step6'),
        "rec_step7": request.form.get('rec_step7'),
        "rec_step8": request.form.get('rec_step8'),
        "rec_step9": request.form.get('rec_step9'),
        "rec_step10": request.form.get('rec_step10'),
        "rec_step11": request.form.get('rec_step11'),
        "rec_step12": request.form.get('rec_step12'),
        "rec_step13": request.form.get('rec_step13'),
        "rec_step14": request.form.get('rec_step14'),
        "rec_step15": request.form.get('rec_step15'),
        "rec_pic": request.form.get('rec_pic')
    })
    return redirect(url_for('recipe_db'))


@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    mongo.db.recipe.remove({'_id': ObjectId(recipe_id)})
    return redirect(url_for('recipe_db'))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
