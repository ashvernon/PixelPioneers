# PixelPioneers

A simple Pygame project inspired by the classic Lemmings game.

## Requirements

- Python 3.8 or newer
- Pygame 2.6.1

## Setup

Install the dependencies using pip:

```bash
pip install -r requirements.txt
```

## Running the Game

After installing the requirements, run the main module:

```bash
python main.py
```

This will launch the PixelPioneers window.

## Lemming Skills

During the game you can assign skills to individual lemmings using the toolbar
at the top of the window:

- **dig** – dig the tile below.
- **build** – place a tile in front of the lemming.
- **block** – stand still and block others.
- **umbrella** – slow down falling speed.

## Level Creator

You can design your own maps using the graphical level creator tool:

```bash
python level_creator.py my_map.txt
```

Left click places the selected tile while right click erases. Use the mouse
wheel or number keys (1-3) to change the current tile type. When you are happy
with the layout, press `S` to save your map.
