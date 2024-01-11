from flask import Flask, render_template, url_for, request, redirect, jsonify
from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId
import copy

TF_ENABLE_ONEDNN_OPTS = 0

app = Flask(__name__, static_url_path='/static')

import whisper
import spacy

model = whisper.load_model('base')
nlp = spacy.load('en_core_web_sm')

client = MongoClient('localhost', 27017)

#default is get, can explicitly declare other methods
@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST' and 'content' in request.form and 'degree' in request.form:
        content = request.form['content']
        degree = request.form['degree']
        timestamp = str(datetime.now())
        datetime_obj = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')
        formatted_date = datetime_obj.strftime('%B %d')
        formatted_date = datetime.now()
        
        todos.insert_one({'content': content, 'degree': degree, 'timestamp': formatted_date, 'new_old': "old"})
        return redirect(url_for('index'))
    
    current_date_and_time = str(datetime.now())
    
    all_todos = todos.find().sort('timestamp', -1)
    
    i_todos = []
    it5 = []
    un_todos = []
    unt5 = []
    i_num = 0
    un_num = 0

    for todo in all_todos:
        if todo['degree'] == 'important':
            i_todos.append(todo)
            i_num = i_num+1
            if i_num < 6:
                it5.append(todo)
        else:
            un_todos.append(todo)
            un_num = un_num + 1
            if un_num < 6:
                unt5.append(todo)
    if i_num < 6:
        i_num = 0
    else:
        i_num = 1
    if un_num < 6:
        un_num = 0
    else:
        un_num = 1

    return render_template('index.html', todos_important=i_todos, todos_unimportant=un_todos,
                           icount = i_num, uncount = un_num,
                           it5_in = it5, unt5_in = unt5)

@app.route("/past_wav", methods=['GET', 'POST'])
def wavsort():

    nt_c = 0
    top_3_new = []

    new_todos = []
    all_todos = todos.find()
    for todo in all_todos:
        if todo['new_old'] == 'new':
            new_todos.append(todo)
            nt_c = nt_c + 1
            if nt_c < 4:
                top_3_new.append(todo)
    if nt_c > 3:
        nt_c = 1
    else:
        nt_c = 0

    return render_template('wavfile.html', new_todos=new_todos, 
                           count = nt_c, top_3_new = top_3_new)
###########################################################################################

@app.route("/upload_wav", methods=['GET', 'POST'])
def wavmove():
    file = request.files['file']
    api_response = pass_to_api(file)
    #text = 'I need to go to the store tomorrow. His shirt is big and yellow. I think bob is ugly. I need to make an appointment'
    #text = api_response
    #splitted = text.split('. ')
    #proc = []
    #for i in range(len(splitted)):
    #    proc.append(splitted[i])

    for content_p in api_response:
        content = content_p
        degree = "important"
        timestamp = str(datetime.now())
        datetime_obj = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')
        formatted_date = datetime_obj.strftime('%B %d')
        formatted_date = datetime.now()
        todos.insert_one({'content': content, 'degree': degree, 'timestamp': formatted_date, 'new_old': "new"})

    return redirect(url_for('wavsort'))

##########################################################################
from use_model import use_model
def main_load_and_use_v2(my_list_in = []):
    final_list = []
    for text_in in my_list_in:
        predictions = use_model(text_in)
        if predictions > 0.8:
            final_list.append(text_in)
    return final_list
##########################################################################

def pass_to_api(file):
    file_path = 'temp.wav'
    file.save(file_path)
    # Use the uploaded file with your script
    result = model.transcribe(file_path, fp16=False)
    text = result['text']
    #the below line sends through the following, comment it out to send the actual text
    #from the audio clip (in line above)
    #text = 'I need to go to the store tomorrow. His shirt is big and yellow. I think bob is ugly. I need to make an appointment'
    splitted = text.split('. ')
    proc = []
    for i in range(len(splitted)):
        proc.append(splitted[i])
    return main_load_and_use_v2(proc)

"""
    if request.method == 'POST':
        content = request.form['content']
        degree = request.form['degree']
        timestamp = str(datetime.now())
        datetime_obj = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')
        formatted_date = datetime_obj.strftime('%B %d')
        formatted_date = datetime.now()
        
        todos.insert_one({'content': content, 'degree': degree, 'timestamp': formatted_date, 'new_old': "old"})
        return render_template('wavfile.html', pre_filled_text=proc)
""" 
    #return render_template('wavfile.html', pre_filled_text=proc)
###########################################################################################
@app.post("/wavfile/<id>/delete/")
def delete_wav(id): #delete function by targeting a todo document by its own id
    obj_id = ObjectId(id)
    todo = todos.find_one({'_id': obj_id})
    todos.insert_one({'content': todo['content'],
                       'degree': todo['degree'], 
                       'timestamp': todo['timestamp'], 
                       'new_old': "old"})
    todos.delete_one({"_id":ObjectId(id)}) 
    return redirect(url_for('wavsort')) 

@app.post("/wavfile/<id>/remove/")
def remove_wav(id): #delete function by targeting a todo document by its own id
    todos.delete_one({"_id":ObjectId(id)}) 
    return redirect(url_for('wavsort')) 

@app.route('/overflow1.html')
def overflow():
    return render_template('overflow1.html')

@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/schedule.html')
def schedule():
    return render_template('schedule.html')

@app.route('/wavfile.html')
def wavf():
    return redirect(url_for('wavsort')) 

@app.route('/index.html')
def index_home():
    return redirect(url_for('index')) 

#could use: app.route("/", methods['POST'])...
@app.post("/<id>/delete/")
def delete(id): #delete function by targeting a todo document by its own id
    todos.delete_one({"_id":ObjectId(id)}) #deleting the selected todo document by its converted id
    return redirect(url_for('index')) # again, redirecting you to the home page

#database, this is a mongodb database
db = client.flask_database
#creates a todos collection/table
todos = db.todos

if __name__ == "__main__":
    app.run(debug=True)