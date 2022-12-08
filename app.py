import pymysql, os
from flask import Flask, render_template, request, jsonify, redirect
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/img'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# 프로필 페이지
@app.route('/')
def home():
    return redirect('/mypage')


@app.route('/mypage')
def mypage():
    return render_template("mypage.html")


# 프로필 수정 페이지
@app.route('/edit')
def mypage_edit():
    return render_template("mypage_edit.html")


# 페이지 DB GET정보
@app.route('/users/<id>', methods=["GET"])
def get_users(id):
    db = pymysql.connect(host='localhost', user='root', db='yogurt', password='221114', charset='utf8')
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

    return jsonify({'users': result}), 200


# 페이지 DB 수정
@app.route('/users/<id>', methods=["PUT"])
def put_users(id):
    db = pymysql.connect(host='localhost', user='root', db='yogurt', password='221114', charset='utf8')
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

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
