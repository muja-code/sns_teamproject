import pymysql
from flask import Flask, render_template, request, json

app = Flask(__name__)



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


   sql = '''INSERT INTO `user` (user_id, user_pw, user_name, user_email) VALUES (%s, %s, %s, %s)
      '''
   curs.execute(sql, (user_id, user_pw, user_name, user_email))

   db.commit()
   db.close()
   return 'insert success', 200

@app.route('/users/<id>', methods=["GET"])
def get_users(id):
   db = pymysql.connect(host='localhost', user='root', db='yogurt', password='0000', charset='utf8')
   curs = db.cursor()

   sql = '''SELECT user_id, user_name FROM `user` AS u WHERE u.id=%s'''

   curs.execute(sql, id)

   rows = curs.fetchall()
   print(rows)

   json_str = json.dumps(rows, indent=4, sort_keys=True, default=str)
   db.commit()
   db.close()
   return json_str, 200


@app.route('/board', methods=["POST"])
def writing():
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
   print(rows)

   json_str = json.dumps(rows, indent=4, sort_keys=True, default=str)
   db.commit()
   db.close()
   return json_str, 200


@app.route('/login', methods=["POST"])
def login():
   db = pymysql.connect(host='localhost', user='root', db='yogurt', password='0000', charset='utf8')
   curs = db.cursor()

   login = request.json

   user_id = login["user_id"]
   user_pw = login["user_pw"]

   sql = '''SELECT user_pw FROM `user` AS u WHERE u.user_id=%s;
   '''
   curs.execute(sql, user_id)

   row = curs.fetchall()

   db.commit()
   db.close()

   if user_pw == row[0][0]:
      return 'login success', 200
   else:
      return "login fail", 200



if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)