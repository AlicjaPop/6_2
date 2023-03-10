import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn

def execute_sql(conn, sql):
    """ Execute sql
    :param conn: Connection object
    :param sql: a SQL script
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(sql)
    except Error as e:
        print(e)

def add_customer(conn, customer):
    """
    Create a new customer into customers table
    :param conn:
    :param customer:
    :retun: customer_id
    """
    sql='''INSERT INTO customers (customer_id, phone_number, email)
            VALUES(?,?,?)'''
    cur = conn.cursor()
    cur.execute(sql, customer)
    conn.commit()
    return cur.lastrowid

def add_order(conn, order):
    """
    Create a new order into orders table
    :param conn:
    :param order:
    :retun: order_number
    """
    sql='''INSERT INTO orders (customer_id, order_number, email)
            VALUES(?,?,?)'''
    cur = conn.cursor()
    cur.execute(sql, order)
    conn.commit()
    return cur.lastrowid

if __name__ == '__main__':

    create_orders_table="""
    CREATE TABLE IF NOT EXISTS orders (
    order_number integer PRIMARY KEY,
    customer_id integer,
    order_value float,
    FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
    );
    """

    create_customers_table="""
    CREATE TABLE IF NOT EXISTS customers (
    customer_id integer PRIMARY KEY,
    phone_number text,
    email text NOT NULL
    );
    """

    db_file="C:/Users/user/OneDrive/Desktop/Kodilla/6_2/Task_6_2_database.db"
    conn=create_connection(db_file)
    if conn is not None:
        execute_sql(conn, create_orders_table)
        execute_sql(conn, create_customers_table)
        conn.close()