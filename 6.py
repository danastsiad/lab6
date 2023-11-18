from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI()

def connect_to_database():
    return sqlite3.connect('shop.db')

def create_table():
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    surname TEXT NOT NULL,
    telephone TEXT NULL
    )
    ''')
    connection.commit()
    connection.close()
    
def insert_user(name, surname, telephone):
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute('INSERT INTO Users (name, surname, telephone) VALUES (?, ?, ?)', (name, surname, telephone))
    connection.commit()
    connection.close()

def select_all_users():
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM Users')
    users = cursor.fetchall()

    for user in users:
        print(user)

    connection.close()

def select_user_by_surname(surname):
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute('SELECT name, surname, telephone From Users WHERE surname = ? ', (surname,))
    results = cursor.fetchall()

    for row in results:
        print(row)

    connection.close()

def update_telephone_by_surname(surname, new_telephone):
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute('UPDATE Users SET telephone = ? WHERE surname = ?', (new_telephone, surname))
    connection.commit()
    connection.close()

def delete_user_by_surname(surname):
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute('DELETE FROM Users WHERE surname = ?', (surname,))
    connection.commit()
    connection.close()

def main():
    create_table()

    while True:
        print('Выберите дейтсвие:')
        print('1. Добавить нового пользователя')
        print('2. Просмотреть всех пользователей')
        print('3. Найти пользователя по фамилии')
        print('4. Изменить номер телефона по фамилии')
        print('5. Удалить пользователя')
        print('0. Выйти')

        choise = int(input('Введите номер действия: '))

        match choise:
            case 1:
                name = input('Имя: ')
                surname = input('Фамилия: ')
                telephone = input('Телефон: ')
                insert_user(name, surname, telephone)
                print('Пользователь добавлен')
            case 2:
                print('Таблица пользователей')
                select_all_users()
            case 3:
                surname = input('Введите фамилию пользователя для поиска: ')
                select_user_by_surname(surname)
            case 4:
                surname = input('Введите фамилию пользователя для изменения номера телефона: ')
                new_telephone = input('Введите новый номер телефона: ')
                update_telephone_by_surname(surname, new_telephone)
                print('Номер телефона обновлен')
            case 5:
                surname = input('Введите фамилию пользователя для удаления: ')
                delete_user_by_surname(surname)
                print('Пользователь удален')
            case 0:
                print('Выход выполнен')
                break


class UserCreate(BaseModel):
    name: str
    surname: str
    telephone: str = None

class UserUpdateTelephone(BaseModel):
    telephone: str    

@app.post("/users/", response_model=UserCreate)
async def create_user(user: UserCreate):
    insert_user(user.name, user.surname, user.telephone)
    return user

@app.get("/users/")
async def read_users():
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute('SELECT name, surname, telephone From Users')
    users = cursor.fetchall()
    connection.close()
    return {"Пользователи": users}


@app.get("/users/{surname}")
async def read_users_by_surname(surname: str):
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute('SELECT name, surname, telephone From Users WHERE surname = ?', (surname,))
    users = cursor.fetchall()
    connection.close()
    
    return {"Пользователи": users}

@app.put("/users/{surname}")
async def update_telephone_by_surname(surname: str, user_update: UserUpdateTelephone):
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute('UPDATE Users SET telephone = ? WHERE surname = ?', (user_update.telephone, surname))
    connection.commit()
    connection.close()

    return {"message": f"Номер телефона {surname} обновлен."}

@app.delete("/users/{surname}")
async def delete_user_by_surname(surname: str):
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute('DELETE FROM Users WHERE surname = ?', (surname,))
    connection.commit()
    connection.close()

    return {"message": f"Пользователь {surname} удален."}

if __name__ == '__main__':
    main()

