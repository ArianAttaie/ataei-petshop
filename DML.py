import mysql.connector


def insert_product_info(product_name, price, inventory, category, description, message_id):
    config = {'user': 'root', 'password': 'password', 'host': 'localhost', 'database': 'pet_shop'}
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    SQL_Query = """INSERT IGNORE INTO product
                    (product_name, price, inventory, category, description, message_id)
                    VALUES (%s, %s, %s, %s, %s, %s)"""
    cursor.execute(SQL_Query, (product_name, price, inventory, category, description, message_id))
    code = cursor.lastrowid
    conn.commit()
    conn.close()
    print(f'item {code} inserted to product table')

def change_product_inventory(code, amount):
    config = {'user': 'root', 'password': 'password', 'host': 'localhost', 'database': 'pet_shop'}
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    cursor.execute("UPDATE product SET inventory=inventory-%s WHERE product_id=%s", (code, amount))
    conn.commit()
    conn.close()
    print(f'item {code} updated in product table')

def insert_customer_info(customer_id, customer_first_name, customer_last_name=None, phone_num=None, address=None, zip_code=None, email=None):
    config = {'user': 'root', 'password': 'password', 'host': 'localhost', 'database': 'pet_shop'}
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    SQL_Query = """INSERT IGNORE INTO customer
                    (customer_id, customer_first_name, customer_last_name, phone_num, address, zip_code, email)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)"""
    cursor.execute(SQL_Query, (customer_id, customer_first_name, customer_last_name, phone_num, address, zip_code, email))
    conn.commit()
    conn.close()
    print(f'user {customer_id} inserted into customer table')

def insert_sale_info(customer_id, product_id, quantity):
    config = {'user': 'root', 'password': 'password', 'host': 'localhost', 'database': 'pet_shop'}
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    SQL_Query = """INSERT IGNORE INTO sale
                    (customer_id, product_id, quantity)
                    VALUES (%s, %s, %s)"""
    cursor.execute(SQL_Query, (customer_id, product_id, quantity))
    conn.commit()
    conn.close()
    print('new sale inserted into sale table')

def update_customer_info(customer_id, customer_first_name, customer_last_name = None, phone_num=None, address=None, zip_code=None, email=None):
    config = {'user': 'root', 'password': 'password', 'host': 'localhost', 'database': 'pet_shop'}
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    SQL_Query = """UPDATE customer SET customer_first_name=%s, customer_last_name=%s, phone_num=%s, address=%s, zip_code=%s, email=%s WHERE customer_id=%s"""
    cursor.execute(SQL_Query, (customer_first_name, customer_last_name, phone_num, address, zip_code, email, customer_id))
    conn.commit()
    conn.close()
    print(f'user {customer_id} updated from customer table')

def update_customer_first_name(customer_id, customer_first_name):
    config = {'user': 'root', 'password': 'password', 'host': 'localhost', 'database': 'pet_shop'}
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    SQL_Query = """UPDATE customer SET customer_first_name=%s WHERE customer_id=%s"""
    cursor.execute(SQL_Query, (customer_first_name, customer_id))
    conn.commit()
    conn.close()
    print(f'user {customer_id} updated from customer table')

def update_customer_last_name(customer_id, customer_last_name):
    config = {'user': 'root', 'password': 'password', 'host': 'localhost', 'database': 'pet_shop'}
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    SQL_Query = """UPDATE customer SET customer_last_name=%s WHERE customer_id=%s"""
    cursor.execute(SQL_Query, (customer_last_name, customer_id))
    conn.commit()
    conn.close()
    print(f'user {customer_id} updated from customer table')

def update_customer_phone_num(customer_id, customer_phone_num):
    config = {'user': 'root', 'password': 'password', 'host': 'localhost', 'database': 'pet_shop'}
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    SQL_Query = """UPDATE customer SET phone_num=%s WHERE customer_id=%s"""
    cursor.execute(SQL_Query, (customer_phone_num, customer_id))
    conn.commit()
    conn.close()
    print(f'user {customer_id} updated from customer table')

def update_customer_address(customer_id, customer_address):
    config = {'user': 'root', 'password': 'password', 'host': 'localhost', 'database': 'pet_shop'}
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    SQL_Query = """UPDATE customer SET address=%s WHERE customer_id=%s"""
    cursor.execute(SQL_Query, (customer_address, customer_id))
    conn.commit()
    conn.close()
    print(f'user {customer_id} updated from customer table')

def update_customer_zip_code(customer_id, customer_zip_code):
    config = {'user': 'root', 'password': 'password', 'host': 'localhost', 'database': 'pet_shop'}
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    SQL_Query = """UPDATE customer SET zip_code=%s WHERE customer_id=%s"""
    cursor.execute(SQL_Query, (customer_zip_code, customer_id))
    conn.commit()
    conn.close()
    print(f'user {customer_id} updated from customer table')

def update_customer_email(customer_id, customer_email):
    config = {'user': 'root', 'password': 'password', 'host': 'localhost', 'database': 'pet_shop'}
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    SQL_Query = """UPDATE customer SET email=%s WHERE customer_id=%s"""
    cursor.execute(SQL_Query, (customer_email, customer_id))
    conn.commit()
    conn.close()
    print(f'user {customer_id} updated from customer table')
    

if __name__ == '__main__':
    pass