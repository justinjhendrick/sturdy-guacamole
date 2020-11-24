# STURDY-GUACAMOLE

INSTALL
-------
Install Python and Pip

```
$ pip install pygame
$ pip install Box2D
```

PLAY
----
Reach the blue square to win!
* A: move left
* D: move right
* SPACE: jump
* mouse position: point flashlight

```
python main.py --map-file stairs_map.json
```

MAP EDITOR
------------
You can build your own maps for this game
* Hold the `r` key, click and drag to make rectangles
* Hold the `x` key, click to delete objects

```
python main.py --map-file new_map.json --debug --map-editor
```

`new_map.json` only has walls around the edges and you can add more walls where you'd like. If you want to start a fresh map, choose a nonexistent file name that ends with "_map.json" and put it after `--map-file` in the above command.

TODO: Add ability to create blue goal square in the level editor.