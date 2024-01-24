# app.py

from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import os

from relational import relation, parser, rtypes
from relational import maintenance

app = Flask(__name__)
CORS(app, resources={r"/execute_query": {"origins": "http://localhost:3000"}})
ui = maintenance.UserInterface()

def divide_chunks(l, n):  
    # looping till length l 
    for i in range(0, len(l), n):  
        yield l[i:i + n] 

def replacements(query: str) -> str:
    '''This function replaces ascii easy operators with the correct ones'''
    rules = (
        ('join', parser.JOIN),
        ('left_join', parser.JOIN_LEFT),
        ('right_join', parser.JOIN_RIGHT),
        ('full_join', parser.JOIN_FULL),
        ('project', parser.PROJECTION),
        ('select', parser.SELECTION),
        ('rename', parser.RENAME),
    )
    for asciiop, op in rules:
        query = query.replace(asciiop, op)
    return query

def create_relation(input):
    placeholder = -1
    for i in range(0, len(input)):
        if input[i]=='}':
            title = input[placeholder+1]
            name = title[0:title.index(' ')]
            attributes = title[title.index('(')+1:title.index(')')]
            attributes = attributes.split(', ')
            temp_relation = ", ".join(input[placeholder+2:i])
            temp_relation = temp_relation.split(', ')
            temp_relation = list(divide_chunks(temp_relation, len(attributes)))
            placeholder = i
            ui.set_relation(name, relation.Relation.create_from(attributes, temp_relation))
    
@app.route('/')
def index():
    return render_template('/public/index/html')  # This should point to your main HTML file

@app.route('/execute_query', methods=['POST'])
async def execute_query():
    # get the relation and query from webform
    relation_text = request.form['relation']
    query_text = request.form['query']
    query_text = replacements(query_text)
    input = relation_text.split('\n')
    create_relation(input)
    
    pyquery = parser.parse(query_text)
    result = pyquery(ui.relations)
    result = result.pretty_string(tty=True)
    # return JSON result
    return jsonify(result), 200, {'Access-Control-Allow-Origin': 'http://localhost:3000'}

# Serve React static files
@app.route('/src/App.js')
def serve_static(filename):
    root_dir = os.path.dirname(os.getcwd())
    return send_from_directory(os.path.join(root_dir, 'ease', 'build', 'static'), filename)

# Serve React index.html
@app.route('/public/index.html')
def serve_index(path):
    root_dir = os.path.dirname(os.getcwd())
    return send_from_directory(os.path.join(root_dir, 'ease', 'build'), 'index.html')

if __name__ == '__main__':
    app.run(debug=True)