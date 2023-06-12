from flask import Flask, jsonify, request

app = Flask(__name__)
app.debug = True


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/super_simple')
def super_simple():
    return jsonify(message='Hello from the super simple Planetary API.')


@app.route('/not_found')
def not_found():
    return jsonify(message='Some fancy error message.'), 404


@app.route('/parameters')
def parameters():
    name = request.args.get('name')
    age = int(request.args.get('age'))

    if(age<18):
        return jsonify(message=f'Sorry {name}, you are not old enough.'), 401
    else:
        return jsonify(message=f'{name}, you are old enough.')


@app.route('/url_parameters/<string:name>/<int:age>')
def url_parameters(name: str, age: int):
    if(age<18):
        return jsonify(message=f'Sorry {name}, you are not old enough.'), 401
    else:
        return jsonify(message=f'{name}, you are old enough.')


if __name__ == '__main__':
    app.run()
