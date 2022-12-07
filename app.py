import os

import pymysql
from flask import Flask, render_template, request, json, jsonify, session, redirect, url_for, flash, Blueprint
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename

# from flask_pagination import Pagination, get_page_parameter

app = Flask(__name__)

app.config["SECRET_KEY"] = "secret_pw_key"
app.config["BCRYPT_LEVEL"] = 10
bcrypt = Bcrypt(app)

mod = Blueprint('users', __name__)

UPLOAD_FOLDER = 'static/img'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# @app.route('/')
# def home():
#    return render_template('index.html')

@app.route('/')
def home():
    db = pymysql.connect(host='localhost', user='root', db='yogurt', password='0000', charset='utf8')
    curs = db.cursor()

    sql = "SELECT * FROM board;"

    curs.execute(sql)

    data_list = curs.fetchall()
    db.commit()
    db.close()

    print(data_list)
    if "id" not in session:
        id = None;
        name = None;
        return render_template("main.html", id=id, name=name, data_list=data_list)

    # page = request.args.get(get_page_parameter(), type=int, default=1)

    return render_template("main.html", id=session["id"], name=session["name"], data_list=data_list)

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

    sql = 'INSERT INTO user (user_id, user_pw, user_name, user_email) values(%s, %s, %s, %s)'
    cursor.execute(sql, (user_id_receive, pw_hash, name_receive, email_receive))

    db.commit()
    db.close()
    return 'insert success',200
#
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
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
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
