# RULE ENGINE WITH ABSTRACT SYNTAX TREE (AST)

OBJECTIVE
    The Rule Engine project allows users to create dynamic rules using custom conditions and evaluate those rules against user data. The rules are parsed and represented as Abstract Syntax Trees (AST), enabling flexible rule manipulation and evaluation. The system is built using Python's Flask framework for the backend, MongoDB for storing rules, and Postman or a front-end form for creating and testing rules.

FEATURES
    Create Custom Rules: Users can define rules involving conditions like age, department, salary, etc.
    Evaluate Rules: Rules can be evaluated against user data to check if conditions are met.
    MongoDB Storage: The rules are stored in MongoDB in a structured format (AST), enabling easy retrieval and evaluation.
    Error Handling: The system provides feedback for invalid rules or missing data.

## PREREQUISITES
Before running this project, ensure you have the following installed:
    Python 3.8+
    MongoDB (Running locally or using a cloud instance like MongoDB Atlas)
    Postman (Optional, for testing API requests)
    Git (For version control and pushing to GitHub)

### SETUP INSTRUCTIONS

1. Clone the Repository
git clone https://github.com/your-username/rule-engine-ast.git
cd rule-engine-ast
2. Create a Virtual Environment
python -m venv venv
source venv/bin/activate  # For Linux/Mac
venv\Scripts\activate      # For Windows
3. Install Dependencies
pip install -r requirements.txt
4. Ensure MongoDB is Running
Make sure MongoDB is running locally at mongodb://localhost:27017/.
5. Run the Flask Application
python app.py
The Flask server will start on http://127.0.0.1:5000.

#### API ENPOINTS
1. Create Rule
    Endpoint: /create_rule
    Method: POST
    Description: Creates a new rule from the provided rule string and stores it in MongoDB.
Request Payload:
{
  "rule_string": "(age > 30 AND department == 'Sales') OR (salary > 50000)"
}

Response:
{
  "message": "Rule created",
  "rule_id": "<MongoDB ObjectID>"
}

2. Evaluate Rule
    Endpoint: /evaluate_rule/<rule_id>
    Method: POST
    Description: Evaluates a specific rule stored in the database against the provided user data.
Request Payload:
{
  "user_data": {
    "age": 35,
    "department": "Sales",
    "salary": 60000
  }
}

Response:
{
  "result": true
}


EXAMPLE USAGE
To use this project, you can use Postman or similar tools to test the APIs.

1. Create a Rule: Send a POST request to http://localhost:5000/create_rule with the rule string in the request body.
2. Evaluate a Rule: Send a POST request to http://localhost:5000/evaluate_rule/<rule_id> with the user data in the request body.
For example, if the rule (age > 30 AND department == 'Sales') OR (salary > 50000) was created, you can evaluate it against the following user data:
{
  "user_data": {
    "age": 35,
    "department": "Marketing",
    "salary": 60000
  }
}
In this case, the rule would return true because the salary condition is satisfied.

##### DEVELOPMENT NOTES
    AST Representation: The project uses Python's ast module to parse rule strings into Abstract Syntax Trees (AST), allowing dynamic rule manipulation and efficient evaluation.
    MongoDB Structure: Rules are stored as a dictionary that represents the AST structure, allowing the system to recreate and evaluate rules directly from the database.
    Error Handling: The system includes checks for invalid rule formats and incorrect MongoDB ObjectIDs, ensuring that users receive helpful error messages when something goes wrong.

###### FUTURE IMPROVEMENTS
    Support for More Complex Rules: Expand the rule syntax to include more operators (like <=, >=, etc.).
    Improved Frontend: Build a more user-friendly UI for creating and testing rules, instead of relying on Postman.
    Support for Functions: Add support for user-defined functions within the rules.
