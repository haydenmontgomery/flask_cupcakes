"""Flask app for Cupcakes"""

from flask import Flask, request, jsonify, render_template, redirect
from models import db, connect_db, Cupcake
from forms import CupcakeForm

def create_app(database_name, testing=False):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql:///{database_name}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SECRET_KEY'] = "abc123"
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

    if testing:
        app.config["WTF_CSRF_ENABLED"] = False

    app.app_context().push()
    connect_db(app)
    db.create_all()

    @app.route('/', methods=["GET", "POST"])
    def index_page():
        form = CupcakeForm()
        if form.validate_on_submit():
            flavor = form.flavor.data
            size = form.size.data
            rating = form.rating.data
            print("*******************************************")
            print(form.image.data is "")
            print("*******************************************")
            if form.image.data != "":
                image = form.image.data
                cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)
            else:
                cupcake = Cupcake(flavor=flavor, size=size, rating=rating)
            db.session.add(cupcake)
            db.session.commit()
            return redirect('/')
        else:
            return render_template('index.html', form=form)

    @app.route('/api/cupcakes')
    def list_cupcakes():
        all_cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
        return jsonify(cupcakes=all_cupcakes)
    
    @app.route('/api/cupcakes/<int:id>')
    def get_cupcake(id):
        cupcake = Cupcake.query.get_or_404(id)
        return jsonify(cupcake=cupcake.serialize())
    
    @app.route('/api/cupcakes', methods=["POST"])
    def create_cupcake():
        new_cupcake = Cupcake(flavor=request.json["flavor"],
                              size=request.json["size"],
                              rating=request.json["rating"],
                              image=request.json["image"])
        db.session.add(new_cupcake)
        db.session.commit()
        response_json = jsonify(cupcake=new_cupcake.serialize())
        return (response_json, 201)
    
    @app.route('/api/cupcakes/<int:id>', methods=["PATCH"])
    def update_cupcake(id):
        cupcake = Cupcake.query.get_or_404(id)
        cupcake.flavor = request.json.get('flavor', cupcake.flavor)
        cupcake.size = request.json.get('size', cupcake.size)
        cupcake.rating = request.json.get('rating', cupcake.rating)
        cupcake.image = request.json.get('image', cupcake.image)
        db.session.commit()
        return jsonify(cupcake=cupcake.serialize())
    
    @app.route('/api/cupcakes/<int:id>', methods=["DELETE"])
    def delete_cupcake(id):
        cupcake = Cupcake.query.get_or_404(id)
        db.session.delete(cupcake)
        db.session.commit()
        return jsonify(message="deleted")

    return app

if __name__=='__main__':
    app = create_app('cupcakes')
    #connect_db(app)
    app.run(debug=True)