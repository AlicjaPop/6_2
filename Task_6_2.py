import random
from faker import Faker
fake=Faker()

import sqlite3
from sqlite3 import Error

# Functions
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
    sql='''INSERT INTO customers (customer_id, name, email)
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
    sql='''INSERT INTO orders (order_number, customer_id, order_value)
            VALUES(?,?,?)'''
    cur = conn.cursor()
    cur.execute(sql, order)
    conn.commit()
    return cur.lastrowid

def all_records(conn, table):
   """
   Query all rows in the table
   :param conn: the Connection object
   :return:
   """
   cur = conn.cursor()
   cur.execute(f"SELECT * FROM {table}")
   rows = cur.fetchall()
   return rows

def filter(conn, table, **query):
   """
   Query tasks from table with data from **query dict
   :param conn: the Connection object
   :param table: table name
   :param query: dict of attributes and values
   :return:
   """
   cur = conn.cursor()
   qs = []
   values = ()
   for k, v in query.items():
       qs.append(f"{k}=?")
       values += (v,)
   q = " AND ".join(qs)
   cur.execute(f"SELECT * FROM {table} WHERE {q}", values)
   rows = cur.fetchall()
   return rows

def update_customer(conn, customer_id, **kwargs):
   """
   update status, begin_date, and end date of a task
   :param conn:
   :param table: table name
   :param id: row id
   :return:
   """
   parameters = [f"{k} = ?" for k in kwargs]
   parameters = ", ".join(parameters)
   values = tuple(v for v in kwargs.values())
   values += (customer_id, )

   sql = f''' UPDATE customers
             SET {parameters}
             WHERE customer_id = ?'''
   try:
       cur = conn.cursor()
       cur.execute(sql, values)
       conn.commit()
       print("Updated")
   except sqlite3.OperationalError as e:
       print(e)

def update_order(conn, order_number, **kwargs):
   """
   update status, begin_date, and end date of a task
   :param conn:
   :param table: table name
   :param id: row id
   :return:
   """
   parameters = [f"{k} = ?" for k in kwargs]
   parameters = ", ".join(parameters)
   values = tuple(v for v in kwargs.values())
   values += (order_number, )

   sql = f''' UPDATE orders
             SET {parameters}
             WHERE order_number = ?'''
   try:
       cur = conn.cursor()
       cur.execute(sql, values)
       conn.commit()
       print("Updated")
   except sqlite3.OperationalError as e:
       print(e)

def delete_customer(conn, **kwargs):
   """
   Delete from table where attributes from
   :param conn:  Connection to the SQLite database
   :param table: table name
   :param kwargs: dict of attributes and values
   :return:
   """
   qs = []
   values = tuple()
   for k, v in kwargs.items():
       qs.append(f"{k}=?")
       values += (v,)
   q = " AND ".join(qs)

   sql = f'DELETE FROM customers WHERE {q}'
   cur = conn.cursor()
   cur.execute(sql, values)
   conn.commit()
   print("Deleted")

def delete_order(conn, **kwargs):
   """
   Delete from table where attributes from
   :param conn:  Connection to the SQLite database
   :param table: table name
   :param kwargs: dict of attributes and values
   :return:
   """
   qs = []
   values = tuple()
   for k, v in kwargs.items():
       qs.append(f"{k}=?")
       values += (v,)
   q = " AND ".join(qs)

   sql = f'DELETE FROM orders WHERE {q}'
   cur = conn.cursor()
   cur.execute(sql, values)
   conn.commit()
   print("Deleted")

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
    name text,
    email text NOT NULL
    );
    """
# File path
    db_file="C:/Users/user/OneDrive/Desktop/Kodilla/6_2/Task_6_2_database.db"

# Connection
    conn=create_connection(db_file)

    if conn is not None:

# Tables creation
        execute_sql(conn, create_orders_table)
        execute_sql(conn, create_customers_table)


# Tables fill-out

        for i in range(10):
            customer_id=i+1
            name=str(fake.name())
            email=str(fake.email())
            customer=(customer_id, name, email)
            add_customer(conn, customer)

        for i in range(10):
            order_number=i+1
            customer_id=random.randint(1,10)
            order_value=float(random.randint(100,200))
            order=(order_number, customer_id, order_value)
            add_order(conn, order)


        customer_11=(11, str(fake.name()), str(fake.email()))
        customer_12=(12, str(fake.name()), str(fake.email()))
        customer_13=(13, str(fake.name()), str(fake.email()))

        order_11=(11,3,230.55)
        order_12=(12,2,450.12)
        order_13=(13,1,660.76)

# Adding records

        add_order(conn, order_11)
        add_order(conn, order_12)
        add_order(conn, order_13)

        add_customer(conn, customer_11)
        add_customer(conn, customer_12)
        add_customer(conn, customer_13)

# Filtering
        print(all_records(conn, "orders"))
        print(filter(conn, "orders", order_number=1))

# Records update

        update_order(conn, 3, order_value=765.98)
        update_customer(conn, 1, email="aaa@aaa.pl")

        print(filter(conn, "orders", order_number=3))
        print(filter(conn, "customers", customer_id=1))

# Records deletion

        delete_customer(conn, customer_id=1)
        delete_order(conn, order_number=2)

        print(all_records(conn, "orders"))
        print(all_records(conn, "customers"))


        conn.close()