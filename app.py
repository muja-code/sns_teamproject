import pymysql
from flask import Flask, render_template, request, json, jsonify, session, redirect, url_for
from flask_bcrypt import Bcrypt

app = Flask(__name__)

app.config["SECRET_KEY"] = "secret_pw_key"
app.config["BCRYPT_LEVEL"] = 10
bcrypt = Bcrypt(app)


@app.route('/')
def home():
   return render_template("main.html")

@app.route('/write')
def write():
    return render_template("write.html")

@app.route('/board', methods=['GET'])
def board():
    db = pymysql.connect(host='localhost', user='root', db='yogurt', password='810665', charset='utf8')
    curs = db.cursor()

    sql = "SELECT * FROM  board b inner JOIN `user` u ON b.user_id = u.id"

    curs.execute(sql)

    data_list = curs.fetchall()

    db.commit()
    db.close()

    return render_template('board.html', data_list=data_list)

@app.route('/<num>', methods=['GET'])
def view(num):
    db = pymysql.connect(host='localhost', user='root', db='yogurt', password='810665', charset='utf8')
    curs = db.cursor()

    sql = f"SELECT * FROM  board WHERE num = '{num}'"

    curs.execute(sql)

    rows = curs.fetchall()
    list = []
    for row in rows:
        list.append(row)

    db.commit()
    db.close()

    return render_template('view.html', list=list)

@app.route('/edit/<num>', methods=['GET'])
def correction(num):
    db = pymysql.connect(host='localhost', user='root', db='yogurt', password='810665', charset='utf8')
    curs = db.cursor()

    sql = f"SELECT * FROM board WHERE num = '{num}'"

    curs.execute(sql)

    rows = curs.fetchall()
    
    list = []
    for row in rows:
        list.append(row)

    db.commit()
    db.close()  

    return render_template('edit.html', list=list)

@app.route('/write/post', methods=['POST'])
def write_post():
    db = pymysql.connect(host='localhost', user='root', db='yogurt', password='810665', charset='utf8')
    curs = db.cursor()

    title = request.form["title"]
    cont = request.form["cont"]
    sql = f"INSERT INTO BOARD  (title, CONTENTS, NAME, `date`, user_id) VALUES(%s, %s, %s, NOW(), 1);"

    curs.execute(sql,(title, cont, "테스트8"))

    db.commit()
    db.close()

    return jsonify({'msg': '등록성공'})

@app.route('/<num>', methods=['POST'])
def hit(num):
    db = pymysql.connect(host='localhost', user='root', db='yogurt', password='810665', charset='utf8')
    curs = db.cursor()

    sql = f"update board set hit = hit + 1 where num = '{num}';"

    curs.execute(sql)
    return render_template("index.html")
    
@app.route("/<num>", methods=["DELETE"])
def delete_boadr(num):
    db = pymysql.connect(host='localhost', user='root', db='yogurt', password='810665', charset='utf8')
    curs = db.cursor()

    sql = f"DELETE FROM board WHERE num = '{num}'"
    curs.execute(sql)

    db.commit()
    db.close()

    return jsonify({'msg': '삭제 완료!'})

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
