import psycopg2

# Connect to the PostgreSQL server
def connect():
    try:
        conn = psycopg2.connect(user="dsUser", 
                            password="Lahticity2", 
                            host="services-ds-project.postgres.database.azure.com", 
                            port=5432, 
                            database="postgres")
        print("Connected to PostgreSQL!")            

    # Create a cursor and execute something simple
        cur = conn.cursor()
        cur.execute("SELECT version();")
        record = cur.fetchone()
        print("PostgreSQL version:", record)

        return conn


    except Exception as e:
        print("Failed to connect:", e)

connect()