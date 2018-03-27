import psycopg2

def connect(dbname, host, user=None, password=None):
  try:
    if user is None or password is None:
      connection_str = "dbname={} host={}".format(dbname, host)
      connection = psycopg2.connect(connection_str)
      print('Connection successful')

      return connection
    else:
      connection_str = "dbname={} host={} user={} pass={}".format(dbname, host, user, password)
      connection = psycopg2.connect(connection_str)
      print('Connection successful')

      return connection
  except:
    print('Unable to connect')
    return None

def close(connection):
  connection.close()
  print('Connection closed')