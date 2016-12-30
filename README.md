# SimpleCellularAutomaton

GameOfLife.py is written for python 2.7

To use from commandline there are four options:

1. Use the default test board (provided with the specs) that is hardcoded in

   $ python GameOfLife.py

2. Pass in the gameboard in string format as an argument (if using bash, it must be wrapped in '' and
   preceded with $)

   $ python GameOfLife.py $'1111\n0110\n1010\n0000'

3. Pass in the 'file' arg, then the name of a file containing the gameboard

   $ python GameOfLife.py file gameboard

4. Same as #3, but add the 'loop' arg, to overwrite in the input file with the new output,
   allowing the command to be called repeatedly and the gameboard to consecutively progress

   $ python GameOfLife.py file gameboard3 loop
   $ python GameOfLife.py file gameboard3 loop
   ...
