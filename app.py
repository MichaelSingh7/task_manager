import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId


app = Flask(__name__)

app.config["MONGO_DBNAME"] = 'task_manager'
app.config["MONGO_URI"] = 'mongodb+srv://root:toor@myfirstcluster-f87ek.mongodb.net/task_manager?retryWrites=true&w=majority'

mongo = PyMongo(app)


@app.route('/')
@app.route('/get_tasks')
def get_tasks():
    return render_template("tasks.html", tasks=mongo.db.tasks.find())


@app.route('/add_task')
def add_task():
    return render_template('addtask.html',
                           catagories=mongo.db.catagories.find())


@app.route('/insert_task', methods=['POST'])
def insert_task():
    tasks = mongo.db.tasks
    tasks.insert_one(request.form.to_dict())
    return redirect(url_for('get_tasks'))


@app.route('/edit_task/<task_id>')
def edit_task(task_id):
    the_task = mongo.db.tasks.find_one({"_id": ObjectId(task_id)})
    all_categories = mongo.db.catagories.find()
    return render_template('edittask.html', task=the_task,
                           catagories=all_categories)


@app.route('/update_task/<task_id>', methods=["POST"])
def update_task(task_id):
    tasks = mongo.db.tasks
    tasks.update({'_id': ObjectId(task_id)},
                 {
                   'task_name': request.form.get('task_name'),
                 'catagory_name': request.form.get('catagory_name'),
                 'task_description': request.form.get('task_description'),
                   'due date': request.form.get('due_date'),
                   'is_urgent': request.form.get('is_urgent')
                 })
    return redirect(url_for('get_tasks'))


@app.route('/delete_task/<task_id>')
def delete_task(task_id):
    mongo.db.tasks.remove({'_id': ObjectId(task_id)})
    return redirect(url_for('get_tasks'))


@app.route('/get_catagories')
def get_catagories():
    return render_template('catagories.html',
                           catagories=mongo.db.catagories.find())


@app.route('/delete_catagory/<catagory_id>')
def delete_catagory(catagory_id):
    mongo.db.catagories.remove({'_id': ObjectId(catagory_id)})
    return redirect(url_for('get_catagories'))


@app.route('/update_catagory/<catagory_id>', methods=['POST'])
def update_catagory(catagory_id):
    mongo.db.catagories.update(
        {'_id': ObjectId(catagory_id)},
        {'catagory_name': request.form.get('catagory_name')})
    return redirect(url_for('get_catagories'))


@app.route('/insert_catagory', methods=['POST'])
def insert_category():
    catagory_doc = {'catagory_name': request.form.get('catagory_name')}
    mongo.db.catagories.insert_one(catagory_doc)
    return redirect(url_for('get_catagories'))


@app.route('/add_catagory')
def add_catagory():
    return render_template('addcatagory.html')


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
