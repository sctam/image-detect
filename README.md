# Image Detect
## Background
This application plays a sound and highlight it when it has detected a reference image (`reference.jpg`) in the image that is being scanned.

## Example Usage
One could detect the following gem in a game on Bejeweled.

![Reference Image](example/reference.jpg)

![Reference Image](example/matchedExample.jpg)

## Setup
Install Tkinter through normal Python distribution. The other dependencies may be installed through `pip`.
```sh
pip install -r requirements.txt
```

## Run

### Python
Simply run the script with Python with the following call.
```sh
python main.py
```

### Build Executable
To make it a standalone executable, use PyInstaller and build with the recommended command below.
```sh
pyinstaller main.py --windowed --onefile
```

## Potential Improvements
- Add mask option to template matching.
- The image may be matched several times without a padded block out.
- Adjustments are too coarse.
- Adjustable refresh rate.