# SA_scorer_gui

### Introduction

This is a small graphical user interface I built that scores raw data for Spontaneous Alternation. Originally I had been using the scoring code by itself in iPython notebooks to score my data, however other people in my lab wanted to be able to use it to score their own data, as I could do it much faster and with less error than by doing it by hand. This repository is the result of my work.

### Spontaneous Alternation

If you are not a behavioral neuroscientist, you are probably wondering what spontaneous alternation is. In short its a behavioral task for rats or mice that tests an animals spatial learning and working memory. The way it works is, an animal is placed on a 4-arm plus maze (other mazes such as radial mazes can be used as well, but this GUI only works for data from 4-arm plus mazes) for certain amount of time, and then the arms that the animal enters are recorded. An animal is said to have good spatial learning and working memory if they don't enter the same arm within 4 choices, this is called an alternation because the animal alternated which arm it entered for each opportunity it had in the previous 4 opportunities (the first 3 choices do not count towards their score since they didn't have opportunities to make a full alternation). A researcher can then tally up the number of times that an animal alternated and compare groups against each other. So therefore, if your experimental manipulation is hypothesized to improve spatial learning and working memory, you would expect that group to have a significantly higher mean alternation score than your control group and vice versa.

### How it Works

First a user starts the program. Next they upload a file of raw data (a template and an example file can be downloaded from the excel files directory). Next they choose how many choices they would like scored, whether full, custom, from first 6 or 12 minutes. Finally they choose a save name and location and finally press submit. At this point a file with the scored data, and description data if the group column is filled out, is saved into the specified location. 
