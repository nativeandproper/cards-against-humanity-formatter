import argparse
import os

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

formatted_data_filenames = os.listdir('data/formatted')

if args.all:
  print('--all, run all migrations')
  # loop formatted_data_filenames and migrate
elif args.filename == 'all':
  print('no args, run all migrations')
  # loop formatted_data_filenames and migrate
else:
  if args.filename in formatted_data_filenames:
    print('filename exists, run single migration')
    # migrate args.filename
  else:
    parser.print_help()
    print('\nNo file with the name {} exists in `/data/formatted/`. Please try again.\n'.format(args.filename))