# Project's description

As you can guess, I play [FPL](http://fantasy.premierleague.com). I used to check how some managers are doing, opening many tabs in my browser. It was an annoying experience, so I decided to develop this project. 

Thanks to **fpl-rivals-tracker**, you can follow your rivals much easier. After running the script, you're asked how do you want to sort the data, by:
1) Total points
2) Gameweek points

Then, you're prompted to answer whether you want to check some **stats** based on it.

**PS**: The table contains 13 columns, so if it doesn't fit in your terminal, just decrease its font size until it looks good. 

# Getting started

## Prerequisites

* Python 3.6.7

## Installing

```
git clone git@github.com:arndff/fpl-rivals-tracker.git
cd fpl-rivals-tracker

pip install -r requirements.txt
```

## Running the project

```
python3 main.py IDs_FILE_PATH
```

The script expects **one** argument: path to a text file which contains your rivals IDs. Here's an example of such file:
```
109
2039
82429
94
```

**Important**: Each line should contain a single ID. The file **must** have this structure, otherwise the script won't work properly. Notice how after each ID, there's no other characters.

I have a folder called ```data``` and the file: ```IDs.txt``` is located inside it. So here's how I run the script: 

```
python3 main.py data/IDs.txt
```

# Conclusion

If you notice something doesn't work fine, you can send me a DM on [Twitter](https://twitter.com/arndff_).
