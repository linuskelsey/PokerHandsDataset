# Poker Hands Dataset

Forked from [allenfrostline](https://github.com/allenfrostline/PokerHandsDataset)'s repo, freshened up by myself to include usage for Python3 with up-to-date modules (you will need to `pip3 install print-color` first).

Simple scripts to extract, clean and browse the [IRC Poker Database](https://poker.cs.ualberta.ca/irc_poker_database.html). Note here only hold 'em hands are included, but that can be changed from within [`extract.py`](extract.py). Most (over 95%) hands are dropped either because they're not hold 'em or because of lack of features. It should be noted that hands included in both the `hands_valid.json` and `hands_basic.json` files include only those with at least two final players and only those players who revealed their cards at the end of a round, i.e. those who had a chance to win the pot when all cards were shown.

Additional functionality added by me to extract further basic information about the data ([`extract_basic.py`](extract_basic.py)), reducing a round to the community cards and each players' pocket cards and whether they won/lost. The script [`encode_basic.py`](encode_basic.py) turns the data from `hands_basic.json` into encoded data (strings for cards converted to unique integers via [`encoding.py`](encoding.py)) for easy use in machine learning models.

Provided a script [`separate_stages.py`](separate_stage.py) to allow data to be separated by which part of a hand you are modelling, be it the preflop, flop, river or turn.

## Data Preparation

Run the following codes in order:

```zsh
wget http://poker.cs.ualberta.ca/IRC/IRCdata.tgz  # download the database (-> IRCdata.tgz)
tar -xvf IRCdata.tgz                              # unzip the tgz file (-> IRCdata)
python3 extract.py                                # extract data (-> hands.json)
python3 clean.py                                  # drop invalid hand data (-> hands_valid.json)
python3 extract_basic.py                          # extract only the board, players' pocket cards and winners (-> hands_basic.json)
python3 encode_basic.py                           # encode data from hands_basic.json into integers for a machine learning model (-> encoded_basic.json)
```

Eventually there're 10,233,955 hands in `hands.json` and 437,862 in `hands_valid.json` after cleaning (if all games are considered - with hold 'em only it's 117,801 final hands).

## Data Inspection

You may run the following code to inspect hands in their original order. Any time you'd like to stop browsing, you can just use `Ctrl+C` to interrupt the process.

```zsh
python3 browse.py                                 # print hands in a formatted way
```

The script lists extracted hands history as below.

    ############################################################
       time : 199612            id : 2093
      board : ['Qd', '6s', 'Td', 'Qc', 'Jh']
       pots : [(2, 60), (2, 60), (2, 60), (2, 60)]
    players : 
                             Tiger (#1)                         
    {'action': 30,
     'bankroll': 2922,
     'bets': [{'actions': ['B', 'r'], 'stage': 'p'},
              {'actions': ['k'], 'stage': 'f'},
              {'actions': ['k'], 'stage': 't'},
              {'actions': ['k'], 'stage': 'r'}],
     'pocket_cards': ['9s', 'Ac'],
     'winnings': 30}
    · · · · · · · · · · · · · · · · · · · · · · · · · · · · · · 
                            jvegas2 (#2)                        
    {'action': 30,
     'bankroll': 139401,
     'bets': [{'actions': ['B', 'c'], 'stage': 'p'},
              {'actions': ['k'], 'stage': 'f'},
              {'actions': ['k'], 'stage': 't'},
              {'actions': ['k'], 'stage': 'r'}],
     'pocket_cards': ['9c', 'As'],
     'winnings': 30}
    ############################################################

## Data Format

Once all the data has been extracted and the hands simplified into the basic categories of `num_players`, `board` (the community cards), `players` (the cards each player holds and whether or not they won) and `id` (hand id), there are 3 data files: `hands.json`, `hands_valid.json` and `hands_basic.json`. Running `python3 browse.py` in the terminal will give you data of the form presented above for the second of those three. The `hands_basic.json` contains objects of the form:

```
{
    "num_players": <num_players: int>,
    "board": <board: List[str]>,
    "players": <players: [<cards: List[str]>, <won: bool>]>,
    "id": <id: int>
}
```

Once these have been encoded into a fourth json, `encoded_basic.json`, the data looks like:

```
{
    "num_players": <num_players: int>,
    "board": <board: List[int]>,
    "players": <players: [<cards: List[int]>, <won: bool>]>,
    "id": <id: int>
}
```

with each string representing a card encoded into an `int`. Finally, once the [`separate_stages.py`](separate_stages.py) file is run four times with appropriate inputs, four new files within `game_data` are created (you may need to create the folder `game_data`). The effect of [`separate_stages.py`](separate_stages.py) is that each hand is inspected and split to give an input and output for each player of the hand, each of these players providing a specific data point (to a model).

These new files contain a 1x2 array, the inputs and outputs to a potential ML model. The outputs are simple `bool`'s representing a win or a loss, and the inputs are lists of the cards both in the pocket and on the table (pocket cards always first). For example, from `encoded_river.json`:

```
[[[20, 24, 5, 42, 33, 14], [30, 39, 5, 42, 33, 14], [6, 23, 5, 42, 33, 14], ... ]]
```

## References

- [IRC Poker Database](http://poker.cs.ualberta.ca/irc_poker_database.html), Computer Poker Research Group, University of Alberta, 2017.
- [Miami Data Science Meetup](https://github.com/dksmith01/MSDM/blob/987836595c73423b89f83b29747956129bec16c2/.ipynb_checkpoints/MDSM%20Project%201%20Poker%20Python%20Wrangling%20Code-checkpoint.ipynb), 2015.
