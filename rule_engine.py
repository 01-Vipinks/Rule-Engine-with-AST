import ast

# Node structure for AST
class Node:
    def __init__(self, type, left=None, right=None, value=None):
        self.type = type  # 'operator' or 'operand'
        self.left = left  # Reference to left child
        self.right = right  # Reference to right child
        self.value = value  # For operand nodes or operator

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
        operator = 'and' if isinstance(ast_node.op, ast.And) else 'or'
        
        # For BoolOp, the values are in a list, we need to recursively process all of them
        left = convert_ast_to_node(ast_node.values[0])
        right = convert_ast_to_node(ast_node.values[1])
        
        return Node(
            type='operator',
            left=left,
            right=right,
            value=operator
        )
    elif isinstance(ast_node, ast.Compare):
        # Handle comparison operations (e.g., age > 30)
        left = ast_node.left.id  # E.g., 'age'
        comparator = ast_node.ops[0]
        
        # Determine the operator
        if isinstance(comparator, ast.Gt):
            op = '>'
        elif isinstance(comparator, ast.Lt):
            op = '<'
        elif isinstance(comparator, ast.Eq):
            op = '=='
        else:
            raise ValueError(f"Unsupported comparator: {comparator}")
        
        # Handle string literals
        right_value = ast_node.comparators[0]
        if isinstance(right_value, ast.Num):  # Number comparison
            right = right_value.n
        elif isinstance(right_value, ast.Str):  # String comparison
            right = repr(right_value.s)  # Use repr to add quotes

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
            # Using eval in a restricted manner
            return eval(ast_node.value, {}, data)
        except Exception as e:
            raise ValueError(f"Error evaluating operand {ast_node.value}: {e}")

# Example: Combine multiple rules (optional function)
def combine_rules(rules, operator="AND"):
    """
    Combine multiple rules (AST nodes) into a single AST using a logical operator.
    :param rules: List of AST nodes.
    :param operator: Logical operator to combine the rules ('AND' or 'OR').
    :return: Combined AST node.
    """
    if not rules:
        return None

    if len(rules) == 1:
        return rules[0]

    combined = rules[0]

    for rule in rules[1:]:
        if operator == "AND":
            combined = Node(type="operator", left=combined, right=rule, value="and")
        elif operator == "OR":
            combined = Node(type="operator", left=combined, right=rule, value="or")

    return combined
