def get_db_connection():
    return mysql.connector.connect (
        host="localhost",
        user="root"
        password="", #update is you set a MySQL password
        database="span_scan" #replace with your actual DB name
    )