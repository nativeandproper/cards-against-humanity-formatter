import argparse
import json

parser = argparse.ArgumentParser(description='Format black and white cards from a .json file from crhallberg.com/cah')

parser.add_argument(
  'filename',
  metavar='F',
  type=str,
  help='name of file in /data/raw/ to be formatted'
)
parser.add_argument(
  'edited_filename',
  metavar='E', 
  type=str,
  help='name of file to output in /data/formatted/'
)

args = parser.parse_args()

formatted_set = {
  'black_cards': [],
  'white_cards': []
}

with open('data/raw/{}'.format(args.filename)) as json_set:
  set = json.load(json_set)
  set_name = set[set['order'][0]]['name']
  
  for black_card in set['blackCards']:
    formatted_set['black_cards'].append({
      'set_name': set_name,
      'text': black_card['text'],
      'pick': black_card['pick']
    })

  for white_card in set['whiteCards']:
    formatted_set['white_cards'].append({
      'set_name': set_name,
      'text': white_card
    })

json.dump(
  formatted_set,
  open('data/formatted/{}'.format(args.edited_filename), 'w'),
  indent=2
)