from app import create_app
from models import db, Cupcake

app = create_app("cupcakes", testing=False)

db.drop_all()
db.create_all()

c1 = Cupcake(
    flavor="cherry",
    size="large",
    rating=5,
)

c2 = Cupcake(
    flavor="chocolate",
    size="small",
    rating=9,
    image="https://images.unsplash.com/photo-1587668178277-295251f900ce?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTR8fHBsYWluJTIwY3VwY2FrZXxlbnwwfHwwfHx8MA%3D%3D"
)

db.session.add_all([c1, c2])
db.session.commit()