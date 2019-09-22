# Setting up environment (VS Code)
1. Install Python 3.7.X and Conda
2. From conda prompt : `conda create -n logicmlbot1 pip`
3. `conda activate logicmlbot1`
4. You may need to install Visual Studio with C++ workload enabled to get past some of the dependencies. There is probably a way to get it working with just the build tools installed but I couldn't get it working.

## Environment to just consume rasa without debugging it
1. Install rasa as per https://rasa.com/docs/rasa/user-guide/installation/#quick-installation.

```json
{
    "python.pythonPath": "C:\\Users\\LeeBorlace\\Anaconda3\\envs\\logicmlbot1\\python.exe"
}
```

## Environment to debug rasa itself
There might be better ways to do this - I'm not a Python expert!
1. Clone rasa from https://github.com/RasaHQ/rasa.
2. Install rasa's prereqs but not rasa itself - see https://rasa.com/docs/rasa/user-guide/installation/#building-from-source. I.e. `pip install -r requirements.txt`
3. `pip install ptvsd`
4. From where you cloned rasa, edit `/rasa/rasa/__main__.py` to include the breakpoint / debug stuff (ptvsd) in the beginning of main() -
```python
import ptvsd
ptvsd.enable_attach()
print("DEBUG? Y/N")
line = sys.stdin.readline()
if line == 'y' or line =='Y" :
    print("ATTACH DEBUGGER NOW...")
    ptvsd.wait_for_attach()
```
5. From conda prompt (workaround for an issue) : ```pip install gast==0.2.2```
6. Ensure your launch.json looks like the following.

```
{
    "name": "Python: Remote Attach",
    "type": "python",
    "request": "attach",
    "port": 5678,
    "host": "localhost",
    "pathMappings": [
        {
            "localRoot": "${workspaceFolder}",
            "remoteRoot": "${workspaceFolder}"
        }
    ]
}
```

7. Set up Python path as appropriate in .vscode

```json
{
    "python.pythonPath": "C:\\Users\\LeeBorlace\\Anaconda3\\envs\\logicmlbot1\\python.exe"
}
```

# Debugging  (VS Code)
## Debugging rasa
1. Open the root folder of the rasa repo in Visual Studio Code.
2. Open a conda terminal, cd to where your bot is (doesn't have to be in the Rasa folder) and run the following. This sets PYTHONPATH so rasa resolves, and changes directory to where the bot under development is. You may need to change relative paths to correspond to where rasa and the bot sit in relation to each other.

```
conda activate logicmlbot1
set PYTHONPATH=C:\Users\LeeBorlace\Documents\GitHub\logic-ml-bot\v1;C:\Users\LeeBorlace\Documents\GitHub\rasa
cd C:\Users\LeeBorlace\Documents\GitHub\logic-ml-bot\v1
python ..\..\rasa\rasa\__main__.py train --force
python ..\..\rasa\rasa\__main__.py shell
 ```

2. When it runs it will prompt that you can attach the debugger.

Note 1 : I've also created convenience Windows scripts debugtrain.bat and debugshell.bat to trigger the above. You'd need to customise them for your environment if you want to use them.
Note 2 : If you want to debug the custom actions, policy, component, you can run the above, but then attach the debugger from the VS Code instance which has the custom bot code open.

## Debugging actions
Note : unless you muck around with the config a bit (not covered here), you can only debug either rasa itself or the actions, but not both at the same time

1. Open another conda prompt
2. `conda activate logicmlbot1`
3. cd to the location of the bot e.g. `cd C:\Users\LeeBorlace\Documents\GitHub\logic-ml-bot\v1`
4. `set PYTHONPATH=C:\Users\LeeBorlace\Documents\GitHub\logic-ml-bot\v1;C:\Users\LeeBorlace\Documents\GitHub\rasa`
5. invoke rasa `python ..\..\rasa\rasa\__main__.py run actions --actions logicmlbot.actions.logicmlbot_actions`
6. Attach debugger if you wish!

Note : I've also created convenience Windows script debugactions.bat to trigger the above. You'd need to customise them for your environment if you want to use them.

# Running without debugging rasa
If you don't want to debug rasa then run rasa as per the docco. However, make sure PYTHONPATH is set to allow Python to find any custom modules for this bot, e.g. `set PYTHONPATH=C:\Users\LeeBorlace\Documents\GitHub\logic-ml-bot\v1`. 

