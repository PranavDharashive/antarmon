import sqlite3
from sqlite3 import Error

DATABASE_FILE = "antarmon.db"

def create_connection():
    """ create a database connection to the SQLite database """
    conn = None;
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        return conn
    except Error as e:
        print(e)

    return conn

def create_table(conn):
    """ create a table from the create_table_sql statement """
    create_table_sql = """ CREATE TABLE IF NOT EXISTS metrics (
                                        id integer PRIMARY KEY,
                                        hostname text NOT NULL,
                                        cpu_percent real NOT NULL,
                                        memory_percent real NOT NULL,
                                        disk_percent real NOT NULL,
                                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                                    ); """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def insert_metric(conn, metric):
    """ Create a new metric into the metrics table """
    sql = ''' INSERT INTO metrics(hostname,cpu_percent,memory_percent,disk_percent)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, metric)
    conn.commit()
    return cur.lastrowid

def get_all_metrics(conn):
    """ Query all rows in the metrics table """
    cur = conn.cursor()
    cur.execute("SELECT * FROM metrics ORDER BY timestamp DESC")

    rows = cur.fetchall()
    return rows

def create_user(conn, user):
    """ Create a new user """
    sql = ''' INSERT INTO users(email,hashed_password)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, user)
    conn.commit()
    return cur.lastrowid

def get_user_by_email(conn, email):
    """ Query user by email """
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email=?", (email,))

    row = cur.fetchone()
    return row

def create_agent(conn, agent):
    """ Create a new agent """
    sql = ''' INSERT INTO agents(name,api_key,user_id)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, agent)
    conn.commit()
    return cur.lastrowid

def get_agent_by_api_key(conn, api_key):
    """ Query agent by api_key """
    cur = conn.cursor()
    cur.execute("SELECT * FROM agents WHERE api_key=?", (api_key,))

    row = cur.fetchone()
    return row

def get_agents_by_user_id(conn, user_id):
    """ Query all agents for a user """
    cur = conn.cursor()
    cur.execute("SELECT * FROM agents WHERE user_id=?", (user_id,))

    rows = cur.fetchall()
    return rows

def create_alert(conn, alert):
    """ Create a new alert """
    sql = ''' INSERT INTO alerts(metric_name,threshold,user_id)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, alert)
    conn.commit()
    return cur.lastrowid

def get_alerts_by_user_id(conn, user_id):
    """ Query all alerts for a user """
    cur = conn.cursor()
    cur.execute("SELECT * FROM alerts WHERE user_id=?", (user_id,))

    rows = cur.fetchall()
    return rows

def get_all_alerts(conn):
    """ Query all alerts """
    cur = conn.cursor()
    cur.execute("SELECT * FROM alerts")

    rows = cur.fetchall()
    return rows

def delete_alert(conn, alert_id):
    """ Delete an alert by alert id """
    sql = 'DELETE FROM alerts WHERE id=?'
    cur = conn.cursor()
    cur.execute(sql, (alert_id,))
    conn.commit()

def create_users_table(conn):
    """ create a users table """
    create_table_sql = """ CREATE TABLE IF NOT EXISTS users (
                                        id integer PRIMARY KEY,
                                        email text NOT NULL UNIQUE,
                                        hashed_password text NOT NULL
                                    ); """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def create_agents_table(conn):
    """ create an agents table """
    create_table_sql = """ CREATE TABLE IF NOT EXISTS agents (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        api_key text NOT NULL UNIQUE,
                                        user_id integer NOT NULL,
                                        FOREIGN KEY (user_id) REFERENCES users (id)
                                    ); """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def create_alerts_table(conn):
    """ create an alerts table """
    create_table_sql = """ CREATE TABLE IF NOT EXISTS alerts (
                                        id integer PRIMARY KEY,
                                        metric_name text NOT NULL,
                                        threshold real NOT NULL,
                                        user_id integer NOT NULL,
                                        FOREIGN KEY (user_id) REFERENCES users (id)
                                    ); """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def initialize_database():
    conn = create_connection()
    if conn is not None:
        create_table(conn)
        create_users_table(conn)
        create_agents_table(conn)
        create_alerts_table(conn)
        conn.close()
    else:
        print("Error! cannot create the database connection.")
