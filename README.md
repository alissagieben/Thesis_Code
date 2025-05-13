# Thesis_Code
The code I wrote for my thesis about human-agent collaboration while playing The Game

My thesis set our to answer the research question How does the ability to communicate influence collaboration when viewed through a human and an agents performance of `The Game'?
In order to do so, I created two agents, one that would play the game with communication, and one that would play without communication.

The files contained in yes_comm contain everything for the agent that can communicate. 
The files contained within no_comm contain everything for the agent that cannot communicate.

Both the agents will generate two output files during the game. One called 'output.txt' that contains a detailled log of every move made.
The other output file is called 'simple_output.txt' and contains a less detailed, more straightforward dataset.

Then finally, the result parser. After the experiment this was used to pass the generated simple output files through to tally up certain values and generate an even cleaner data overview.