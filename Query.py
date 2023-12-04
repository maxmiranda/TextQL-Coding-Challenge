from posixpath import split
import re
    
class LogicalOperator:
    def __init__(self, operator, left, right):
        self.operator = operator
        self.left = left
        self.right = right

    def evaluate(self, row):
        if self.operator == "AND":
            return self.left.evaluate(row) and self.right.evaluate(row)
        elif self.operator == "OR":
            return self.left.evaluate(row) or self.right.evaluate(row)

class Condition: 
    def __init__(self, column, operator, value):
        self.column = column
        self.operator = operator
        self.value = value
    
    def evaluate(self, row):
        if self.column not in row:
            raise Exception(f"Column {self.column} not found in row")
        row_value = row[self.column]
        # If the right hand value is given as a column name, allow us to compare on that basis
        if self.value in row: 
            right_hand_value = row[self.value]
        else: 
            # Conver the right_hand_value to the desired type (NOTE: we only have to do this if not coming directly from another column because if coming from other column it's automatically the correc type)
            if type(row_value) is int: 
                right_hand_value = int(self.value)
            elif type(row_value) is str:
                right_hand_value = str(self.value)
        if self.operator == "=":
            return row_value == right_hand_value
        elif self.operator == "!=":
            return row_value != right_hand_value
        elif self.operator == ">": 
            return row_value > right_hand_value
        elif self.operator == "<": 
            return row_value < right_hand_value
        elif self.operator == "<=": 
            return row_value <= right_hand_value
        elif self.operator == ">=": 
            return row_value >= right_hand_value
        raise Exception(f"Unknown operator: {self.operator}")

class Query:
    def __init__(self, query_string):
        self.query_string = query_string
        self.select_columns = None
        self.from_table = None
        self.where_conditions = None
        self.limit = None
        self.parse_query()

    def parse_query(self):
        # Regular expression patterns for different parts of the SQL query
        select_pattern = r"SELECT\s+(.*?)\s+FROM"
        from_pattern = r"FROM\s+(\w+)"
        where_pattern = r"WHERE\s+(.*?)\s*(LIMIT|$)"
        limit_pattern = r"LIMIT\s+(\d+)"

        # Extracting different parts of the SQL query
        select_columns = re.search(select_pattern, self.query_string, re.IGNORECASE)
        from_table = re.search(from_pattern, self.query_string, re.IGNORECASE)
        where_conditions = re.search(where_pattern, self.query_string, re.IGNORECASE)
        limit = re.search(limit_pattern, self.query_string, re.IGNORECASE)

        select_clause = select_columns.group(1).strip()
        # Parsing the results
        if select_clause == '*':
            self.select_columns = '*'
        else:
            self.select_columns = [col.strip() for col in select_columns.group(1).split(',')]
        self.from_table = from_table.group(1).strip() if from_table else None
        self.where_conditions = where_conditions.group(1).strip() if where_conditions else None
        self.limit = int(limit.group(1).strip()) if limit else None

    def execute(self, table, table_name):
        num_data_points = 0
        output_list = []
        for row in table: 
            # If where conditions are all satisified
            if self.where_conditions_satisfied(row): 
                if self.select_columns == "*":
                    output_list.append(row)
                    print(row)
                else:
                    # validate the selected columns from the query
                    selected_columns = []
                    for c in self.select_columns:
                        if c not in row:
                            print(f"No column {c} in table {table_name}")
                            return
                        selected_columns.append(row[c])
                    output_str = ', '.join(selected_columns)
                    output_list.append(output_str)
                    print(output_str)
                num_data_points += 1
                if num_data_points == self.limit:
                    return output_list
        return output_list
    
    def where_conditions_satisfied(self, row):
        if not self.where_conditions:
            return True
        condition_tree = self.parse_condition_string(self.where_conditions)
        return condition_tree.evaluate(row)
    
    def parse_condition_string(self, cond_str):
        tokens = re.findall(r'\(|\)|\w+|[<>=!]+|AND|OR', cond_str)
        def parse_expression(tokens):
            stack = []
            while tokens:
                token = tokens.pop(0)
                if token == '(':
                    stack.append(parse_expression(tokens))
                elif token == ')':
                    break
                elif token in ['AND', 'OR']:
                    left = stack.pop()
                    right = parse_expression(tokens)
                    stack.append(LogicalOperator(token, left, right))
                else:  # it's a condition
                    column, operator, value = token, tokens.pop(0), tokens.pop(0)
                    stack.append(Condition(column, operator, value))
            return stack[0] if len(stack) == 1 else stack

        return parse_expression(tokens)