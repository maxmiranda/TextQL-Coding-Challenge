# TextQL-Coding-Challenge

To run:

```
python3 textQLChallenge.py
```

File Overviews: 
- `textQLChallenge.py`: Enables command line interface, allowing users to either:
    - IMPORT new tables or
    - Run queries of the structure `SELECT (comma separated list of cols or \*) FROM TABLE WHERE (conditions) LIMIT (integer);`
- `JSONFileManager.py`: Simple solution to enable users to import from different JSON files while we keep track of what tables correspond to what data
- `Query.py`: The meat of the problem, contains all the logic for how we:
  - Parse a query (into the core components of SELECT, FROM, WHERE, LIMIT)
  - Execute a query on some given table
  - Parse the conditions of a query
  - Evaluate a particular row against the parsed conditions
      - This is where the classes `LogicalOperator` & `Condition` come in handy
- `TestQueries.py`: Runs through 10 different tests on data1.json ensuring we have ability to:
  - Select *
  - Select multiple rows
  - Execute compound queries
  - Parse Parentheses properly
  - Use the LIMIT operator
  - Use >, >=, !=, =, AND, and OR operators
