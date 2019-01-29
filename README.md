# Project's description

As you can guess, I play [FPL](http://fantasy.premierleague.com). I used to check how some managers are doing, opening many tabs in my browser. It was an annoying experience, so I decided to develop this project. 

Thanks to **fpl-rivals-tracker**, you can follow your rivals much easier. After running the script, you're asked how do you want to sort the data, by:
1) Total points
2) Gameweek points

Then, you're prompted to answer whether you want to check some **stats** based on it.

**PS**: The table contains 13 columns, so if it doesn't fit in your terminal, just decrease its font size until it looks good. 

# Getting started

## Prerequisites

* [Python 3](https://www.python.org/downloads/)

## Installing

```
git clone https://github.com/arndff/fpl-rivals-tracker.git
cd fpl-rivals-tracker

pip install -r requirements.txt
```

## Running the project

How you'll do it, depends on your setup.

Either this:
```
python main.py {IDs_FILE_PATH}
```

or that way:

```
python3 main.py {IDs_FILE_PATH}
```

The script expects **one** argument: path to a text file which contains your rivals IDs. The path can be absolute or relative. 

In ```data``` folder, there's a file called ```example_file_with_ids.txt```. Its content looks like this:

```
4668
29104
64342
829593
```

**Important**: Each line should contain a single ID. And there's no newline after the last ID. Your file with rivals IDs **must** have this structure, otherwise the script won't work properly. Notice how after each ID, there's no other characters on the same line.

Here's how the script can be run with the aforemetnioned file:

```
python3 main.py data/example_file_with_ids.txt
```

# Contribution

If you notice that something doesn't work correctly, you can send me a DM on [Twitter](https://twitter.com/arndff_). 

Good luck in beating your rivals! 😉
