import argparse
import configparser
import os
import json

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

formatted_data_path = 'data/formatted'
formatted_data_filenames = os.listdir(formatted_data_path)

# MIGRATION HELPERS
def get_set(connection, set_name):
  cur = connection.cursor()

  cur.execute("""
    SELECT * FROM sets WHERE name = %s;
    """,
    [set_name]
  )
  row = cur.fetchone()
  cur.close()

  return row


def insert_set(connection, set_name):
  cur = connection.cursor()
  cur.execute("""
    INSERT INTO sets (name) VALUES (%s) RETURNING id;
    """,
    [set_name]
  )
  id = cur.fetchone()[0]
  cur.close()
  connection.commit()
  
  return id


def insert_and_get_set_id(connection, black_cards, white_cards):
  if len(black_cards) > 0:
    set_name = black_cards[0]['set_name']
    existing_set = get_set(connection, set_name)

    if existing_set is None:
      set_id = insert_set(connection, set_name)
      return set_id

    return existing_set[0]
  else:
    set_name = white_cards[0]['set_name']
    existing_set = get_set(connection, set_name)

    if existing_set is None:
      set_id = insert_set(connection, set_name)
      return set_id

    return existing_set[0]


def insert_black_card():
  return None


def insert_black_cards(connection, black_cards):
  return None


def insert_white_card():
  return None


def insert_white_cards(connection, white_cards):
  return None


# MAIN
def main():
  if args.all:
    print('--all, run all migrations')
    connection = dbh.connect(dbname, dbhost, dbuser, dbpassword)

    if connection is None:
      print('Could not connect to DB, stopping hydration process.')
      return None

    for counter, filename in enumerate(formatted_data_filenames):
      with open('{}/{}'.format(formatted_data_path, filename)) as json_set:
        set = json.load(json_set)
        black_cards = set['black_cards']
        white_cards = set['white_cards']

        set_id = insert_and_get_set_id(
          connection,
          black_cards,
          white_cards
        )

        # loop insert black cards
        # loop insert white cards

      break

    dbh.close(connection)
  elif args.filename == 'all':
    print('no args, run all migrations')
    connection = dbh.connect(dbname, dbhost, dbuser, dbpassword)

    if connection is None:
      print('Could not connect to DB, stopping hydration process.')
      return None

    # loop formatted_data_filenames
      # open formatted_data_file
        # return / insert set_name
        # insert black cards
        # insert white cards

    dbh.close(connection)
  else:
    if args.filename in formatted_data_filenames:
      print('filename exists, run single migration')
      connection = dbh.connect(dbname, dbhost, dbuser, dbpassword)

      if connection is None:
        print('Could not connect to DB, stopping hydration process.')
        return None
    
      # open args.filename
        # return / insert set_name
        # insert black cards
        # insert white cards

      dbh.close(connection)
    else:
      parser.print_help()
      print('\nNo file with the name {} exists in `/data/formatted/`. Please try again.\n'.format(args.filename))
      return None


main()