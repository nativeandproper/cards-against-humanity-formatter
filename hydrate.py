import argparse
import configparser
import os
import json
from psycopg2.extensions import AsIs

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
dbhost = config.get('postgresqlDB', 'host', fallback='localhost')
dbport = config.get('postgresqlDB', 'port', fallback='5432')
dbname = config.get('postgresqlDB', 'dbname', fallback='cards_against_humanity')
dbuser = config.get('postgresqlDB', 'user', fallback=None)
dbpassword = config.get('postgresqlDB', 'password', fallback=None)

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


def get_card(connection, card_type_table, text):
  cur = connection.cursor()

  cur.execute("""
    SELECT * FROM %s WHERE text = %s;
    """,
    [AsIs(card_type_table), text]
  )
  row = cur.fetchone()
  cur.close()

  return row


def insert_black_card(connection, set_id, black_card):
  cur = connection.cursor()

  cur.execute("""
    INSERT INTO black_cards (text, pick, set_id) VALUES (%s, %s, %s) RETURNING id;
    """,
    [black_card['text'], black_card['pick'], set_id]
  )
  id = cur.fetchone()[0]
  cur.close()
  connection.commit()

  return id


def insert_white_card(connection, set_id, white_card):
  cur = connection.cursor()

  cur.execute("""
    INSERT INTO white_cards (text, set_id) VALUES (%s, %s) RETURNING id;
    """,
    [white_card['text'], set_id]
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


def insert_black_cards(connection, set_id, black_cards):
  black_card_count = len(black_cards)
  print('Starting insert of {} black cards with set_id {}'.format(black_card_count, set_id))

  new_black_card_ids = []
  existing_black_card_ids = []
  for counter, black_card in enumerate(black_cards):
    existing_black_card = get_card(connection, 'black_cards', black_card['text'])

    if existing_black_card is not None:
      existing_black_card_ids.append(existing_black_card[0])
    else:
      inserted_black_card_id = insert_black_card(
        connection,
        set_id,
        black_card
      )
      new_black_card_ids.append(inserted_black_card_id)

    print('... {}/{} complete'.format((counter + 1), black_card_count))

  print('{}/{} inserted new black_cards, {}/{} already existing black_cards with set_id {}'.format(len(new_black_card_ids), black_card_count, len(existing_black_card_ids), black_card_count, set_id))
  return len(new_black_card_ids)


def insert_white_cards(connection, set_id, white_cards):
  white_card_count = len(white_cards)
  print('Starting insert of {} white cards with set_id {}'.format(white_card_count, set_id))

  new_white_card_ids = []
  existing_white_card_ids = []
  for counter, white_card in enumerate(white_cards):
    existing_white_card = get_card(connection, 'white_cards', white_card['text'])

    if existing_white_card is not None:
      existing_white_card_ids.append(existing_white_card[0])
    else:
      inserted_white_card_id = insert_white_card(
        connection,
        set_id,
        white_card
      )
      new_white_card_ids.append(inserted_white_card_id)

    print('... {}/{} complete'.format((counter + 1), white_card_count))

  print('{}/{} inserted new white_cards, {}/{} already existing white_cards with set_id {}'.format(len(new_white_card_ids), white_card_count, len(existing_white_card_ids), white_card_count, set_id))
  return len(new_white_card_ids)


# MAIN
def main():
  if args.all:
    connection = dbh.connect(dbname, dbhost, dbport, dbuser, dbpassword)

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
        inserted_black_card_count = insert_black_cards(
          connection,
          set_id,
          black_cards
        )
        inserted_white_card_count = insert_white_cards(
          connection,
          set_id,
          white_cards
        )

        print('Finished insert of {} black_cards and {} white_cards with set_id {}'.format(inserted_black_card_count, inserted_white_card_count, set_id))

    dbh.close(connection)
  elif args.filename == 'all':
    connection = dbh.connect(dbname, dbhost, dbport, dbuser, dbpassword)

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
        inserted_black_card_count = insert_black_cards(
          connection,
          set_id,
          black_cards
        )
        inserted_white_card_count = insert_white_cards(
          connection,
          set_id,
          white_cards
        )

        print('Finished insert of {} black_cards and {} white_cards with set_id {}'.format(inserted_black_card_count, inserted_white_card_count, set_id))

    dbh.close(connection)
  else:
    if args.filename in formatted_data_filenames:
      print('filename exists, run single migration')
      connection = dbh.connect(dbname, dbhost, dbport, dbuser, dbpassword)

      if connection is None:
        print('Could not connect to DB, stopping hydration process.')
        return None
    
      with open('{}/{}'.format(formatted_data_path, args.filename)) as json_set:
        set = json.load(json_set)
        black_cards = set['black_cards']
        white_cards = set['white_cards']

        set_id = insert_and_get_set_id(
          connection,
          black_cards,
          white_cards
        )
        inserted_black_card_count = insert_black_cards(
          connection,
          set_id,
          black_cards
        )
        inserted_white_card_count = insert_white_cards(
          connection,
          set_id,
          white_cards
        )

        print('Finished insert of {} black_cards and {} white_cards with set_id {}'.format(inserted_black_card_count, inserted_white_card_count, set_id))

      dbh.close(connection)
    else:
      parser.print_help()
      print('\nNo file with the name {} exists in `/data/formatted/`. Please try again.\n'.format(args.filename))
      return None


main()