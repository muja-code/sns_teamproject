from flask import Flask, render_template, request, redirect, url_for, jsonify
import pymysql
from sqlalchemy import create_engine, text

app = Flask(__name__)

db = pymysql.connect(host='localhost', user='root', db='yogurt', password='810665', charset='utf8')
curs = db.cursor()

@app.route('/')
def home():
   return render_template("main.html")

@app.route('/write')
def write():
    return render_template("write.html")

@app.route('/board/<user_name>', methods=['GET'])
def board(user_name):
    sql = f"SELECT * FROM  board b inner JOIN `user` u ON b.user_id = u.id WHERE user_name = '{user_name}'"

    curs.execute(sql)

    data_list = curs.fetchall()
    db.commit()
    db.close()

    return render_template('board.html', data_list=data_list)

@app.route('/<user_id>/<num>', methods=['GET'])
def view(user_id, num):
    sql = f"SELECT * FROM  board b inner JOIN `user` u ON b.user_id = u.id WHERE num = '{num}'"

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
    title = request.form["title"]
    cont = request.form["cont"]
    sql = f"INSERT INTO BOARD  (title, CONTENTS, NAME, `date`, user_id) VALUES(%s, %s, %s, NOW(), 1);"

    curs.execute(sql,(title, cont, "테스트8"))

    db.commit()
    db.close()

    return jsonify({'msg': '등록성공'})

@app.route('/hit/post', methods=['POST'])
def hit(num):
    sql = f"update board set hit = hit + 1 where num = 7;"

    curs.execute(sql)

    db.commit()
    db.close()

    return jsonify({'msg': '업데이트 성공'})

@app.route("/<num>", methods=["DELETE"])
def delete_boadr(num):

    sql = f"DELETE FROM board WHERE num = '{num}'"
    curs.execute(sql)
    db.commit()
    db.close()

    return jsonify({'msg': '삭제 완료!'})

if __name__ == '__main__':
    app.config.from_pyfile("config.py")
    database = create_engine(app.config['DB_URL'], encoding = 'utf-8', max_overflow = 0)
    app.database = database
    app.run('0.0.0.0', port=5000, debug=True)