# Project's Description

As you can guess, I play [FPL](http://fantasy.premierleague.com). I used to check how some managers are doing, opening many tabs in my browser. It was an annoying experience, so that motivated me to develop this project.

Thanks to **fpl-rivals-tracker**, you can follow your rivals much easier. After running the script, you're asked how do you want to sort the data, by:
1) Total points
2) Gameweek points

Then, you're prompted to answer whether you want to check some **stats** based on it.

**PS**: The table contains 13 columns, so if it doesn't fit in your terminal, just decrease its font size until it looks good. 

# Getting Started

## Prerequisites

* [Python 3](https://www.python.org/downloads/)

## Installing

0) Open your Terminal/PowerShell. Each step below will be executed there.

1) Check Python version:
   
   1.1) Type: ```python --version``` -- if you see a similar output: *Python 3.6.7*, then you can skip 1.2)
   
   1.2) Type: ```python3 --version``` -- if you installed Python successfully, you should see something like this: *Python 3.6.7*.
   
   ~> You're going to use either **python** & **pip** or **python3** & **pip3** during the whole guide.

2) Then follow these steps:

```
git clone https://github.com/arndff/fpl-rivals-tracker.git
cd fpl-rivals-tracker

pip install -r requirements.txt
```

## Running the Project

Don't forget to keep your Terminal/PowerShell open.

### File Utils

If you want to **generate** a file with rivals IDs or **modify** an existing one by adding more IDs to its end, you can run *file_utils_main.py* this way: ```python file_utils_main.py```.

You're asked to choose one of these 2 options and then you have to enter a file name (without its extension). For instance,
*example_file_with_ids* **instead of** *example_file_with_ids.txt*. 

After that, simply enter an integer which indicates how many IDs you want to add. Then you're able to write them one by one.

**PS:** These files are stored into the *data* folder, located inside the project. You can modify them manually but there're some rules:
* Each line should contain a single ID.
* Notice how after each ID, there's no other characters on the same line.
* File extension **must** be *.txt*.

Your files with rivals IDs **must** have this structure, otherwise the script won't work properly. 

### The Project

Okay, let's assume you've just generated a file with IDs. The script expects **only one** argument: path to a text file which contains your rivals IDs (the path can be relative/absolute). Now, let's run the script. Here's how:

```python main.py {path}```.

#### A Concrete Example

In *data* folder, there's a file called *example_file_with_ids.txt*. Its content looks like this:

```
4668
29104
64342
829593
```

Here's how the script can be run with the aforemetnioned file:

```
python main.py data/example_file_with_ids.txt
```

# Contribution

If you have any questions or notice that something doesn't work correctly, you can send me a DM on [Twitter](https://twitter.com/arndff_). 

Good luck in beating your rivals! 😉
