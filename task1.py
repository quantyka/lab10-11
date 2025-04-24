import psycopg2
import csv

def connect():

    return psycopg2.connect(

        dbname="postgres",
        user="postgres",
        password="147852",
        host="localhost",
        port="5432"

    )

def create_table():

    conn = connect()

    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(100),
            phone_number VARCHAR(20)
        )
    """)

    conn.commit()
    cur.close()
    conn.close()

    print("Таблица готова.")

def insert_from_csv(path):

    try:

        conn = connect()
        cur = conn.cursor()

        with open(path, "r") as file:

            reader = csv.reader(file)

            next(reader)

            for row in reader:

                cur.execute("INSERT INTO phonebook (first_name, phone_number) VALUES (%s, %s)", row)

        conn.commit()

        print("Данные загружены из CSV.")

    except FileNotFoundError:

        print("Файл не найден.")

    finally:

        cur.close()
        conn.close()

def insert_from_console():

    name = input("Имя: ")
    phone = input("Телефон: ")
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO phonebook (first_name, phone_number) VALUES (%s, %s)", (name, phone))
    conn.commit()
    cur.close()
    conn.close()

    print("Добавлено!")

def update_phone(name, new_phone):

    conn = connect()
    cur = conn.cursor()
    cur.execute("UPDATE phonebook SET phone_number = %s WHERE first_name = %s", (new_phone, name))
    conn.commit()
    cur.close()
    conn.close()

    print(f"Обновлено: {name} → {new_phone}")

def update_name(old_name, new_name):

    conn = connect()
    cur = conn.cursor()
    cur.execute("UPDATE phonebook SET first_name = %s WHERE first_name = %s", (new_name, old_name))
    conn.commit()
    cur.close()
    conn.close()

    print(f"Имя обновлено: {old_name} → {new_name}")

def query_filter_by_phone_start(start):

    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM phonebook WHERE phone_number LIKE %s", (f"{start}%",))
    rows = cur.fetchall()

    if rows:

        for row in rows:

            print(row)
    else:

        print("Ничего не найдено.")

    cur.close()
    conn.close()

def delete_by_name(name):

    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM phonebook WHERE first_name = %s", (name,))
    conn.commit()
    cur.close()
    conn.close()

    print(f"Удалено по имени: {name}")

def delete_by_phone(phone):

    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM phonebook WHERE phone_number = %s", (phone,))
    conn.commit()
    cur.close()
    conn.close()

    print(f"Удалено по номеру: {phone}")

def show_all():

    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM phonebook ORDER BY id")
    rows = cur.fetchall()

    print("Все записи:")

    for row in rows:

        print(row)

    cur.close()
    conn.close()

def menu():

    while True:

        print("/nPHONEBOOK MENU")
        print("1. Создать таблицу")
        print("2. Загрузить из CSV")
        print("3. Добавить вручную")
        print("4. Обновить номер")
        print("5. Обновить имя")
        print("6. Найти по началу номера")
        print("7. Удалить по имени")
        print("8. Удалить по номеру")
        print("9. Показать все")
        print("0. Выход")

        choice = input("Выберите действие: ")

        if choice == "1":

            create_table()

        elif choice == "2":

            path = input("C:/Users/quant/Desktop/lab10-11/phonebook.csv")

            insert_from_csv(path)

        elif choice == "3":

            insert_from_console()

        elif choice == "4":

            name = input("Чьё имя обновить? ")

            new_phone = input("Новый номер: ")

            update_phone(name, new_phone)

        elif choice == "5":

            old_name = input("Текущее имя: ")

            new_name = input("Новое имя: ")

            update_name(old_name, new_name)

        elif choice == "6":

            start = input("Начало номера: ")

            query_filter_by_phone_start(start)

        elif choice == "7":

            name = input("Имя для удаления: ")

            delete_by_name(name)

        elif choice == "8":

            phone = input("Номер для удаления: ")

            delete_by_phone(phone)

        elif choice == "9":

            show_all()

        elif choice == "0":

            print("Выход.")

            break

        else:

            print("Неверный ввод. Попробуйте ещё раз.")

if __name__ == "__main__":
    
    menu()