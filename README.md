# Disclaimer
This program was only tested on [Hyprland](https://hypr.land/), installed on an [Arch Linux](https://archlinux.org/) system. It should work on other wayland compositors, but no guarantees.

# Dependencies
- `grim`
- `slurp`
- [`manga-ocr`](https://github.com/kha-white/manga-ocr)

# How to run
1. Clone this repository and `cd` into the cloned directory.
```bash
git clone https://github.com/Atr-eus/Fumiko.git
cd Fumiko
```
2. Start up a local server to display the OCR output in your browser.
```fish
python3 -m http.server 8765 --directory .
```
3. Install required dependencies and run the `start.py` script.
```fish
python start.py
```
You probably want to make a keybind for this.

4. Browse to `http://localhost:8765/` to view the OCR output from your taken screenshot. Lastly, it is advised to install [Yomichan](https://github.com/FooSoft/yomichan) or another pop-up dictionary of your choice to look up words in your browser without having to copy paste the text.

# Future work
I'll try to package this using `pip`.
