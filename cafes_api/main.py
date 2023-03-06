from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.app_context().push()


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


db.create_all()


@app.route("/")
def home():
    return render_template("index.html")
    

## HTTP GET - Read Record
@app.route("/random", methods=["GET"])
def get_random_cafe():
    cafes = db.session.query(Cafe).all()
    random_cafe = random.choice(cafes)
    return jsonify(random_cafe.to_dict())


@app.route("/search", methods=["GET"])
def get_cafe_by_location():
    cafes = db.session.query(Cafe).filter_by(location=request.args.get("loc"))
    print(cafes)
    return jsonify([cafe.to_dict() for cafe in cafes])


@app.route("/all", methods=["GET"])
def get_all_cafes():
    cafes = db.session.query(Cafe).all()
    return jsonify([cafe.to_dict() for cafe in cafes])


## HTTP POST - Create Record
@app.route("/add", methods=["POST"])
def add_cafe():
    new_cafe = Cafe(name=request.form['name'],
                    map_url=request.form['map_url'],
                    img_url=request.form['img_url'],
                    location=request.form['location'],
                    seats=request.form['seats'],
                    has_toilet=bool(request.form['has_toilet']),
                    has_wifi=bool(request.form['has_wifi']),
                    has_sockets=bool(request.form['has_sockets']),
                    can_take_calls=bool(request.form['can_take_calls']),
                    coffee_price=request.form['coffee_price'])
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify({"success": "Successfully added the new cafe."})


## HTTP PUT/PATCH - Update Record
@app.route("/update-price/<cafe_id>", methods=["PATCH"])
def update_price(cafe_id):
    cafe = Cafe.query.get(cafe_id)
    cafe.coffee_price = request.args.get("new_price")
    db.session.add(cafe)
    db.session.commit()
    return jsonify({"success": "Successfully updated coffee price"})


## HTTP DELETE - Delete Record
@app.route("/report-closed/<cafe_id>", methods=["DELETE"])
def delete_cafe(cafe_id):
    if request.args.get("api_key") == "TopSecretAPIKey":
        Cafe.query.filter_by(id=cafe_id).delete()
        db.session.commit()
        return jsonify({"success": "Successfully deleted the cafe"})
    else:
        return jsonify({"fail": "wrong key/cafe_id does not exist"})


if __name__ == '__main__':
    app.run(debug=True)
