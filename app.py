# app.py

from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import os, re

app = Flask(__name__)
CORS(app, resources={r"/execute_query": {"origins": "http://localhost:3000"}})

# Your logic for parsing and executing queries here
class Relation:
    def __init__(self, name, attributes, tuples):
        self.name = name
        self.attributes = attributes
        self.tuples = tuples

def parse_relation(text):
    # Extracting relation name, attributes, and tuples using regex
    match = re.match(r'(\w+)\s*\(([^)]+)\)\s*=\s*{([^}]*)}', text)
    
    if match:
        name = match.group(1)
        attributes = [attr.strip() for attr in match.group(2).split(',')]
        
        # Parse tuples
        tuples_text = match.group(3).split()
        tuples = []
        for tuple_text in tuples_text:
            tuple_values = [value.strip() for value in tuple_text.split(',')]
            tuples.append(dict(zip(attributes, tuple_values)))

        return Relation(name, attributes, tuples)
    else:
        raise ValueError("Invalid relation text")
    
def parse_query(query):
    # Extracting operation, attributes, condition, and operands using regex
    match = re.match(r'(\w+)\(([^)]+)(?:\s*([<>]=?|!=)\s*([^)]+))?\)', query)
    print(query)
    print(match)
    if match:
        operation = match.group(1).lower()
        components = [comp.strip() for comp in match.group(2).split(',')]

        if len(components) > 1:
            # For operations with attributes and operands
            attributes = components[0]
            operands = components[1]
        else:
            # For operations without attributes (e.g., set operations)
            attributes = None
            operands = components[0]

        condition_operator = match.group(3)
        condition_value = match.group(4) if condition_operator else None

        return (operation, attributes, condition_operator, condition_value, operands)
    else:
        raise ValueError("Invalid query text")


def execute_query(operations, relations):
    operation, operand = operations
    relation = next((rel for rel in relations if rel.name == operand), None)

    if operation == "select":
        # Example: Select operation for Age > 30
        result = [tuple for tuple in relation.tuples if tuple["Age"] > 30]
        return result
    else:
        raise ValueError("Invalid operation")
    
@app.route('/')
def index():
    return render_template('/public/index/html')  # This should point to your main HTML file

@app.route('/execute_query', methods=['POST'])
def execute_query():
    # get the relation and query from webform
    relation_text = request.form['relation']
    query_text = request.form['query']
    
    # parsing and execution logic
    result=str(execute_query(parse_query(query_text), [parse_relation(relation_text)]))

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
    app.run(debug=False)