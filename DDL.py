import mysql.connector


def create_database(database_name):
    config = {'user': 'root', 'password': 'password', 'host': 'localhost', 'auth_plugin': 'mysql_native_password'}
    conn = mysql.connector.connect(**config)
    c = conn.cursor(dictionary=True)
    c.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
    print(f'database "{database_name}" created')

def create_customer_table():
    config = {'user': 'root', 'password': 'password', 'host': 'localhost', 'database': 'pet_shop', 'auth_plugin': 'mysql_native_password'}
    conn = mysql.connector.connect(**config)
    c = conn.cursor(dictionary=True)
    c.execute("""CREATE TABLE customer (
        customer_id         bigint primary key,
        customer_first_name varchar(50) NOT NULL,
        customer_last_name  varchar(50),
        phone_num           varchar(15),
        address             text,
        zip_code            int,
        email               varchar(100),
        join_date           datetime not null default current_timestamp
    )""")
    print('customer table created')
    
def create_product_table():
    config = {'user': 'root', 'password': 'password', 'host': 'localhost', 'database': 'pet_shop', 'auth_plugin': 'mysql_native_password'}
    conn = mysql.connector.connect(**config)
    c = conn.cursor(dictionary=True)
    c.execute("""CREATE TABLE product (
        product_id   int not null auto_increment primary key,
        product_name varchar(100) not null,
        price        bigint,
        inventory    int,
        category     enum('dog_food','cat_food','toy','tool','furniture'),
        description  text,
        message_id   int not null
    )""")
    print('product table created')

def create_sale_table():
    config = {'user': 'root', 'password': 'password', 'host': 'localhost', 'database': 'pet_shop', 'auth_plugin': 'mysql_native_password'}
    conn = mysql.connector.connect(**config)
    c = conn.cursor(dictionary=True)
    c.execute("""CREATE TABLE sale (
        sale_id     int primary key,
        date        datetime not null default current_timestamp,
        customer_id bigint,
        constraint fk_cost foreign key (customer_id) references customer(customer_id)
    )""")
    print('sale table created')

def create_sale_row_table():
    config = {'user': 'root', 'password': 'password', 'host': 'localhost', 'database': 'pet_shop', 'auth_plugin': 'mysql_native_password'}
    conn = mysql.connector.connect(**config)
    c = conn.cursor(dictionary=True)
    c.execute("""CREATE TABLE sale_row (
        sale_id    int,
        product_id int,
        quantity   tinyint,
        constraint fk_sale foreign key (sale_id) references sale(sale_id),
        constraint fk_product foreign key (product_id) references product(product_id)
    )""")
    print('sale_row table created')


if __name__ == '__main__':
    create_database("pet_shop")
    create_customer_table()
    create_product_table()
    create_sale_table()
    create_sale_row_table()