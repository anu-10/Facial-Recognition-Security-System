import sqlite3

def create_main(db):
    connection = sqlite3.connect(db)
    query = '''CREATE TABLE IF NOT EXISTS MAIN(
                PRN INT PRIMARY KEY,
                NAME TEXT);
            '''
    connection.execute(query)
    connection.close()

def add_to_main(db, prn, name):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    query = "SELECT PRN FROM MAIN WHERE PRN = ?"
    cursor.execute(query, [prn])
    result = cursor.fetchone()
    if result:
        result = 0
    else:
        query = '''INSERT INTO MAIN
                    (PRN, NAME)
                    VALUES(?,?);
                '''
        conn.execute(query,[prn, name]) 
        conn.commit()
        result = 1
    conn.close()
    return result

def remove_from_main(db, prn):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    query = "SELECT PRN FROM MAIN WHERE PRN = ?"
    cursor.execute(query, [prn])
    result = cursor.fetchone()
    if not result:
        result = 0
    else:
        query = '''DELETE FROM MAIN
                    WHERE PRN = ?;
                '''
        conn.execute(query,[prn]) 
        conn.commit()
        result = 1
    conn.close()
    return result

def search_main(db, prn):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    query = "SELECT PRN, NAME FROM MAIN WHERE PRN = ?"
    cursor.execute(query, [prn])
    result = cursor.fetchone()
    conn.close()
    return result
    
def view_main(db):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    query = "SELECT PRN, NAME FROM MAIN ORDER BY PRN"
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return result
    
def create_accounts(db):
    connection = sqlite3.connect(db)
    query = '''CREATE TABLE IF NOT EXISTS ACCOUNTS(
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                USER TEXT,
                PASSWORD TEXT);
            '''
    connection.execute(query)
    connection.close()

def add_user(db, user, pwd):
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    query = "SELECT USER FROM ACCOUNTS WHERE USER = ?"
    cursor.execute(query, [user])
    result = cursor.fetchone()
    if result:
        result = 0
    else:
        query = '''INSERT INTO ACCOUNTS
                    (USER, PASSWORD)
                    VALUES(?,?);
                '''
        connection.execute(query,[user, pwd]) 
        connection.commit()
        result = 1
    connection.close()
    return result

def user_exists(db, user, pwd):
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    query = '''SELECT USER FROM ACCOUNTS WHERE (USER = ? AND PASSWORD = ?);
            '''
    cursor.execute(query, [user, pwd])
    result = cursor.fetchone()
    connection.close()
    return result

def remove_user(db, user):
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    query = '''SELECT USER FROM ACCOUNTS WHERE USER = ?;
            '''
    cursor.execute(query, [user])
    result = cursor.fetchone()
    if result:
        query = '''DELETE FROM ACCOUNTS WHERE USER = ?;'''
        cursor.execute(query, [user])
        connection.commit()
        result = 1
    else:
        result = 0
    connection.close()
    return result
        

"""from IPython.display import Image

if __name__ == '__main__':
    database = 'C:\Programming\Application\Database\data.db'
    create_main(database)
    print('Enter prn and name.')
    prn = 20070122022#int(input())
    name = 'Anupam Muralidharan'#input()
    result = add_to_main(database, prn, name)
    if result:
        print("ADDED PRN")
    else:
        print("PRN EXISTS")
    
    #display_database(database)"""