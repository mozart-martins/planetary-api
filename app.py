import os

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager, jwt_required, create_access_token


app = Flask(__name__)
app.debug = True
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'planets.db')
app.config['JWT_SECRET_KEY'] = 'super-secret'

db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)


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


@app.route('/planets', methods=['GET'])
def planets():
    planet_list = Planet.query.all()
    return planets_schema.dump(planet_list)


@app.route('/register', methods=['POST'])
def register():
    email = request.form.get('email')
    test = User.query.filter_by(email = email).first()

    if test:
      return jsonify(message='This e-mail already exits.'), 409
    else:
      first_name = request.form.get('first_name')
      last_name = request.form.get('last_name')
      password = request.form.get('password')
      user = User(first_name=first_name, last_name=last_name, email=email, password=password)
      db.session.add(user)
      db.session.commit()
      return jsonify(message='User created successfully.'), 201


@app.route('/login', methods=['POST'])
def login():
    if request.is_json:
        email = request.json.get('email')
        password = request.json.get('password')
    else:
        email = request.form.get('email')
        password = request.form.get('password')

    test = User.query.filter_by(email = email)

    if test:
        access_token = create_access_token(identity=email)
        return jsonify(message='Login succeeded!', access_token=access_token)
    else:
        return jsonify(message='Bad e-mail or password.'), 401




class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'email', 'password')

user_schema = UserSchema()
users_schema = UserSchema(many=True)


class Planet(db.Model):
    __tablename__ = 'planets'
    planet_id = Column(Integer, primary_key=True)
    planet_name = Column(String)
    planet_type = Column(String)
    home_star = Column(String)
    mass = Column(Float)
    radius = Column(Float)
    distance = Column(Float)

class PlanetSchema(ma.Schema):
    class Meta:
        fields = ('planet_id',
                  'planet_name',
                  'planet_type',
                  'home_star',
                  'mass',
                  'radius',
                  'distance')


planet_shema = PlanetSchema()
planets_schema = PlanetSchema(many=True)

@app.cli.command('db_create')
def db_create():
  db.create_all()
  print('Database created!')


@app.cli.command('db_drop')
def db_drop():
  db.drop_all()
  print('Database dropped!')


@app.cli.command('db_seed')
def db_seed():
    mercury = Planet(planet_name='Mercury',
                    planet_type='Class D',
                    home_star='Sol',
                    mass=3.258e23,
                    radius=1516,
                    distance=35.88e6)

    venus = Planet(planet_name='Venus',
                    planet_type='Class K',
                    home_star='Sol',
                    mass=4.867e24,
                    radius=2760,
                    distance=67.24e6)

    earth = Planet(planet_name='Earth',
                    planet_type='Class M',
                    home_star='Sol',
                    mass=5.872e24,
                    radius=3858,
                    distance=82.88e6)

    db.session.add(mercury)
    db.session.add(venus)
    db.session.add(earth)

    test_user = User(first_name='William',
                    last_name='Herschell',
                    email='test@test.com',
                    password='P@ssword')

    db.session.add(test_user)

    db.session.commit()
    print('Database seeded!')


if __name__ == '__main__':
    app.run()
