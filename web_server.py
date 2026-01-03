from flask import Flask, send_file, jsonify, request, send_from_directory
import threading
import time
from io import BytesIO
from game_core import GameCore

app = Flask(__name__, static_folder='.')

game = GameCore()
latest_frame = None
frame_lock = threading.Lock()
running = True

def game_loop():
    global latest_frame, running
    # update at game's speed (game.speed moves per second)
    while running:
        start = time.time()
        game.tick()
        img_bytes = game.render_png_bytes()
        with frame_lock:
            latest_frame = img_bytes
        # sleep a bit (aim for 30 fps render regardless of game speed)
        elapsed = time.time() - start
        time.sleep(max(0, 1/30 - elapsed))

thread = threading.Thread(target=game_loop, daemon=True)
thread.start()

@app.route('/')
def index():
    return send_from_directory('.', 'web_index.html')

@app.route('/frame')
def frame():
    with frame_lock:
        if latest_frame is None:
            return ('', 204)
        buf = BytesIO(latest_frame)
    return send_file(buf, mimetype='image/png')

@app.route('/input', methods=['POST'])
def input_route():
    data = request.json or {}
    key = data.get('key')
    if key == 'left': game.set_direction('left')
    if key == 'right': game.set_direction('right')
    if key == 'up': game.set_direction('up')
    if key == 'down': game.set_direction('down')
    if key == 'restart': game.reset()
    return jsonify({'ok': True})

@app.route('/state')
def state():
    return jsonify(game.get_state())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)
