# app.py
from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from rule_engine import create_rule, evaluate_rule, Node
from bson.objectid import ObjectId

app = Flask(__name__)

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client['rule_engine_db']
rules_collection = db['rules']

@app.route("/")
def index():
    """ Renders the rule creation page. """
    return render_template('index.html')

@app.route('/create_rule', methods=['POST'])
def create_rule_endpoint():
    rule_string = request.json['rule_string']
    
    # Create the AST from the rule string
    ast_node = create_rule(rule_string)
    
    # Convert the AST Node to a dictionary for MongoDB storage
    rule_dict = ast_node.to_dict()

    # Store the rule dictionary into the MongoDB collection
    rule_id = rules_collection.insert_one({
        'rule_string': rule_string,
        'rule_ast': rule_dict
    }).inserted_id

    return jsonify({'message': 'Rule created', 'rule_id': str(rule_id)})

@app.route("/evaluate_rule/<rule_id>", methods=["POST"])
def evaluate_rule_endpoint(rule_id):
    """ API to evaluate a rule stored in MongoDB against user data """
    try:
        data = request.json
        user_data = data.get("user_data")
        
        if not user_data:
            return jsonify({"error": "User data is required"}), 400

        # Fetch rule from MongoDB
        rule = rules_collection.find_one({"_id": ObjectId(rule_id)})
        
        if not rule:
            return jsonify({"error": "Rule not found"}), 404

        # Recreate AST Node from MongoDB data
        ast_node = Node.from_dict(rule['rule_ast'])

        # Evaluate the rule against the user data
        result = evaluate_rule(ast_node, user_data)
        
        return jsonify({"result": result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
