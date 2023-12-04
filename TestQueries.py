import unittest
import json
from Query import Query

class TestQueries(unittest.TestCase):
    def test_equals_query(self):
        file_path = "data1.json"
        with open(file_path, 'r') as file:
            table = json.load(file)
            table_name = file_path.replace(".json", "")
            query = Query("""SELECT state FROM table WHERE pop = 1;""")
            result = query.execute(table, table_name)
            expected_states = ['California', 'Texas']
            self.assertListEqual(result, expected_states)

    def test_compound_query(self):
        file_path = "data1.json"
        with open(file_path, 'r') as file:
            table = json.load(file)
            table_name = file_path.replace(".json", "")
            query = Query("""SELECT state FROM table WHERE pop = 1 AND state != 'California';""")
            result = query.execute(table, table_name)
            expected_states = ['Texas'] 
            self.assertListEqual(result, expected_states)

    def test_select_all(self):
        file_path = "data1.json"
        with open(file_path, 'r') as file:
            table = json.load(file)
            table_name = file_path.replace(".json", "")
            query = Query("""SELECT * FROM table WHERE pop = 1 AND state != 'California';""")
            result = query.execute(table, table_name)
            expected_states = [{"state": "Texas", "region": "South", "pop": 1, "pop_male": 4, "pop_female": 6}] 
            self.assertListEqual(result, expected_states)

    def test_parentheses_1(self):    
        file_path = "data1.json"
        with open(file_path, 'r') as file:
            table = json.load(file)
            table_name = file_path.replace(".json", "")
            query = Query("""SELECT state FROM table WHERE pop > 3 OR (pop_female = 6 AND region = 'West');""")
            result = query.execute(table, table_name)
            expected_states = ['California', 'New York', 'Illinois', 'Arizona']  
            self.assertListEqual(result, expected_states)

    def test_parentheses_2(self):    
        file_path = "data1.json"
        with open(file_path, 'r') as file:
            table = json.load(file)
            table_name = file_path.replace(".json", "")
            query = Query("""SELECT state FROM table WHERE (pop > 3 OR pop_female = 6) AND region = 'West';""")
            result = query.execute(table, table_name)
            expected_states = ['California', 'Arizona']  
            self.assertListEqual(result, expected_states)
    
    def test_two_col_comparison(self):
        file_path = "data1.json"
        with open(file_path, 'r') as file:
            table = json.load(file)
            table_name = file_path.replace(".json", "")
            query = Query("""SELECT state FROM table WHERE pop_male > pop_female;""")
            result = query.execute(table, table_name)
            expected_states = ['Florida']  
            self.assertListEqual(result, expected_states)

    def test_greater_than_equal_to(self):
        file_path = "data1.json"
        with open(file_path, 'r') as file:
            table = json.load(file)
            table_name = file_path.replace(".json", "")
            query = Query("""SELECT state FROM table WHERE pop_male >= pop_female;""")
            result = query.execute(table, table_name)
            expected_states = ['Florida', 'New York']  
            self.assertListEqual(result, expected_states)

    def test_limit(self):
        file_path = "data1.json"
        with open(file_path, 'r') as file:
            table = json.load(file)
            table_name = file_path.replace(".json", "")
            query = Query("""SELECT state FROM table LIMIT 3""")
            result = query.execute(table, table_name)
            expected_states = ['California', 'Texas', 'Florida']  
            self.assertListEqual(result, expected_states)
            
if __name__ == '__main__':
    unittest.main()
