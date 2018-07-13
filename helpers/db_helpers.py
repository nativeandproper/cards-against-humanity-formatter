import psycopg2

def connect(dbname, host, port, user=None, password=None):
  try:
    if user is None or password is None:
      connection_str = "dbname={} host={} port={} sslmode='disable'".format(dbname, host, port)
      connection = psycopg2.connect(connection_str)
      print('Connection successful')

      return connection
    else:
      connection_str = "dbname={} host={} port={} user={} password={} sslmode='disable'".format(dbname, host, port, user, password)
      connection = psycopg2.connect(connection_str)
      print('Connection successful')

      return connection
  except psycopg2.Error as e:
    print('Unable to connect')
    print('Error: ', e.pgerror)
    return None


def close(connection):
  connection.close()
  print('Connection closed')