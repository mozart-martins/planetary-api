from flask import Flask

app = Flask(__name__)
app.debug = True


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/super_simple')
def super_simple():
  return 'Hello from the super simple Planetary API. boo yah'


if __name__ == '__main__':
    app.run()
