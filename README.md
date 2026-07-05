# Purpose
This project is mainly for me to get engauged with tracking my both my time and my money. It is  adapted to my specific way of thinking about time and money management.

# Usage
Click the `Add` button to add an entry to the table widget. Each row in the table widget represents a specific purchase you have made. Then enter the name of the purchase, where you made that purchase, it's price, date, and a `tag`. Tags are ways of categorizing you puchases. For example, you could have a tag for `groceries`. Tags are currently used to display a breakdown by category in the pie chart widget. The will be used in the future for filtering and other features that are currently not implemented.

# Building and development.
Below shows how to run the app through `Python` as well as create an executable with `PyInstaller`.  

```
# Commands should be called in the root directory of this project.

python -m venv .venv                # Create a virtual environment.
source .venv/bin/activate           # Activate the virtual environment.
.venv\Scripts\activate              # Use this line if you are on windows.
pip install -r requirements.txt     # Install Python packages.
python src/main.py                  # This will run the application!
```

If you want to bundle this program with `PyInstaller`, run `pyinstaller src/main.py`. This will create an executable in `dist/main/`. `main.exe` depends on anything in `dist/main`, so if you want to move the program around, it must stay in that same directory!

# Dependencies
- `Python: 3.14.5`
- `Windows` or `Ubuntu` (This may work outside these platforms, but this app has only been tested on Windows and WSL)