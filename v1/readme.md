# Setting up environment
These are the steps if you want to be able to debug rasa. There might be better ways to do this - I'm not a Python expert!

1. Install Python 3.7.X and Conda
2. From conda prompt : `conda create -n logicmlbot1`
3. `conda activate logicmlbot1`
4. `conda install pip`
5. Clone rasa from https://github.com/RasaHQ/rasa.
6. Install rasa's prereqs but not rasa itself - see https://rasa.com/docs/rasa/user-guide/installation/#building-from-source. I.e. `pip install -r requirements.txt`
7. `pip install ptvsd`
8. From where you cloned rasa, edit `/rasa/rasa/__main__.py` to include the breakpoint / debug stuff (ptvsd) -
```python
import ptvsd
ptvsd.enable_attach()
ptvsd.wait_for_attach()
```
9. From conda prompt (workaround for an issue) : ```pip3 install gast==0.2.2```
10. Ensure your launch.json looks like the following.

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

# Debugging
1. Open a conda terminal, go to where your bot is (doesn't have to be in the Rasa folder) and run the following. This sets PYTHONPATH so rasa resolves, and changes directory to where the bot under development is. You may need to change relative paths to correspond to where rasa and the bot sit in relation to each other.

```
conda activate logicmlbot1
set PYTHONPATH=C:\Users\Lee\Documents\GitHub\rasa
cd C:\Users\Lee\Documents\GitHub\logic-ml-bot\v1
python ..\..\rasa\rasa\__main__.py train
python ..\..\rasa\rasa\__main__.py shell
 ```

2. When it runs it will prompt that you can attach the debugger.

