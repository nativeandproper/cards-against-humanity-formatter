import argparse
import configparser
import os

# Local Imports
import helpers.db_helpers as dbh

parser = argparse.ArgumentParser(description='Hydrates PostgresQL DB with Cards Against Humanity Black and White Cards')
parser.add_argument(
  '--filename',
  metavar='f',
  type=str,
  default='all',
  help='name of file in /data/raw/ to be formatted'
)
parser.add_argument(
  '--all',
  action='store_true',
  help='flag to hydrate the database with all files located in /data/formatted/'
)
args = parser.parse_args()

config = configparser.ConfigParser()
config.read('config.ini')
dbhost = config.get('dbconfig', 'host', fallback='localhost')
dbname = config.get('dbconfig', 'dbname', fallback='cards_against_humanity')
dbuser = config.get('dbconfig', 'user', fallback=None)
dbpassword = config.get('dbconfig', 'password', fallback=None)

formatted_data_filenames = os.listdir('data/formatted')

# MIGRATION HELPERS
def get_set():
  return None

def insert_set():
  return None

def insert_black_card():
  return None

def insert_black_cards():
  return None

def insert_white_card():
  return None

def insert_white_cards():
  return None

# MAIN
def main():
  if args.all:
    print('--all, run all migrations')
    # connect and return connection
    connection = dbh.connect(dbname, dbhost, dbuser, dbpassword)

    if connection is None:
      return None

    cur = connection.cursor()
    set_name = 'testing insert'
    cur.execute("""
      INSERT INTO sets (name) VALUES (%s);
      """,
      [set_name]
    )
    cur.execute("""
      SELECT * FROM sets;
    """)
    fetched = cur.fetchone()
    print('fetched: ', fetched)
    connection.commit()
    cur.close()
    # loop formatted_data_filenames
      # open formatted_data_file
        # return / insert set_name
        # insert black cards
        # insert white cards

    # close connection
    dbh.close(connection)
  elif args.filename == 'all':
    print('no args, run all migrations')
    # connect and return connection
    connection = dbh.connect(dbname, dbhost, dbuser, dbpassword)

    if connection is None:
      return None

    # loop formatted_data_filenames
      # open formatted_data_file
        # return / insert set_name
        # insert black cards
        # insert white cards

    # close connection
    dbh.close(connection)
  else:
    if args.filename in formatted_data_filenames:
      print('filename exists, run single migration')
      # connect and return connection
      connection = dbh.connect(dbname, dbhost, dbuser, dbpassword)

      if connection is None:
        return None
    
      # open args.filename
        # return / insert set_name
        # insert black cards
        # insert white cards

      # close connection
      dbh.close(connection)
    else:
      parser.print_help()
      print('\nNo file with the name {} exists in `/data/formatted/`. Please try again.\n'.format(args.filename))
      return None

main()