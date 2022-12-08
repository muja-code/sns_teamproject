from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from flask_paginate import Pagination, get_page_args
# from flask_sqlalchemy import pagination
import pymysql

app = Flask(__name__)

ROWS_PER_PAGE = 8

@app.route('/')
def home():
   return render_template("main.html")

@app.route('/write')
def write():
    return render_template("write.html")

@app.route('/board', methods=['GET'])
def board():
    per_page = 8
    page, _, offset = get_page_args(per_page=per_page)  # 포스트 10개씩 페이지네이션

    db = pymysql.connect(host='localhost', user='root', db='yogurt', password='810665', charset='utf8')
    curs = db.cursor()

    curs.execute("SELECT COUNT(*) FROM board;")

    all_count = curs.fetchall()[0][0]

    curs.execute("SELECT * FROM board ORDER BY `date` DESC LIMIT %s OFFSET %s;", (per_page, offset))
    data_list = curs.fetchall()

    db.commit()
    db.close()

    pagination = Pagination(page=page, per_page=per_page, total=all_count, record_name='board', css_framework='foundation', bs_version=5)

    return render_template('board.html', data_lists=data_list, pagination=pagination)


@app.route('/board/<num>', methods=['GET'])
def view(num):
    db = pymysql.connect(host='localhost', user='root', db='yogurt', password='810665', charset='utf8')
    curs = db.cursor()

    sql = f"update board set hit = hit + 1 where num = {num};"

    curs.execute(sql)

    sql = f"SELECT * FROM  board WHERE num = '{num}'"

    curs.execute(sql)

    rows = curs.fetchall()
    list = []
    for row in rows:
        list.append(row)
    
    
    db.commit()
    db.close()

    return render_template('view.html', list=list)

@app.route('/edit_board/<num>', methods=['GET'])
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

@app.route('/board', methods=['POST'])
def write_post():
    db = pymysql.connect(host='localhost', user='root', db='yogurt', password='810665', charset='utf8')
    curs = db.cursor()
    
    title = request.form["subject"]
    cont = request.form["contents"]

    # if title == "" or cont == "":
    #     return flash

    sql = f"INSERT INTO BOARD  (title, CONTENTS, NAME, `date`, user_id) VALUES(%s, %s, %s, NOW(), 1);"

    curs.execute(sql,(title, cont, "테스트8"))

    db.commit()
    db.close()

    return redirect('/board')

@app.route('/edit_board/<num>', methods=['POST'])
def edit(num):
    db = pymysql.connect(host='localhost', user='root', db='yogurt', password='810665', charset='utf8')
    curs = db.cursor()

    title = request.form["subject"]
    cont = request.form["contents"]

    sql = f"UPDATE board SET title = %s, contents = %s WHERE num = '{num}';"

    curs.execute(sql, (title, cont))

    db.commit()
    db.close()

    return redirect(f'/board/{num}')

@app.route("/board/<num>", methods=["DELETE"])
def delete_boadr(num):
    db = pymysql.connect(host='localhost', user='root', db='yogurt', password='810665', charset='utf8')
    curs = db.cursor()

    sql = f"DELETE FROM board WHERE num = '{num}'"
    curs.execute(sql)

    db.commit()
    db.close()

    return jsonify({'msg': '삭제 완료!'})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)