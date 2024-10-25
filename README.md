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
&nbsp;- git clone https://github.com/your-username/rule-engine-ast.git  
&nbsp;- cd rule-engine-ast
2. Create a Virtual Environment:  
&nbsp;- python -m venv venv  
&nbsp;- source venv/bin/activate # For Linux/Mac  
&nbsp;- venv\Scripts\activate &emsp;# For Windows  
3. Install Dependencies:  
&nbsp;- pip install -r requirements.txt  
4. Ensure MongoDB is Running:  
&nbsp;- Make sure MongoDB is running locally at mongodb://localhost:27017/.  
5. Run the Flask Application:  
&nbsp;- python app.py  
The Flask server will start on http://127.0.0.1:5000.

### API ENPOINTS
1. Create Rule  
&nbsp;Endpoint: /create_rule  
&nbsp;Method: POST  
&nbsp;Description: Creates a new rule from the provided rule string and stores it in MongoDB.

&emsp; &emsp; &emsp;Request Payload:  
&emsp; &emsp; &emsp;{  
  &emsp; &emsp; &emsp;"rule_string": "(age > 30 AND department == 'Sales') OR (salary > 50000)"  
&emsp; &emsp; &emsp;}  

&emsp; &emsp; &emsp;Response:  
&emsp; &emsp; &emsp;{  
  &emsp; &emsp; &emsp;"message": "Rule created",  
  &emsp; &emsp; &emsp;"rule_id": "MongoDB ObjectID"  
&emsp; &emsp; &emsp;}  

2. Evaluate Rule  
&nbsp;Endpoint: /evaluate_rule/<rule_id>  
&nbsp;Method: POST  
&nbsp;Description: Evaluates a specific rule stored in the database against the provided user data.

&emsp; &emsp; &emsp;Request Payload:  
&emsp; &emsp; &emsp;{  
  &emsp; &emsp; &emsp;"user_data": {  
    &emsp; &emsp; &emsp;"age": 35,  
    &emsp; &emsp; &emsp;"department": "Sales",  
    &emsp; &emsp; &emsp;"salary": 60000  
  &emsp; &emsp; &emsp;}  
&emsp; &emsp; &emsp;}  

&emsp; &emsp; &emsp;Response:  
&emsp; &emsp; &emsp;{  
  &emsp; &emsp; &emsp;"result": true  
&emsp; &emsp; &emsp;}  

### API Endpoints (Simplified)
Create Rule: /create_rule  

&nbsp;Method: POST  
&nbsp;Payload: { "rule_string": "(age > 30 AND department = 'Sales')" }  
&nbsp;Response: { "rule_id": "<rule_id>" }  

Evaluate Rule: /evaluate_rule/<rule_id>  

&nbsp;Method: POST  
&nbsp;Payload: { "user_data": {"age": 35, "department": "Sales"} }  
&nbsp;Response: { "result": true/false }  

## Non-Functional Requirements
1. SECURITY  
&emsp;-Input Validation: All inputs from users are validated to prevent injection attacks, such as invalid characters or improper data types. Validation is enforced in API endpoints to ensure only well-formed rules are processed.  
&emsp;-MongoDB Security: Ensure MongoDB is secured with authentication if deployed in production. Using environment variables for sensitive data like the MongoDB URI is encouraged.  
&emsp;-Error Handling: Implemented detailed error handling to ensure that meaningful messages are returned in case of failure, such as invalid rules or database errors.  

2. PERFORMANCE  
&emsp;-Optimized Rule Evaluation: AST is stored in a structured format (as dictionaries), minimizing the overhead of re-parsing rules during evaluation.  
&emsp;-Caching: In a larger production environment, frequently used rules could be cached to reduce the number of database queries and enhance performance.  
&emsp;-Database Indexing: MongoDB collections have indexes on the _id field, which speeds up rule retrieval. Additional indexing on frequently queried fields can be added for optimization.  

3. SCALABILITY  
&emsp;-Modular Design: The architecture separates concerns (UI, API, and database) allowing the application to scale independently for different layers.  
&emsp;-Cloud-Ready: The system is designed to be easily deployable on cloud services like AWS or Heroku by adjusting environment configurations.  

4. EXTENSIBILITY  
&emsp;-Dynamic Rule Modification: The rule engine can be easily extended to allow users to modify existing rules or add new types of conditions to the AST.  
&emsp;-Custom Functions: The system can be extended to support custom user-defined functions for more advanced rule logic in the future.  

## DEPLOYMENT TO GITHUB
Step-by-Step Guide to Push Your Code to GitHub:  
1. Initialize Git If not already initialized, run the following in your project directory:  
&ensp;git init  
2. Add Remote Repository If your GitHub repository is already created, link it to your local project:  
&ensp;git remote add origin https://github.com/your-username/your-repo-name.git  
3. Add Files and Commit Stage the files and commit the changes:  
&ensp;git add .  
&ensp;git commit -m "Initial project setup with Rule Engine"  
4. Push to GitHub Push the local changes to your GitHub repository:  
&ensp;git push -u origin main  
5. Check on GitHub Verify that all files are now uploaded to your repository on GitHub.  

## DEVELOPMENT NOTES  
&nbsp;-AST Representation: The project uses Python's ast module to parse rule strings into Abstract Syntax Trees (AST), allowing dynamic rule manipulation and efficient evaluation.  
&nbsp;-MongoDB Structure: Rules are stored as a dictionary that represents the AST structure, allowing the system to recreate and evaluate rules directly from the database.  
&nbsp;-Error Handling: The system includes checks for invalid rule formats and incorrect MongoDB ObjectIDs, ensuring that users receive helpful error messages when something goes wrong.  

## FUTURE IMPROVEMENTS  
&nbsp;-Support for More Complex Rules: Expand the rule syntax to include more operators (like <=, >=, etc.).  
&nbsp;-Improved Frontend: Build a more user-friendly UI for creating and testing rules, instead of relying on Postman.  
&nbsp;-Support for Functions: Add support for user-defined functions within the rules.  

## License  
This project is licensed under the MIT License.
