# Project's description

As you can guess, I play [FPL](http://fantasy.premierleague.com). I used to check how some managers are doing, opening many tabs in my browser. It was an annoying experience, so that motivated me to develop this project.

Thanks to **fpl-rivals-tracker**, you can follow your rivals much easier. After running the script, you're asked how do you want to sort the data, by:
1) Total points
2) Gameweek points

Then, you're prompted to answer whether you want to check some **stats** based on it.

**PS**: The table contains 13 columns, so if it doesn't fit in your terminal, just decrease its font size until it looks good. 

# Getting started

## Prerequisites

* [Python 3](https://www.python.org/downloads/)

## Installing

Open your Terminal/PowerShell. Then follow these steps:

```
git clone https://github.com/arndff/fpl-rivals-tracker.git
cd fpl-rivals-tracker

pip install -r requirements.txt
```

## Running the project

### File Utils

If you want to generate a file with rivals IDs or modify an existing one by adding more IDs to its end, you can run ```file_main.py```
this ```python files_main.py``` or that way: ```python3 files_main.py```.

You're asked to choose one of these 2 options and then you have to enter a file name (without its extension). For instance,
```example_file_with_ids``` **instead of** ```example_file_with_ids.txt```. 

After that, simply enter an integer which indicates how many IDs you want to add. Then you're able to write them one by one.

**PS:** These files are stored into ```data```. You can modify them manually but there're some rules.
* Each line should contain a single ID.
* Notice how after each ID, there's no other characters on the same line.
* Also, there's no newline after the last ID.
* File extension **must** be ```.txt```.

Your files with rivals IDs **must** have this structure, otherwise the script won't work properly. 

### The project

Okay, let's assume you've generated a file with IDs. Now, it's time to run the project. The script expects **only one** argument: file name which contains your rivals IDs. You can do it:

either this: ```python main.py {file_name}``` or that way: ```python3 main.py {file_name}```.

In ```data``` folder, there's a file called ```example_file_with_ids.txt```. Its content looks like this:

```
4668
29104
64342
829593
```

Here's how the script can be run with the aforemetnioned file:

```
python3 main.py example_file_with_ids
```

# Contribution

If you have any questions or notice that something doesn't work correctly, you can send me a DM on [Twitter](https://twitter.com/arndff_). 

Good luck in beating your rivals! 😉
