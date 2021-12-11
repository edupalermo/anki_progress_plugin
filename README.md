# anki_progress_plugin

## TODO list
- [ ] Improve README.md
- [ ] Improve text position on current progress
- [ ] New progress bar with gradient background
- [ ] New Graph widget for future cards
- [ ] Remove from done card with relearn state

## Configuring PyCharm
###### Configure virtual environment

Reference: https://www.jetbrains.com/help/pycharm/creating-virtual-environment.html

###### Install Anki’s bundled source code so you can get type completion
```python
import subprocess

subprocess.check_call(["pip3", "install", "--upgrade", "pip"])
subprocess.check_call(["pip3", "install", "mypy", "aqt"])
```
Reference: https://addon-docs.ankiweb.net/editor-setup.html 

## Reference
###### Basic writing and formatting syntax
Reference: https://docs.github.com/en/github/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax