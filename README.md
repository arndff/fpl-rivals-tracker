# Project's description

As you can guess, I play [FPL](http://fantasy.premierleague.com). I used to check how some managers are doing, opening many tabs in my browser. It was an annoying experience, so I decided to develop this project. 

Thanks to **fpl-rivals-tracker**, you can follow your rivals much easier. After running the script, you're being asked how do you want to sort the data:
1) Total points
2) Gameweek points

Then, you're prompted to answer whether you want to check some *stats* based on it.

**PS**: The table contains 13 columns, so if it doesn't fit in your terminal, just decrease its font size. 

# Getting started

## Prerequisites

* Python 3.6.7

## Installing

```
git clone git@github.com:arndff/fpl-rivals-tracker.git
cd fpl_rivals

pip install -r requirements.txt
```

## Running the project

```
python3 main.py IDs_FILE_PATH
```

Example: 

```
python3 main.py data/IDs.txt
```

Into {IDs_FILE_PATH}, simply put your rivals IDs. 

**Important**: Each line should contain a single ID. The file **must** have this structure, otherwise the script won't work properly.

Example file:
```
109
2039
82429
94
```

Notice how after each ID, there's no other characters.

# Conclusion

If you notice something doesn't work fine, you can send me a DM on [Twitter](https://twitter.com/arndff_).
