import os

import pymysql
from flask import Flask, render_template, request, jsonify, session, redirect, flash
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename

from flask_paginate import Pagination, get_page_args

app = Flask(__name__)

app.config["SECRET_KEY"] = "secret_pw_key"
app.config["BCRYPT_LEVEL"] = 10
bcrypt = Bcrypt(app)

UPLOAD_FOLDER = 'static/img'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    image = '< img src = "data:image/png;base64,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" >'

    per_page = 8
    page, _, offset = get_page_args(per_page=per_page)  # 포스트 10개씩 페이지네이션
    print(page, _, offset)

    db = pymysql.connect(host='localhost', user='root', db='yogurt', password='0000', charset='utf8')
    curs = db.cursor()

    curs.execute("SELECT COUNT(*) FROM board;")

    all_count = curs.fetchall()[0][0]

    curs.execute("SELECT * FROM board ORDER BY `date` DESC LIMIT %s OFFSET %s;", (per_page, offset))
    data_list = curs.fetchall()

    db.commit()
    db.close()

    pagination = Pagination(page=page, per_page=per_page, total=all_count, record_name='board',
                            css_framework='foundation', bs_version=5)
    if "id" not in session:
        id = None;
        name = None;
        return render_template('main.html', data_lists=data_list, pagination=pagination, id=id, name=name)

    return render_template('main.html', data_lists=data_list, pagination=pagination, id=session["id"],
                           name=session["name"], css_framework='foundation', bs_version=5, image=image)


@app.route('/users')
def user_page():
    return render_template("creat_user.html")


@app.route("/users", methods=["POST"])
def login_info_post():
    db = pymysql.connect(host='localhost', user='root', password='0000', database='yogurt', charset='utf8')
    cursor = db.cursor()

    user_id_receive = request.form['user_id_give']
    user_pass_receive = request.form['user_pass1_give']
    name_receive = request.form['name_give']
    email_receive = request.form['email_give']

    pw_hash = bcrypt.generate_password_hash(user_pass_receive)

    sql = 'INSERT INTO `user` (user_id, user_pw, user_name, user_email) values(%s, %s, %s, %s)'
    cursor.execute(sql, (user_id_receive, pw_hash, name_receive, email_receive))

    db.commit()
    db.close()
    return 'insert success', 200


# @app.route('/users', methods=["POST"])
# def create_user():
#     db = pymysql.connect(host='localhost', user='root', db='yogurt', password='0000', charset='utf8')
#     curs = db.cursor()
#
#     user = request.form
#
#     user_id = user["id"]
#     user_pw = user["pw"]
#     user_name = user["name"]
#     user_email = user["email"]
#     user_disc = user["disc"]
#
#     pw_hash = bcrypt.generate_password_hash(user_pw)
#
#     sql = '''INSERT INTO `user` (user_id, user_pw, user_name, user_email, user_disc) VALUES (%s, %s, %s, %s, %s)
#           '''
#     curs.execute(sql, (user_id, pw_hash, user_name, user_email, user_disc))
#
#     db.commit()
#     db.close()
#     return 'insert success', 200


@app.route('/write')
def write():
    if "id" not in session:
        flash("로그인을 하세요!!")
        return render_template("login.html")

    return render_template("write.html")


@app.route('/board', methods=['GET'])
def board():
    if "id" not in session:
        flash("로그인을 하세요!!")
        return render_template("login.html")

    db = pymysql.connect(host='localhost', user='root', db='yogurt', password='0000', charset='utf8')
    curs = db.cursor()

    sql = "SELECT * FROM  board b inner JOIN `user` u ON b.user_id = u.id"

    curs.execute(sql)

    data_list = curs.fetchall()
    db.commit()
    db.close()

    return render_template('board.html', data_list=data_list)


@app.route('/board/<id>', methods=['GET'])
def view(id):
    if "id" not in session:
        flash("로그인을 하세요!!")
        return render_template("login.html")

    db = pymysql.connect(host='localhost', user='root', db='yogurt', password='0000', charset='utf8')
    curs = db.cursor()

    sql = f"update board set hit = hit + 1 where id = {id};"

    curs.execute(sql)

    sql = f"SELECT * FROM  board WHERE id = '{id}'"

    curs.execute(sql)

    rows = curs.fetchall()
    print(rows)
    list = []
    for row in rows:
        list.append(row)

    db.commit()
    db.close()

    return render_template('view.html', list=list)


@app.route('/edit/<id>', methods=['GET'])
def correction(id):
    if "id" not in session:
        flash("로그인을 하세요!!")
        return render_template("login.html")

    db = pymysql.connect(host='localhost', user='root', db='yogurt', password='0000', charset='utf8')
    curs = db.cursor()

    sql = f"SELECT * FROM board WHERE id = {id}"

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
    if "id" not in session:
        flash("로그인을 하세요!!")
        return render_template("login.html")

    db = pymysql.connect(host='localhost', user='root', db='yogurt', password='0000', charset='utf8')
    curs = db.cursor()

    id = session["id"]
    name = session["name"]
    title = request.form["subject"]
    cont = request.form["contents"]
    sql = f"INSERT INTO BOARD  (title, contents, NAME, `date`, user_id) VALUES(%s, %s, %s, NOW(), %s);"

    curs.execute(sql, (title, cont, name, id))

    db.commit()
    db.close()
    return redirect('/board')


@app.route('/edit/<id>', methods=['POST'])
def edit(id):
    if "id" not in session:
        flash("로그인을 하세요!!")
        return render_template("login.html")

    db = pymysql.connect(host='localhost', user='root', db='yogurt', password='0000', charset='utf8')
    curs = db.cursor()

    title = request.form["subject"]
    cont = request.form["contents"]

    sql = f"UPDATE board SET title = %s, contents = %s WHERE id = '{id}';"

    curs.execute(sql, (title, cont))

    db.commit()
    db.close()

    return redirect(f'/board/{id}')


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
    return redirect("/")


@app.route('/upload', methods=["POST"])
def upload_file():
    print(request.form)
    print(request.files)
    if 'file' in request.files:
        file = request.files['file']
        print(file.filename)
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect("/")

    return jsonify({"msg": "good"})


@app.route('/logout', methods=["POST"])
def logout():
    session.clear()
    return jsonify({'msg': "logout secces!"}), 200


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
