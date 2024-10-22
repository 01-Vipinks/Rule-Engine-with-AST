import ast

# Node structure for AST
class Node:
    def __init__(self, type, left=None, right=None, value=None):
        self.type = type  # 'operator' or 'operand'
        self.left = left  # Reference to left child
        self.right = right  # Reference to right child
        self.value = value  # For operand nodes

    # Method to serialize the node to a dictionary
    def to_dict(self):
        node_dict = {
            'type': self.type,
            'value': self.value,
        }
        if self.left:
            node_dict['left'] = self.left.to_dict()
        if self.right:
            node_dict['right'] = self.right.to_dict()
        return node_dict

    # Method to deserialize a dictionary back into a Node object (optional for later use)
    @staticmethod
    def from_dict(node_dict):
        node = Node(
            type=node_dict['type'],
            value=node_dict['value']
        )
        if 'left' in node_dict:
            node.left = Node.from_dict(node_dict['left'])
        if 'right' in node_dict:
            node.right = Node.from_dict(node_dict['right'])
        return node


# Function to convert AST to custom Node structure
def convert_ast_to_node(ast_node):
    if isinstance(ast_node, ast.BoolOp):
        # Handle Boolean operations (and/or)
        operator = None
        if isinstance(ast_node.op, ast.And):
            operator = 'and'
        elif isinstance(ast_node.op, ast.Or):
            operator = 'or'
        
        # For BoolOp, the values are in a list, we need to recursively process all of them
        left = convert_ast_to_node(ast_node.values[0])
        right = convert_ast_to_node(ast_node.values[1])
        
        return Node(
            type='operator',
            left=left,
            right=right,
            value=operator
        )
    elif isinstance(ast_node, ast.BinOp):
        # Handle binary operations (like adding numbers)
        operator = None
        if isinstance(ast_node.op, ast.Add):
            operator = '+'
        elif isinstance(ast_node.op, ast.Sub):
            operator = '-'
        # Additional operators can be added here
        return Node(
            type='operator',
            left=convert_ast_to_node(ast_node.left),
            right=convert_ast_to_node(ast_node.right),
            value=operator
        )
    elif isinstance(ast_node, ast.Compare):
        # Handle comparison operations (e.g., age > 30)
        left = ast_node.left.id  # E.g., 'age'
        comparator = ast_node.ops[0]
        if isinstance(comparator, ast.Gt):
            op = '>'
        elif isinstance(comparator, ast.Lt):
            op = '<'
        elif isinstance(comparator, ast.Eq):
            op = '=='
        else:
            raise ValueError(f"Unsupported comparator: {comparator}")
        
        right = ast_node.comparators[0].n  # E.g., '30'
        return Node(
            type='operand',
            value=f"{left} {op} {right}"
        )
    else:
        raise ValueError(f"Unsupported AST node type: {type(ast_node)}")

# Function to create an AST from rule string
def create_rule(rule_string):
    # Step 1: Replace logical operators to Python-compatible ones
    rule_string = rule_string.replace("AND", "and").replace("OR", "or").replace("NOT", "not")
    
    # Step 2: Parse the rule string into an AST
    try:
        tree = ast.parse(rule_string, mode="eval")
        return convert_ast_to_node(tree.body)
    except SyntaxError as e:
        raise ValueError(f"Invalid rule syntax: {e}")

# Function to evaluate the rule AST against user data
def evaluate_rule(ast_node, data):
    if ast_node.type == 'operator':
        # Evaluate based on operator (and/or)
        left_result = evaluate_rule(ast_node.left, data)
        right_result = evaluate_rule(ast_node.right, data)

        if ast_node.value == 'and':
            return left_result and right_result
        elif ast_node.value == 'or':
            return left_result or right_result
        else:
            raise ValueError(f"Unknown operator: {ast_node.value}")
    
    elif ast_node.type == 'operand':
        # Evaluate a single condition (e.g., age > 30)
        try:
            return eval(ast_node.value, {}, data)
        except Exception as e:
            raise ValueError(f"Error evaluating operand {ast_node.value}: {e}")

# Example: Combine multiple rules (optional function)
def combine_rules(rules):
    # Combining multiple ASTs for rules into one, 
    # Here, for simplicity, we just 'and' them together
    combined_ast = rules[0]
    for rule in rules[1:]:
        combined_ast = Node(
            type='operator',
            left=combined_ast,
            right=rule,
            value='and'
        )
    return combined_ast
