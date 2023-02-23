import psycopg2
import urllib.parse as up
import os

def connect_to_db():
    up.uses_netloc.append("postgres")
    url = up.urlparse(os.environ["DATABASE_URL"])
    conn = psycopg2.connect(database=url.path[1:],
                            user=url.username,
                            password=url.password,
                            host=url.hostname,
                            port=url.port
                            )
    conn.autocommit = True
    return conn

def build_tables(conn):
    with conn.cursor() as cur:
        sql_create_hsc_performance_table = """
                                        CREATE TABLE IF NOT EXISTS hsc_performance(
                                        student_id text,
                                        course_id text,
                                        course text,
                                        school_assessment numeric,
                                        moderated_assessment numeric,
                                        exam_mark numeric,
                                        hsc_mark numeric,
                                        band text,
                                        notational_band text,
                                        uni_grade text,
                                        uni_grade_desc text,
                                        withheld_reason text);
                                        """
        cur.execute(sql_create_hsc_performance_table)
        print("Table Created....")

def tasks():
    conn = connect_to_db()
    #build_tables(conn)
    sample_login_table(conn)

def sample_login_table(conn): #Initialisation
    with conn.cursor() as cur:
        cur.execute(""" CREATE TABLE IF NOT EXISTS USERS (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        password VARCHAR(50) NOT NULL,
        hash VARBINARY(50),
        salt VARBINARY(50));
        """) #TODO: work out out to use a binary type to transfer from 'password' to 'hash' and 'salt'
        conn.commit()

        #Insert some sample users
        #cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", ("Agastya", "password1"))
        #conn.commit()

tasks()