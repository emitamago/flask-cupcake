from flask import Flask, render_template, request, redirect, jsonify
from models import db, connect_db, Cupcake
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes-app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "secret"

debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route('/')
def cupcakes_index():
    return render_template('index.html')


@app.route('/cupcakes')
def show_cupcakes():
    """ Show all cupcakes """

    # Get all cupcakes from database
    cupcakes = Cupcake.query.all()

    serialized_cupcakes = [Cupcake.serialize(cupcake) for cupcake in cupcakes]

    return jsonify(cupcakes=serialized_cupcakes)


@app.route('/cupcakes', methods=['POST'])
def add_cupcake():
    """ Add a cupcake to database and return response with json """

    # Get cupcake info from json input
    cupcake = request.json
    
    # Create new cupcake instance
    new_cupcake = Cupcake(flavor=cupcake['flavor'], size=cupcake['size'], 
                          rating=cupcake['rating'], image=cupcake['image'] or None)

    # Add to database
    db.session.add(new_cupcake)
    db.session.commit()

    return jsonify(cupcake=Cupcake.serialize(new_cupcake))


@app.route('/cupcakes/<int:cupcake_id>', methods=['PATCH'])
def update_cupcake(cupcake_id):
    """update cupcake with user's input """
   
    cupcake = Cupcake.query.get(cupcake_id)

    user_input = request.json

    cupcake.flavor = user_input['flavor']
    cupcake.size = user_input['size']
    cupcake.rating = user_input['rating']
    cupcake.image = user_input['image'] or None

    db.session.commit()

    return jsonify(cupcake=Cupcake.serialize(cupcake))


@app.route('/cupcakes/<int:cupcake_id>', methods=['DELETE'])
def delete_cupcake(cupcake_id):
    """update cupcake with user's input """
   
    cupcake = Cupcake.query.get(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify({'message': 'deleted'})