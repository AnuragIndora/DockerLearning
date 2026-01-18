from flask import Flask
import pymysql


app = Flask(__name__)

@app.route("/")
def home():
    return "Docker Network Adapters Tutorial ..."

@app.route("/insert_data")
def insert_data():
    
    # connect to the database 
    connection = pymysql.connect(
        host='mysql_cont',
        user='root',
        password='12345678',
        database='demodb'
    )

    # Create a cursor object 
    cursor = connection.cursor()

    # Insert data into the database 
    insert_query = "INSERT INTO users (city, temp) VALUES (%s, %s)"

    data = ("NEW YORK", 25)

    cursor.execute(insert_query, data)

    # commit the transaction 
    connection.commit()
    cursor.close()
    connection.close()

    return "Data Inserted Successfully!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)