import os

import pymysql
from flask import Flask, render_template, request, jsonify, session, redirect, flash, Blueprint
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
from flask_paginate import Pagination, get_page_args

app = Flask(__name__)

app.config["SECRET_KEY"] = "secret_pw_key"
app.config["BCRYPT_LEVEL"] = 10
bcrypt = Bcrypt(app)

mod = Blueprint('users', __name__)

UPLOAD_FOLDER = 'static/img'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    per_page = 8
    page, _, offset = get_page_args(per_page=per_page)
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
                           name=session["name"], css_framework='foundation', bs_version=5)


@app.route('/users')
def user_page():
    return render_template("creat_user.html")


@app.route("/users", methods=["POST"])
def login_info_post():
    db = pymysql.connect(host='localhost', user='root', password='0000', database='yogurt', charset='utf8')
    cursor = db.cursor()
    print(1)
    print(request.form)
    user_id_receive = request.form['user_id_give']
    user_pass_receive = request.form['user_pass1_give']
    name_receive = request.form['name_give']
    email_receive = request.form['email_give']
    disc_receive = request.form['disc_give']
    img_receive = request.form['img_give']

    # pw_hash = bcrypt.generate_password_hash(user_pass_receive)

    sql = 'INSERT INTO user (user_id, user_pw, user_name, user_email, user_image, user_disc) values(%s, %s, %s, %s, %s, %s)'
    cursor.execute(sql, (user_id_receive, user_pass_receive, name_receive, email_receive, img_receive, disc_receive))

    db.commit()
    db.close()
    print(2)
    flash("회원가입 성공!!")
    print(3)
    return jsonify({"msg":"성공!"})


@app.route('/write')
def write():
    if "id" not in session:
        flash("로그인을 하세요!!")
        return render_template("login.html")

    return render_template("write.html")


@app.route('/board', methods=['GET'])
def board():
    per_page = 8
    page, _, offset = get_page_args(per_page=per_page)

    if "id" not in session:
        flash("로그인을 하세요!!")
        return render_template("login.html")

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

    return render_template('board.html', data_lists=data_list, pagination=pagination)


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
    list = []
    for row in rows:
        list.append(row)

    db.commit()
    db.close()

    return render_template('view.html', list=list)


@app.route('/board/edit/<id>', methods=['GET'])
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


@app.route('/board/edit/<id>', methods=['POST'])
def edit(id):
    if "id" not in session:
        flash("로그인을 하세요!!")
        return render_template("login.html")

    db = pymysql.connect(host='localhost', user='root', db='yogurt', password='0000', charset='utf8')
    curs = db.cursor()

    title = request.form["subject"]
    cont = request.form["contents"]

    sql = f"UPDATE board SET title = %s, contents = %s WHERE num = '{id}';"

    curs.execute(sql, (title, cont))

    db.commit()
    db.close()

    return redirect(f'/board/{id}')


@app.route("/board/<id>", methods=["DELETE"])
def delete_boadr(id):
    db = pymysql.connect(host='localhost', user='root', db='yogurt', password='0000', charset='utf8')
    curs = db.cursor()

    sql = f"DELETE FROM board WHERE id = '{id}'"
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
    return redirect("/")


@app.route('/logout', methods=["POST"])
def logout():
    session.clear()
    return jsonify({'msg': "logout secces!"}), 200


@app.route('/users/<id>', methods=["PUT"])
def put_users(id):
    db = pymysql.connect(host='localhost', user='root', db='yogurt', password='0000', charset='utf8')
    curs = db.cursor()

    name = request.form["name"]
    email = request.form["email"]
    disc = request.form["disc"]

    if 'file' in request.files:
        file = request.files['file']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        user_img = file.filename

    else:

        user_img = "default.png"

    sql = '''UPDATE `user` SET user_name=%s, user_email=%s, user_disc=%s, user_image=%s WHERE id=%s;'''

    curs.execute(sql, (name, email, disc, user_img, id))

    db.commit()
    db.close()

    return jsonify({'msg': '수정이 완료되었습니다'}), 200


@app.route('/users/<id>', methods=["GET"])
def get_users(id):
    print(id)
    print(1)
    db = pymysql.connect(host='localhost', user='root', db='yogurt', password='0000', charset='utf8')
    curs = db.cursor()
    print(2)
    sql = '''SELECT user_id, user_name, user_email, user_disc, user_image FROM `user` AS u WHERE u.id=%s'''
    print(3)
    curs.execute(sql, id)
    print(4)
    rows = curs.fetchall()
    print(5)
    result = {
        "user_id": rows[0][0],
        "user_name": rows[0][1],
        "user_email": rows[0][2],
        "user_disc": rows[0][3],
        "user_image": rows[0][4]
    }

    db.commit()
    db.close()
    print(6)
    return jsonify({'users': result}), 200


@app.route('/users/mypage')
def mypage():
    return render_template("mypage.html")


# 프로필 수정 페이지
@app.route('/users/edit')
def mypage_edit():
    return render_template("mypage_edit.html")


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
