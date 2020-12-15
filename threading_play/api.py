import time
import flask
import random

random.seed()
app = flask.Flask(__name__)


@app.route('/hit', methods=['POST'])
def get_hit():
    if flask.request.method == 'POST':
        if flask.request.is_json:
            output = flask.json.dumps(flask.request.get_json())
            with open('dump.json', 'a', encoding='utf-8') as out_file:
                out_file.write(f'{output}\n')
    return {}


@app.route('/slow', methods=['POST'])
def slow_route():
    rnd_slow = random.randint(1, 10)
    if flask.request.method == 'POST':
        if flask.request.is_json:
            output = flask.json.dumps(flask.request.get_json())
            time.sleep(rnd_slow)
            with open('dump.json', 'a', encoding='utf-8') as out_file:
                out_file.write(f'{output}\n')
    return {}


if __name__ == '__main__':
    app.run(debug=True)
