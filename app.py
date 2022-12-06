from flask import Flask, render_template, request, redirect, url_for, jsonify
import pymysql


app = Flask(__name__)



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

@app.route('/board', methods=['POST'])
def write_post():
    db = pymysql.connect(host='localhost', user='root', db='yogurt', password='810665', charset='utf8')
    curs = db.cursor()

    title = request.form["subject"]
    cont = request.form["contents"]
    sql = f"INSERT INTO BOARD  (title, CONTENTS, NAME, `date`, user_id) VALUES(%s, %s, %s, NOW(), 1);"

    curs.execute(sql,(title, cont, "테스트8"))

    db.commit()
    db.close()

    return redirect('/board')

@app.route('/edit/<num>', methods=['POST'])
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

# @app.route('/board/<num>', methods=['POST'])
# def hit(num):
#     db = pymysql.connect(host='localhost', user='root', db='yogurt', password='810665', charset='utf8')
#     curs = db.cursor()

    

#     db.commit()
#     db.close()

#     return jsonify({'msg': '업데이트 성공'})

@app.route("/<num>", methods=["DELETE"])
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