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

        with open(path, "r", newline='') as file:

            reader = csv.reader(file)

            next(reader)

            for row in reader:

                cur.execute(

                    "INSERT INTO phonebook (first_name, phone_number) VALUES (%s, %s)",
                    row
                )

        conn.commit()

        print("Данные загружены из CSV.")

    except FileNotFoundError:

        print("Файл не найден.")

    finally:

        cur.close()
        conn.close()

def upsert_user():

    name = input("Имя: ")
    phone = input("Телефон: ")

    conn = connect()
    cur = conn.cursor()
    cur.execute(
        "UPDATE phonebook SET phone_number = %s WHERE first_name = %s",
        (phone, name)
    )
    if cur.rowcount == 0:

        cur.execute(
            "INSERT INTO phonebook (first_name, phone_number) VALUES (%s, %s)",
            (name, phone)
        )

        print(f"Добавлено: {name} — {phone}")

    else:

        print(f"Обновлено: {name} — {phone}")

    conn.commit()
    cur.close()
    conn.close()

def search_pattern(start):

    conn = connect()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM phonebook WHERE first_name ILIKE %s OR phone_number LIKE %s",
        (f"%{start}%", f"%{start}%")
    )

    rows = cur.fetchall()

    if rows:

        print("Результаты поиска:")

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

def paginate_records():

    lim = int(input("Limit: "))
    off = int(input("Offset: "))

    conn = connect()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM phonebook ORDER BY id LIMIT %s OFFSET %s",
        (lim, off)
    )

    rows = cur.fetchall()

    print(f"Вывод {lim} записей, начиная с {off}:")

    for row in rows:

        print(row)

    cur.close()
    conn.close()

def add_set():

    val = int(input("Введите количество контактов:\n"))

    for _ in range(val):

        upsert_user()

    print("Готово!")

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

        print("\nPHONEBOOK MENU")
        print("1. Загрузить из CSV")
        print("2. Добавить/обновить вручную")
        print("3. Ввод списком")
        print("4. Найти по паттерну")
        print("5. Ввывод списка")
        print("6. Удалить по имени")
        print("7. Удалить по номеру")
        print("8. Показать все")
        print("0. Выход")

        choice = input("Выберите действие: ")

        if choice == "1":

            path = input("Путь к CSV-файлу: ")

            insert_from_csv(path)

        elif choice == "2":

            upsert_user()

        elif choice == "3":

            add_set()

        elif choice == "4":

            pat = input("Паттерн: ")

            search_pattern(pat)

        elif choice == "5":

            paginate_records()

        elif choice == "6":

            name = input("Имя для удаления: ")

            delete_by_name(name)

        elif choice == "7":

            phone = input("Номер для удаления: ")

            delete_by_phone(phone)

        elif choice == "8":

            show_all()

        elif choice == "0":

            print("Выход.")

            break

        else:
            
            print("Неверный ввод. Попробуйте ещё раз.")

if __name__ == "__main__":

    create_table()
    
    menu()