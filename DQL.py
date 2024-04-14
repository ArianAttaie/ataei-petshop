import mysql.connector



def dog_food_products():
    config = {'user': 'root', 'password': 'password', 'host': 'localhost', 'database': 'pet_shop'}
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT product_id, product_name, inventory, message_id FROM product WHERE category='dog_food'")
    res = cursor.fetchall()
    return res

def cat_food_products():
    config = {'user': 'root', 'password': 'password', 'host': 'localhost', 'database': 'pet_shop'}
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT product_id, product_name, inventory, message_id FROM product WHERE category='cat_food'")
    res = cursor.fetchall()
    return res

def toy_products():
    config = {'user': 'root', 'password': 'password', 'host': 'localhost', 'database': 'pet_shop'}
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT product_id, product_name, inventory, message_id FROM product WHERE category='toy'")
    res = cursor.fetchall()
    return res

def tool_products():
    config = {'user': 'root', 'password': 'password', 'host': 'localhost', 'database': 'pet_shop'}
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT product_id, product_name, inventory, message_id FROM product WHERE category='tool'")
    res = cursor.fetchall()
    return res

def furniture_products():
    config = {'user': 'root', 'password': 'password', 'host': 'localhost', 'database': 'pet_shop'}
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT product_id, product_name, inventory, message_id FROM product WHERE category='furniture'")
    res = cursor.fetchall()
    return res

def get_product_info(product_id):
    config = {'user': 'root', 'password': 'password', 'host': 'localhost', 'database': 'pet_shop'}
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM product WHERE product_id={product_id}")
    res = cursor.fetchall()
    return res

def get_customer_info(customer_id):
    config = {'user': 'root', 'password': 'password', 'host': 'localhost', 'database': 'pet_shop'}
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM customer WHERE customer_id={customer_id}")
    res = cursor.fetchall()
    return res