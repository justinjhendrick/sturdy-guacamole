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
Use your mouse to point your flashlight and reach the blue square to win
* A: move left
* D: move right
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
python main.py --map-file MyNewMap_map.json --debug --map-editor
```