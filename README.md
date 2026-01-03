# Snake (Pygame)

Classic Snake game implemented in Python using Pygame.

Run instructions

1. Create a virtual environment (recommended) and install dependencies, then run the Flask web server:

```bash
python -m pip install -r requirements.txt
```

2. Run the game or the web server:

```bash
python snake.py
```

To run the Flask web server, use the following commands:

- To run the Flask web server (optional):

```powershell
cd C:\xampp\htdocs\games\snake
python -m pip install -r requirements.txt
python web_server.py
```

Open http://localhost:8001/ in your browser. Controls: Arrow keys / WASD to move, `R` to restart.

Browser-only version (no Python):

- Open `index.html` in your browser (double-click the file) to play the standalone browser build.


Notes on setup:
- If `python -m pip install -r requirements.txt` fails, ensure your Python and pip are properly installed and on PATH. Run `python -m pip install --upgrade pip` first if needed.
- On Windows, headless pygame may require SDL dependencies; if you see pygame display errors, try running without the headless server or use the provided browser-only `index.html` (if present).
Controls

- Arrow keys: move the snake
Arrow keys: move the snake
R: restart after game over
Q or ESC: quit
T: cycle color themes
M: toggle background music on/off (requires `music.mp3`)
Notes

- The game saves the high score in `highscore.txt` in the same folder.
The game saves the high score in `highscore.txt` in the same folder.
Optional sound files (place in same folder): `eat.wav`, `gameover.wav`, `music.mp3`.
On Windows you can run `run.bat` to install deps and start the game.
