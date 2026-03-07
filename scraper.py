from flask import jsonify
from db_config import get_db_connection
def signup_user(data):
    username=data.get('username')
    email=data.get('email')
    password=data.get('password')

    conn = get_db_connection()
    cursor = conn.cursor()

    #check if username already exists

    cursor.execute("SELECT * FROM login WHERE username = %s ", (username,))
    existing_user = cursor.fetchone()

    if existing_user:
        return jsonify({"success": False, "message" :"Username already exists"}), 409

    #Insert new user
    cursor.execute("INSERT INTO login (username,email,password) VALUE (%s, %s, %s)", (user)
    conn.commit()
    cursor.close()
    conn.close()

        return jsonify({"success": True , "meassage": "Signup successful"}), 201
def login_user(data):
    username = data.get('username')
    password=data.get('password')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM login WHERE username = %s AND password =%s",(username, F))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user:
        return jsonify({"success": True  "meassage": "Signup successful"}), 201
    else:
        return jsonify({"success": False, "message" :"Username already exists"}) 409

