import sqlite3


def connect_database():
    con = sqlite3.connect('database.sqlite')
    return con


def create_table():
    try:
        with connect_database() as conn:
            sql = '''CREATE TABLE IF NOT EXISTS iitems (id INTEGER PRIMARY KEY,userid INTEGER NOT NULL, itemid INTEGER NOT NULL, shopid INTEGER NOT NULL, schedule TEXT NOT NULL,UNIQUE(userid, itemid, shopid))'''
            conn.execute(sql)
            conn.commit()
            print('Created table')
    except Exception as err:
        print(f'create error -> {err}')


def insert_item(item):
    inserted_item = {}
    try:
        with connect_database() as conn:
            cur = conn.cursor()
            sql = '''INSERT INTO iitems (userid, itemid, shopid, schedule) VALUES (?,?,?,?)'''
            param = [item['userid'], item['itemid'],
                     item['shopid'], item['schedule']]
            cur.execute(sql, param)
            conn.commit()
            inserted_item = get_item_by_id(cur.lastrowid)
            print('saved item')
    except Exception as err:
        conn.rollback()
        inserted_item['error'] = 'data may be duplicated'
        print(f'insert error -> {err}')
    return inserted_item


def update_item(item):
    updated_item = {}
    try:
        with connect_database() as conn:
            cur = conn.cursor()
            sql = '''UPDATE iitems SET userid = ?, itemid = ?, shopid = ?, schedule = ? WHERE id = ?'''
            param = (item['userid'], item['itemid'],
                     item['shopid'], item['schedule'], item['id'])
            cur.execute(sql, param)
            conn.commit()
            updated_item = get_item_by_id(item['id'])
            print('updated item')
    except Exception as err:
        conn.rollback()
        updated_item['error'] = 'error update'
        print(f'update error -> {err}')
    return updated_item


def delete_item(id: int):
    message = {}
    try:
        with connect_database() as conn:
            sql = '''DELETE FROM iitems WHERE id = ?'''
            param = [id]
            conn.execute(sql, param)
            conn.commit()
            message['status'] = 'item deleted successfully'
            print(f'deleted data -> {id})')
    except Exception as err:
        conn.rollback()
        message['error'] = 'Cannot delete item'
        print(f'delete error -> {err}')
    return message


def delete_all_item():
    message = {}
    try:
        with connect_database() as conn:
            sql = '''DELETE FROM iitems'''
            conn.execute(sql)
            conn.commit()
            message['status'] = 'item deleted successfully'
            print('deleted all item')
    except Exception as err:
        conn.rollback()
        message['error'] = 'Cannot delete all item'
        print(f'delete error -> {err}')
    return message


def get_item_by_id(id: int):
    item = {}
    try:
        with connect_database() as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            sql = '''SELECT * FROM iitems WHERE id = ?'''
            param = [id]
            cur.execute(sql, param)
            row = cur.fetchone()

            item['id'] = row['id']
            item['userid'] = row['userid']
            item['itemid'] = row['itemid']
            item['shopid'] = row['shopid']
            item['schedule'] = row['schedule']

            print(f'get item by id -> {item}')
    except Exception as err:
        item['data'] = None
        print(f'get item by id error -> {err}')
    return item


def get_items():
    items = []
    try:
        with connect_database() as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            sql = '''SELECT * FROM iitems'''
            cur.execute(sql)
            rows = cur.fetchall()
            for row in rows:
                item = {}
                item['id'] = row['id']
                item['userid'] = row['userid']
                item['itemid'] = row['itemid']
                item['shopid'] = row['shopid']
                items.append(item)
        print(f'get show item -> {items}')
    except Exception as err:
        items = []
        print(f'get error -> {err}')
    return items
