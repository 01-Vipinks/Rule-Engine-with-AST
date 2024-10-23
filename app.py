# app.py
from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from rule_engine import create_rule, evaluate_rule, Node, combine_rules
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
    try:
        # Safely get the 'rule_string' from the request body
        rule_string = request.json.get('rule_string')
        
        # If 'rule_string' is not provided, return an error
        if not rule_string:
            return jsonify({'error': 'rule_string is required in the request body'}), 400

        # Create the AST from the rule string (with proper exception handling)
        try:
            ast_node = create_rule(rule_string)
        except Exception as e:
            return jsonify({'error': f"Failed to create AST from rule string: {str(e)}"}), 400

        # Convert the AST Node to a dictionary for MongoDB storage
        rule_dict = ast_node.to_dict()

        # Store the rule dictionary into the MongoDB collection
        rule_id = rules_collection.insert_one({
            'rule_string': rule_string,
            'rule_ast': rule_dict
        }).inserted_id

        # Return a success response with the rule ID
        return jsonify({'message': 'Rule created', 'rule_id': str(rule_id)})

    except Exception as e:
        # Catch all other errors and return a 500 Internal Server Error response
        return jsonify({'error': f"An unexpected error occurred: {str(e)}"}), 500


@app.route('/combine_rules', methods=['POST'])
def combine_rules_endpoint():
    """
    API to combine multiple rules.
    The request body should contain a list of rule strings and an optional operator ('AND' or 'OR').
    """
    data = request.json
    rule_strings = data.get('rule_strings')
    operator = data.get('operator', 'AND')  # Default to 'AND' if no operator is provided

    if not rule_strings or len(rule_strings) < 2:
        return jsonify({"error": "At least two rules are required for combination"}), 400

    # Create individual ASTs for each rule
    ast_nodes = []
    for rule_string in rule_strings:
        ast_node = create_rule(rule_string)
        ast_nodes.append(ast_node)
    
    # Combine the ASTs
    combined_ast = combine_rules(ast_nodes, operator)

    # Convert combined AST to a dictionary for MongoDB storage
    combined_ast_dict = combined_ast.to_dict()

    # Store the combined rule in MongoDB under 'rule_ast' to keep consistency
    rule_id = rules_collection.insert_one({
        'rule_strings': rule_strings,
        'rule_ast': combined_ast_dict,  # Store under 'rule_ast' for consistency
        'operator': operator
    }).inserted_id

    return jsonify({'message': 'Rules combined', 'combined_rule_id': str(rule_id)})

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
        ast_node = Node.from_dict(rule['rule_ast'])  # Expecting 'rule_ast' key

        # Evaluate the rule against the user data
        result = evaluate_rule(ast_node, user_data)
        
        return jsonify({"result": result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
