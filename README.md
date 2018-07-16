# Cards Against Formatter

This project contains 2 scripts:
1) formatter.py
2) hydrate.py

The formatter script is a simple Python CLI tool built by [Native & Proper](https://github.com/nativeandproper) to format the output from the [JSON Against Humanity](http://www.crhallberg.com/cah/json) API for easier use.

JSON Against Humanity JSON:

```
{
  "blackCards": [
    {
      "text": "Why can't I sleep at night?",
      "pick": 1
    },
    ...
  ],
  "whiteCards": [
    "Pretending to care.",
    ...
  ],
  ["Base"]: {
    "name": "Base Set",
    "black": [0, ...int + N],
    "white"" [0, ... int + N]
  },
  "order": ["Base", ...["Other Deck Names"]]
}
```

Formats to:

```
{
  "black_cards": [
    {
      "set_name": "Base Set",
      "text": "Why can't I sleep at night?",
      "pick": 1
    },
    ...
  ],
  "white_cards": [
    {
      "set_name: "Base Set",
      "text": "Pretending to care."
    },
    ...
  ]
}
```

The hydrate script uses the output files from the formatter script to hydrate the PostgresQL database for [our project](https://github.com/nativeandproper/cards-against-humanity-api).

## Developer Documentation

### Formatter

Raw data files from [JSON Against Humanity](http://www.crhallberg.com/cah/json) need to be saved in the /data/raw/ directory in order for the formatter to work.

```
usage: formatter.py [-h] F E

Format black and white cards from a .json file from crhallberg.com/cah

positional arguments:
  F           name of file in /data/raw/ to be formatted
  E           name of file to output in /data/formatted/

optional arguments:
  -h, --help  show this help message and exit
```

For example, if we have a file called `base_set.json` in the /data/raw/ directory, we can format and save the new structure in /data/formatted/ as `base_set.json` by running the following command:

```
python3 formatter.py base_set.json base_set.json
```

If you want to change the output of the filename to new_name.json, you can run the following:
```
python3 formatter.py base_set.json new_name.json
```

### Hydrate

The `hydrate.py` script uses the psycopg2 dependency in order to connect with the PostgresQL database; please ensure you've installed the depedency from the requirements.txt file.

You must also create your own `config.ini` file in the root of the project in order to connect to your database. An example can be found in config_example.ini or below:
```
[postgresqlDB]
host = 'HOST'
port = 'PORT'
dbname = 'DBNAME'
user = 'USER'
password = 'PASSWORD'
```

```
usage: hydrate.py [-h] [--filename f] [--all]

Hydrates PostgresQL DB with Cards Against Humanity Black and White Cards

optional arguments:
  -h, --help    show this help message and exit
  --filename f  name of file in /data/raw/ to be formatted
  --all         flag to hydrate the database with all files located in
                /data/formatted/
```

In order to hydrate the database with all files located in /data/formatted/, please run the script with the --all flag or no parameters as shown below:
```
# Hydrates with all files using flag
python3 hydrate.py --all

# Hydrates with all files using no flag
python3 hydrate.py
```

In order to hydrate the database with one specific file located in /data/formatted/, please run the script with `--filename filename.json`. For example, if I had a formatted .json file named `trump_set.json` and I only wanted to hydrate those cards, I would run the following:
```
python3 hydrate.py --filename trump_set.json
```

## Thanks

A big thank you to [Chris Hallberg](http://www.crhallberg.com/) for his work on [JSON Against Humanity](http://www.crhallberg.com/cah/json)! Without his work, this team would have to spend hours manually typing the [Cards Against Humanity](https://cardsagainsthumanity.com/) game out (yes, we are fast typers, but no one wants to do that). And of course, thank you [Cards Against Humanity](https://cardsagainsthumanity.com/) Team for bringing out the worst in all of us.
