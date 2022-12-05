db = {
  'user' : 'root',
  'password' : '810665',
  'host' : 'localhost',
  'port' : 3306,
  'database' : 'free_board'
}

DB_URL = f"mysql+mysqlconnector://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}?charset=utf8"




