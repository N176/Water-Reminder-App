# diet_planner/database.py
import mysql.connector
import json
import os
from tkinter import messagebox


import time

# from main import switch_to_update


def read_config_from_json(file_name):
    script_directory = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(script_directory, file_name)
    # print(f"File path: {file_path}")  # Add this line to check the generated file path

    with open(file_path, 'r') as file:
        config_data = json.load(file)

    return config_data


config_data = read_config_from_json('hydration_goals.json')

# Constants
DATABASE_HOST = config_data['mysql_data']['HOST']
DATABASE_USER = config_data['mysql_data']['USER']
DATABASE_PASSWORD = config_data['mysql_data']['PASSWORD']
DATABASE_NAME = config_data['mysql_data']['NAME']

def initialize_database():
    # Create a connection to the MySQL database
    connection = mysql.connector.connect(
        host=DATABASE_HOST,
        user=DATABASE_USER,
        password=DATABASE_PASSWORD,
        database=DATABASE_NAME
    )

    # Create a cursor object to execute SQL queries
    cursor = connection.cursor()

    # Create the user_profiles table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL,
            goal INT NOT NULL,
            age INT,
            weight FLOAT,
            height FLOAT
        )
    ''')
    print("Database connected")
    # Commit the changes and close the connection
    connection.commit()
    connection.close()

# Inside database.py

def save_user_profile(username, email, password, goal, age, height, weight):
    connection = mysql.connector.connect(
        host=DATABASE_HOST,
        user=DATABASE_USER,
        password=DATABASE_PASSWORD,
        database=DATABASE_NAME
    )

    cursor = connection.cursor()

    try:
        # Insert user data into the users table
        cursor.execute('INSERT INTO users (username, email, password, goal, age, height, weight) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                       (username, email, password, goal, age, height, weight))

        print("User added")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        connection.commit()
        connection.close()


def update_user_profile(username, new_goal=None, password=None):
    connection = mysql.connector.connect(
        host=DATABASE_HOST,
        user=DATABASE_USER,
        password=DATABASE_PASSWORD,
        database=DATABASE_NAME
    )
    cursor = connection.cursor()

    try:
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        user_profile = cursor.fetchone()

        if user_profile and user_profile[3] == password:
            # Update the user's goal if a new goal is provided
            if new_goal is not None:
                cursor.execute("UPDATE users SET goal = %s WHERE username = %s;", (new_goal, username))
                connection.commit()
                messagebox.showinfo("Update", "Goal updated!")
            else:
                print("No changes to the goal provided.")
        else:
            print("Access Denied!")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        connection.close()


def get_user_profile(username):
    connection = mysql.connector.connect(
        host=DATABASE_HOST,
        user=DATABASE_USER,
        password=DATABASE_PASSWORD,
        database=DATABASE_NAME
    )

    cursor = connection.cursor()

    try:
        # Retrieve user profile
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        user_profile = cursor.fetchone()


        # Convert the result to a dictionary for easier use
        if user_profile:
            return {
                'user_id': user_profile[0],
                'username': user_profile[1],
                'email': user_profile[2],
                'goal': user_profile[4],
                'age': user_profile[5],
                'height': user_profile[6],
                'weight': user_profile[7]
            }
        else:
            return None

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        connection.close()
# initialize_database()

