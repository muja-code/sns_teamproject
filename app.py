import pymysql
from flask import Flask, render_template, request, json, jsonify, session, redirect, url_for
from flask_bcrypt import Bcrypt

app = Flask(__name__)

app.config["SECRET_KEY"] = "secret_pw_key"
app.config["BCRYPT_LEVEL"] = 10
bcrypt = Bcrypt(app)


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/users', methods=["POST"])
def create_users():
    db = pymysql.connect(host='localhost', user='root', db='yogurt', password='0000', charset='utf8')
    curs = db.cursor()

    user = request.json

    user_id = user["user_id"]
    user_pw = user["user_pw"]
    user_name = user["user_name"]
    user_email = user["user_email"]
    user_disc = user["user_disc"]

    pw_hash = bcrypt.generate_password_hash(user_pw)

    sql = '''INSERT INTO `user` (user_id, user_pw, user_name, user_email, user_disc) VALUES (%s, %s, %s, %s, %s)
      '''
    curs.execute(sql, (user_id, pw_hash, user_name, user_email, user_disc))

    db.commit()
    db.close()
    return 'insert success', 200


@app.route('/users/<id>', methods=["GET"])
def get_users(id):

    if id not in session:
        return redirect("/login")

    db = pymysql.connect(host='localhost', user='root', db='yogurt', password='0000', charset='utf8')
    curs = db.cursor()

    sql = '''SELECT user_id, user_name, user_email, user_disc FROM `user` AS u WHERE u.id=%s'''

    curs.execute(sql, id)

    rows = curs.fetchall()
    print(rows)
    db.commit()
    db.close()
    result = {
        "user_id": rows[0][0],
        "user_name": rows[0][1],
        "user_email": rows[0][2],
        "user_disc": rows[0][3]
    }

    return jsonify({'users': result}), 200


@app.route('/board', methods=["POST"])
def writing():

    if id not in session:
        return redirect("/login")

    db = pymysql.connect(host='localhost', user='root', db='yogurt', password='0000', charset='utf8')
    curs = db.cursor()

    board = request.json

    title = board["title"]
    contents = board["contents"]
    name = board["name"]
    date = board["date"]
    hit = board["hit"]
    user_id = board["user_id"]

    sql = '''
         INSERT INTO board (title, contents, name, date, hit, user_id) VALUES (%s, %s, %s, %s, %s, %s)
         '''
    curs.execute(sql, (title, contents, name, date, hit, user_id))

    db.commit()
    db.close()
    return 'insert success', 200


@app.route('/board/<id>', methods=["GET"])
def get_board(id):

    if id not in session:
        return redirect("/login")

    db = pymysql.connect(host='localhost', user='root', db='yogurt', password='0000', charset='utf8')
    curs = db.cursor()

    sql = """
      SELECT title, contents, name, hit
      FROM board as b
      LEFT JOIN `user` as u
      ON b.user_id = u.id WHERE b.user_id = %s
      """

    curs.execute(sql, id)

    rows = curs.fetchall()
    db.commit()
    db.close()

    json_str = json.dumps(rows, indent=4, sort_keys=True, default=str)

    return json_str, 200

@app.route('/login')
def login_page():
    return render_template("login.html")


@app.route('/login', methods=["POST"])
def login():
    db = pymysql.connect(host='localhost', user='root', db='yogurt', password='0000', charset='utf8')
    curs = db.cursor()

    user_id = request.form["id"]
    user_pw = request.form["pw"]

    sql = '''SELECT id, user_pw, user_name FROM `user` AS u WHERE u.user_id=%s;
   '''
    curs.execute(sql, user_id)

    rows = curs.fetchall()

    db.commit()
    db.close()

    is_login = bcrypt.check_password_hash(rows[0][1], user_pw)

    if is_login == False:
        return jsonify({'login': False}), 401

    session["id"] = rows[0][0]
    session["name"] = rows[0][2]
    return jsonify({'login': "succes"}), 200


@app.route('/logout', methods=["POST"])
def logout():
    session.clear()
    return jsonify({'msg': "logout secces!"}), 200


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
