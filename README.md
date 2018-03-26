# Cards Against Formatter

A simple Python CLI tool built by [Native & Proper](https://github.com/nativeandproper) to format the output from the [JSON Against Humanity](http://www.crhallberg.com/cah/json) API for easier use.

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

The output files are used to hydrate the database for [our project](https://github.com/nativeandproper/cards-against-humanity-api).

## Developer Documentation

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

## Thanks

A big thank you to [Chris Hallberg](http://www.crhallberg.com/) for his work on [JSON Against Humanity](http://www.crhallberg.com/cah/json)! Without his work, this team would have to spend hours manually typing the [Cards Against Humanity](https://cardsagainsthumanity.com/) game out (yes, we are fast typers, but no one wants to do that). And of course, thank you [Cards Against Humanity](https://cardsagainsthumanity.com/) Team for bringing out the worst in all of us.
