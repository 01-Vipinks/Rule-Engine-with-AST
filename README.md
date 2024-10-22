# RULE ENGINE WITH ABSTRACT SYNTAX TREE (AST)

OBJECTIVE

The Rule Engine project allows users to create dynamic rules using custom conditions and evaluate those rules against user data. The rules are parsed and represented as Abstract Syntax Trees (AST), enabling flexible rule manipulation and evaluation. The system is built using Python's Flask framework for the backend, MongoDB for storing rules, and Postman or a front-end form for creating and testing rules.

FEATURES

* Create Custom Rules: Users can define rules involving conditions like age, department, salary, etc.
* Evaluate Rules: Rules can be evaluated against user data to check if conditions are met.
* MongoDB Storage: The rules are stored in MongoDB in a structured format (AST), enabling easy retrieval and evaluation.
* Error Handling: The system provides feedback for invalid rules or missing data.

PREREQUISITES

Before running this project, ensure you have the following installed:
* Python 3.8+
* MongoDB (Running locally or using a cloud instance like MongoDB Atlas)
* Postman/Thunderclient (Optional, for testing API requests)
* Git (For version control and pushing to GitHub)

## SETUP INSTRUCTIONS

1. Clone the Repository:  
    git clone https://github.com/your-username/rule-engine-ast.git  
cd rule-engine-ast
2. Create a Virtual Environment  
python -m venv venv  
source venv/bin/activate   # For Linux/Mac  
venv\Scripts\activate       # For Windows  
3. Install Dependencies  
pip install -r requirements.txt  
4. Ensure MongoDB is Running  
Make sure MongoDB is running locally at mongodb://localhost:27017/.  
6. Run the Flask Application  
python app.py  
The Flask server will start on http://127.0.0.1:5000.

### API ENPOINTS
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

##### API Endpoints (Simplified)
Create Rule: /create_rule

Method: POST
Payload: { "rule_string": "(age > 30 AND department = 'Sales')" }
Response: { "rule_id": "<rule_id>" }

Evaluate Rule: /evaluate_rule/<rule_id>

Method: POST
Payload: { "user_data": {"age": 35, "department": "Sales"} }
Response: { "result": true/false }

###### Non-Functional Requirements
1. SECURITY
    -Input Validation: All inputs from users are validated to prevent injection attacks, such as invalid characters or improper data types. Validation is enforced in API endpoints to ensure only well-formed rules are processed.
    -MongoDB Security: Ensure MongoDB is secured with authentication if deployed in production. Using environment variables for sensitive data like the MongoDB URI is encouraged.
    -Error Handling: Implemented detailed error handling to ensure that meaningful messages are returned in case of failure, such as invalid rules or database errors.

2. PERFORMANCE
    Optimized Rule Evaluation: AST is stored in a structured format (as dictionaries), minimizing the overhead of re-parsing rules during evaluation.
    Caching: In a larger production environment, frequently used rules could be cached to reduce the number of database queries and enhance performance.
    Database Indexing: MongoDB collections have indexes on the _id field, which speeds up rule retrieval. Additional indexing on frequently queried fields can be added for optimization.

3. SCALABILITY
    Modular Design: The architecture separates concerns (UI, API, and database) allowing the application to scale independently for different layers.
    Cloud-Ready: The system is designed to be easily deployable on cloud services like AWS or Heroku by adjusting environment configurations.

4. EXTENSIBILITY
    Dynamic Rule Modification: The rule engine can be easily extended to allow users to modify existing rules or add new types of conditions to the AST.
    Custom Functions: The system can be extended to support custom user-defined functions for more advanced rule logic in the future.

##### DEPLOYMENT TO GITHUB
Step-by-Step Guide to Push Your Code to GitHub:
1. Initialize Git If not already initialized, run the following in your project directory:
   git init
2. Add Remote Repository If your GitHub repository is already created, link it to your local project:
   git remote add origin https://github.com/your-username/your-repo-name.git
3. Add Files and Commit Stage the files and commit the changes:
   git add .
   git commit -m "Initial project setup with Rule Engine"
4. Push to GitHub Push the local changes to your GitHub repository:
   git push -u origin main
5. Check on GitHub Verify that all files are now uploaded to your repository on GitHub.

###### DEVELOPMENT NOTES
    AST Representation: The project uses Python's ast module to parse rule strings into Abstract Syntax Trees (AST), allowing dynamic rule manipulation and efficient evaluation.
    MongoDB Structure: Rules are stored as a dictionary that represents the AST structure, allowing the system to recreate and evaluate rules directly from the database.
    Error Handling: The system includes checks for invalid rule formats and incorrect MongoDB ObjectIDs, ensuring that users receive helpful error messages when something goes wrong.

###### FUTURE IMPROVEMENTS
    Support for More Complex Rules: Expand the rule syntax to include more operators (like <=, >=, etc.).
    Improved Frontend: Build a more user-friendly UI for creating and testing rules, instead of relying on Postman.
    Support for Functions: Add support for user-defined functions within the rules.
