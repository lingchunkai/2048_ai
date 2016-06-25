##INSTALLATION

For the UI, you will need to download and install the [SimpleGUI wrapper](https://pypi.python.org/pypi/SimpleGUITk). Not need for any other steps.

## USAGE

For running and visualizing the agent (defaults to MCTS via UCT)


    >> python hook.py

To change agents (or add your own), edit `hook.py` and change the following line near the bottom to whatever you want.

    >> ai = mcts_2048_ai.TwentyFortyEight_mcts()

For assessment and benchmarking, you may run code directly from the files, for example
 
    >> mcts_2048_ai.py

You may also try other board sizes for fun!
    
## KNOWN ISSUES

* Yes, I know the code is poorly written ;)
* I haven't disabled keyboard input for the gui client. Do not press any keys when the agent is playing!

## CREDITS
* 2048 clone was adapted from [here](https://github.com/MrL1605/CodeSkulptor-Mini-Projects/blob/master/Game-2048.py)
* [CodeSkulptor](http://www.codeskulptor.org/) for simplegui
* Creators of [SimpleGUITk](https://pypi.python.org/pypi/SimpleGUITk)