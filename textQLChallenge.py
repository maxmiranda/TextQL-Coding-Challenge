from Query import Query 
from JSONFileManager import JSONFileManager

query_string = input("\n" +"########################################################" + "\n"+ "\n" + "Welcome to MaxSQL. To begin, import a new file by writing out IMPORT file_name.json. From there you will be able to select from the table file_name \n \n QUERY: ")
file_manager = JSONFileManager()

while query_string:
    if query_string.startswith("IMPORT "):
        file_path = query_string.replace("IMPORT ", "")
        file_manager.import_file(file_path)
    else:
        try: 
            query = Query(query_string)
            file_name = query.from_table
            file = file_manager.get_file_content(file_name)
            if not file: 
                print(f"No such file {file_name} \n Valid files are: {file_manager.list_files()}")
            else: 
                query.execute(file, file_name)
        except Exception as e: 
            print(e)

    query_string = input("Query:")


def runTests(): 
    file_manager = JSONFileManager()
    