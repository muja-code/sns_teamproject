import os
import logging
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
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 로그 생성
logger = logging.getLogger('loggin msg')
logger1 = logging.getLogger('loggin1 msg')

# 로그의 출력 기준 설정
logger.setLevel(logging.INFO)

logger1.setLevel(logging.ERROR)

# log 출력 형식
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# log 출력
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

# log를 파일에 출력
file_handler = logging.FileHandler('logfile.log', encoding='utf-8')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# 메인페이지
@app.route('/')
def home():
    per_page = 8
    page, _, offset = get_page_args(per_page=per_page)

    db = pymysql.connect(host='localhost', user='root', db='yogurt', password='0000', charset='utf8')
    curs = db.cursor()

    curs.execute("SELECT COUNT(*) FROM board;")

    all_count = curs.fetchall()[0][0]

    curs.execute("SELECT * FROM board ORDER BY `date` DESC LIMIT %s OFFSET %s;", (per_page, offset))
    data_list = curs.fetchall()

    db.commit()
    db.close()

    if data_list == ():
        if "id" not in session:
            id = None;
            name = None;
            return render_template("main.html", id=id, name=name)

    pagination = Pagination(page=page, per_page=per_page, total=all_count, record_name='board',
                            css_framework='foundation', bs_version=5)
    if "id" not in session:
        id = None;
        name = None;

        return render_template('main.html', data_lists=data_list, pagination=pagination, id=id, name=name)
    logger.info('홈페이지 접속')
    return render_template('main.html', data_lists=data_list, pagination=pagination, id=session["id"],
                           name=session["name"], css_framework='foundation', bs_version=5)


# 회원가입
@app.route('/users/create')
def user_page():
    logger.info('회원가입 페이지 접속')
    return render_template("creat_user.html")

# 회원가입
@app.route("/users", methods=["POST"])
def login_info_post():
    db = pymysql.connect(host='localhost', user='root', password='0000', database='yogurt', charset='utf8')
    cursor = db.cursor()

    user_id_receive = request.form['user_id_give']
    user_pass_receive = request.form['user_pass1_give']
    name_receive = request.form['name_give']
    email_receive = request.form['email_give']
    disc_receive = request.form['disc_give']
    img_receive = request.form['img_give']

    sql = "SELECT COUNT(*) FROM `user` AS u WHERE u.user_id = %s;"
    cursor.execute(sql, user_id_receive)
    count = cursor.fetchall()[0][0]

    if count != 0:
        flash("아이디가 존재 합니다^^")
        logger.info('아이디가 존재 합니다^^')
        return jsonify({"msg": "아이디가 존재 합니다^^", "check": False})

    pw_hash = bcrypt.generate_password_hash(user_pass_receive)

    sql = 'INSERT INTO user (user_id, user_pw, user_name, user_email, user_image, user_disc) values(%s, %s, %s, %s, %s, %s)'
    cursor.execute(sql, (user_id_receive, pw_hash, name_receive, email_receive, img_receive, disc_receive))

    db.commit()
    db.close()

    flash("회원가입 성공!!")
    logger.info('회원가입 성공')
    return jsonify({"msg": "성공!", "check": True})


# 글쓰기
@app.route('/write')
def write():
    if "id" not in session:
        flash("로그인을 하세요!!")
        logger1.error('로그인 없이 글쓰기 페이지 접속 시도')
        return render_template("login.html")
    logger.info('글쓰기 페이지 접속')
    return render_template("write.html")


# 개인게시판
@app.route('/board', methods=['GET'])
def board():
    if "id" not in session:
        flash("로그인을 하세요!!")
        logger1.error('로그인 없이 게시판 접속')
        return render_template("login.html")

    id = session["id"]

    per_page = 9
    page, _, offset = get_page_args(per_page=per_page)

    db = pymysql.connect(host='localhost', user='root', db='yogurt', password='0000', charset='utf8')
    curs = db.cursor()
    sql = f"SELECT COUNT(*) FROM board AS b WHERE b.user_id = {id};"
    curs.execute(sql)
    cnt = curs.fetchall()[0][0]

    if cnt == 0:
        db.commit()
        db.close()
        return render_template('board.html', data_lists=())

    curs.execute("SELECT COUNT(*) FROM board WHERE user_id=%s;", id)

    all_count = curs.fetchall()[0][0]

    curs.execute("SELECT * FROM board WHERE user_id=%s ORDER BY `date` DESC LIMIT %s OFFSET %s;",
                 (id, per_page, offset))

    data_list = curs.fetchall()

    db.commit()
    db.close()
    # pagination = Pagination(page=page, per_page=per_page, total=all_count, record_name='board')
    pagination = Pagination(page=page, per_page=per_page, total=all_count, record_name='게시판')
    logger.info('게시판 접속 완료')
    return render_template('board.html', data_lists=data_list, pagination=pagination)


# 개인글
@app.route('/board/view/<id>', methods=['GET'])
def view(id):
    if "id" not in session:
        flash("로그인을 하세요!!")
        logger1.error('로그인 없이 개인 게시글 페이지 접속 시도')
        return redirect("/login")

    db = pymysql.connect(host='localhost', user='root', db='yogurt', password='0000', charset='utf8')
    curs = db.cursor()

    sql = f"SELECT COUNT(*) FROM board AS b WHERE b.id = {id};"
    curs.execute(sql)
    cnt = curs.fetchall()[0][0]

    if cnt == 0:
        db.commit()
        db.close()
        flash("존재하지 않은 글 입니다.")
        return redirect("/")

    sql = f"update board set hit = hit + 1 where id = {id};"

    curs.execute(sql)

    sql = f"SELECT * FROM  board WHERE id = {id}"

    curs.execute(sql)

    rows = curs.fetchall()
    list = []
    for row in rows:
        list.append(row)

    db.commit()
    db.close()
    logger.info('게시글 페이지 접속 완료')
    return render_template('view.html', list=list)


