from flask import Flask, jsonify

from mysql_connection import MySQLConnection

app = Flask(__name__)
db = MySQLConnection(
        host="123.31.12.175",
        user="rd_user",
        password="rduser@123",
        database="RD"
    )
db.get_connection()
cursor = db.get_cursor()


@app.route('/profile_info/<public_id>')
def profile_info(public_id):
    query = f"SELECT * FROM profile_info where public_id = {public_id};"
    cursor.execute(query)
    results = cursor.fetchall()
    return jsonify(results)


@app.route('/experience/<public_id>')
def experience(public_id):
    query = f"SELECT * FROM experience where public_id = {public_id};"
    cursor.execute(query)
    results = cursor.fetchall()
    return jsonify(results)


@app.route('/company_detail/<int:id>')
def company_detail(id):
    query = f"SELECT * FROM company_detail where cid = {id};"
    cursor.execute(query)
    results = cursor.fetchall()
    return jsonify(results)


@app.route('/job_posting/<int:id>')
def job_posting(id):
    query = f"SELECT * FROM job_posting where id = {id};"
    cursor.execute(query)
    results = cursor.fetchall()
    return jsonify(results)


@app.route('/job_posting/description/<int:id>')
def job_posting_description(id):
    query = f"SELECT description FROM job_posting where id = {id};"
    cursor.execute(query)
    results = cursor.fetchall()
    return f'<div style="padding: 3rem;">{results[0]["description"]}</div>'


if __name__ == "__main__":
    app.run(debug=True)

