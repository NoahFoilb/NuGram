import mysql.connector
from mysql.connector import Error

def replace_word_in_file(file_path, old_word, new_word):
    # Read the file
    with open(file_path, 'r') as file:
        file_contents = file.read()

    # Replace the word
    file_contents = file_contents.replace(old_word, new_word)

    # Write the file back
    with open(file_path, 'w') as file:
        file.write(file_contents)

def create_db_connection(name,password):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='project',
            user=name,
            password=password
        )
        return connection
    except mysql.connector.Error as err:
        print("MySQL Error: ", err)
        return None

def main():
    name = input("Enter mysql database username: ")
    password = input("Enter mysql database password: ")
    file_path = 'app.py'

    try:
        connection = create_db_connection(name,password)
        if connection is None:
            print("does not work")
        else:
            replace_word_in_file(file_path, 'mysql123', password)
            replace_word_in_file(file_path, 'root', name)
    except Error as e:
        print(f"Error: {e}")
        return None



if __name__ == '__main__':
    main()