# 수정페이지
@app.route('/board/edit/<id>', methods=['GET'])
def correction(id):
    if "id" not in session:
        flash("로그인을 하세요!!")
        logger1.error('로그인 없이 게시물 수정 페이지 접속 시도')
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
    logger.info('게시물 수정 페이지 접속 완료')
    return render_template('edit.html', list=list)


# 게시글 등록
@app.route('/board', methods=['POST'])
def write_post():
    if "id" not in session:
        flash("로그인을 하세요!!")
        logger1.error('로그인 없이 게시글 작성 시도')
        return render_template("login.html")

    db = pymysql.connect(host='localhost', user='root', db='yogurt', password='0000', charset='utf8')
    curs = db.cursor()

    id = session["id"]
    name = session["name"]
    title = request.form["subject"]
    cont = request.form["contents"]
    sql = f"INSERT INTO BOARD  (title, contents, NAME, `date`, user_id) VALUES(%s, %s, %s, NOW(), %s);"

    if len(title) == 0:
        logger1.error('게시글 제목 입력 없음')
        return "<script>alert('제목을 입력하세요');window.location.href='/write'</script>"
    if len(cont) == 0:
        logger1.error('게시글 내용 입력 없음')
        return "<script>alert('내용을 입력하세요');window.location.href='/write'</script>"
    curs.execute(sql, (title, cont, name, id))

    db.commit()
    db.close()
    logger.info('게시글 등록 완료')
    return redirect('/board')


# 게시글 수정
@app.route('/board/edit/<id>', methods=['POST'])
def edit(id):
    if "id" not in session:
        flash("로그인을 하세요!!")
        logger1.error('로그인 없이 게시글 수정 시도')
        return render_template("login.html")

    db = pymysql.connect(host='localhost', user='root', db='yogurt', password='0000', charset='utf8')
    curs = db.cursor()

    title = request.form["subject"]
    cont = request.form["contents"]

    sql = f"UPDATE board SET title = %s, contents = %s WHERE id = '{id}';"

    if len(title) == 0:
        logger1.error('게시글 수정 제목 없음')
        return "<script>alert('제목을 입력하세요');window.location.href='/write'</script>"
    if len(cont) == 0:
        logger1.error('게시글 수정 내용 없음')
        return "<script>alert('내용을 입력하세요');window.location.href='/write'</script>"
    curs.execute(sql, (title, cont))

    db.commit()
    db.close()
    logger.info('게시물 수정 완료')
    return redirect(f'/board/view/{id}')


# 게시글 삭제
@app.route("/board/delete/<id>", methods=["DELETE"])
def delete_boadr(id):
    db = pymysql.connect(host='localhost', user='root', db='yogurt', password='0000', charset='utf8')
    curs = db.cursor()

    sql = f"DELETE FROM board WHERE id = '{id}'"

    curs.execute(sql)

    db.commit()
    db.close()
    logger.info('게시물 삭제 완료')
    return jsonify({'msg': '삭제 완료!'})


# 로그인
@app.route('/login')
def login_page():
    logger.info('로그인 페이지 접속')
    return render_template("login.html")


# 로그인하기
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
    if (rows == ()):
        logger1.error('아이디 입력 없음')
        return jsonify({"msg": "아이디를 확인해주세요^^", "check": False})

    is_login = bcrypt.check_password_hash(rows[0][1], user_pw)

    if is_login == False:
        logger1.error('비밀번호 틀림')
        return jsonify({"msg": "비밀번호를 확인해주세요^^", "check": False})

    session["id"] = rows[0][0]
    session["name"] = rows[0][2]
    logger.info('로그인 성공')
    return jsonify({"msg": "로그인 성공^^", "check": True})


# 로그아웃
@app.route('/logout', methods=["POST"])
def logout():
    session.clear()
    logger.info('로그아웃 성공')
    return jsonify({'msg': "logout secces!"}), 200


# 프로필 수정
@app.route('/users', methods=["PUT"])
def put_users():
    id = session["id"]
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
    logger.info('프로필 수정 완료')
    return jsonify({'msg': '수정이 완료되었습니다'}), 200


# 개인프로필
@app.route('/users', methods=["GET"])
def get_users():
    if "id" not in session:
        return render_template("creat_user.html")
    id = session["id"]
    db = pymysql.connect(host='localhost', user='root', db='yogurt', password='0000', charset='utf8')
    curs = db.cursor()
    sql = '''SELECT user_id, user_name, user_email, user_disc, user_image FROM `user` AS u WHERE u.id=%s'''
    curs.execute(sql, id)
    rows = curs.fetchall()

    result = {
        "user_id": rows[0][0],
        "user_name": rows[0][1],
        "user_email": rows[0][2],
        "user_disc": rows[0][3],
        "user_image": rows[0][4]
    }

    db.commit()
    db.close()
    logger.info('개인 프로필 페이지 접속')
    return jsonify({'users': result}), 200


@app.route('/users/mypage')
def mypage():
    logger.info('개인 프로필 페이지 접속')
    return render_template("mypage.html")


# 프로필 수정 페이지
@app.route('/users/edit')
def mypage_edit():
    logger.info('프로필 수정 페이지 접속')
    return render_template("mypage_edit.html")


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
