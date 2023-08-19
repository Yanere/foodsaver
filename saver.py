import sqlite3
import time
import requests
import threading


def add_food():

    food = input("Enter food name: ")
    expiration_date = input("Enter remaining days: ")

    print(food, expiration_date)
    connection = sqlite3.connect("food.db")
    cursor = connection.cursor()

    cursor.execute('SELECT id FROM foods WHERE name = ?', (food,))
    existing_record = cursor.fetchone()

    if existing_record:
        print(f"{food} already exists in the database")

    else:

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS foods(
            id INTEGER PRIMARY KEY,
            name TEXT,
            expiration_date TEXT
            )
        """)

        cursor.execute(
            "INSERT INTO foods (name, expiration_date) VALUES (?,?)", (food, expiration_date))
        connection.commit()

        print(f"Added food: {food} (Expiration date: {expiration_date} days)")
        print("--------------")

        connection.close()


def check_expiration():
    print("--------------")
    connection = sqlite3.connect("food.db")
    cursor = connection.cursor()

    cursor.execute("SELECT id, name, expiration_date FROM foods")
    all_foods = cursor.fetchall()

    for food in all_foods:
        id, name, expiration_date = food
        if int(expiration_date) <= 0:
            print(f"{name} = EXPIRED")
        elif int(expiration_date) < 5:
            print(f"{name} = {expiration_date} days left - WARNING")
        else:
            print(f"{name} = {expiration_date} days left")
    print("--------------")


def delete_food():
    connection = sqlite3.connect("food.db")
    cursor = connection.cursor()

    food_to_delete = input("Enter name of the food to delete: ")
    cursor.execute('SELECT id FROM foods WHERE name = ?', (food_to_delete,))
    existing_record = cursor.fetchone()

    if existing_record:
        cursor.execute('DELETE FROM foods WHERE name = ?', (food_to_delete,))
        connection.commit()
        print(f"{food_to_delete} has been deleted from the database")
    else:
        print(f"{food_to_delete} not found in the database")

    connection.close()


def send_notification():
    while True:
        connection = sqlite3.connect("food.db")
        cursor = connection.cursor()

        cursor.execute("SELECT name FROM foods WHERE expiration_date <= 0")
        expired_foods = cursor.fetchall()

        for food in expired_foods:
            food_name = food[0]

            requests.post("https://ntfy.sh/<REPLACEME>",
                          data=f"{food_name} has expired 😞".encode(encoding='utf-8'))

        connection.close()
        time.sleep(86400)


def user_input_thread():
    while True:
        print("What do you want to do?")
        print("1. Add food")
        print("2. Check Expiration")
        print("3. Delete Food")

        user_choice = input("Enter your choice: ")

        options = {
            "1": add_food,
            "2": check_expiration,
            "3": delete_food,
        }

        selected_option = options.get(user_choice)
        if selected_option:
            selected_option()
        else:
            print("Invalid choice. Please enter a valid option.")


if __name__ == "__main__":

    connection = sqlite3.connect("food.db")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS foods(
        id INTEGER PRIMARY KEY,
        name TEXT,
        expiration_date TEXT
        )
    """)

    notification_thread = threading.Thread(target=send_notification)
    notification_thread.start()

    user_input_thread = threading.Thread(target=user_input_thread)
    user_input_thread.start()
