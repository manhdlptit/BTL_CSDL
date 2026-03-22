from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SECRET_KEY"] = "makhoabimat"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///shop.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    item = db.Column(db.String(100))
    price = db.Column(db.String(100))


    def __init__(self, item, price):
        self.item = item
        self.price = price + "VNĐ"

def check_item():
    items = Item.query.all()
    list_items = []
    for item in items:
        list_items.append({
            "id" : item.id,
            "item" : item.item,
            "price" : item.price
        })
    return jsonify(list_items)
@app.route("/", methods = ["GET", "POST", "DELETE"])
def create_item():
    data_item = request.form.get("get_item")
    data_price = request.form.get("get_price")
    if data_item and data_price:
        new_item = Item(data_item, data_price)
        db.session.add(new_item)
        db.session.commit()
    return redirect(url_for('index'))
def get_item_with_id(id):
    found_id = db.session.get(Item, id)
    if found_id is None:
        return jsonify({"error" : "error"}), 404
    return jsonify({
        "id" : found_id.id,
        "item" : found_id.item,
        "price" : found_id.price
    })

def delete_item_with_id(id):
    found_id = db.session.get(Item, id)
    if found_id is None:
        return jsonify({"error" : "error"}), 404
    db.session.delete(found_id)
    db.session.commit()
    return jsonify({"ok": "ok"}), 200
    


@app.route("/index", methods = ["GET"])
def index():
    return render_template("manager_page.html")

@app.route("/manager", methods = ["GET", "POST"])
def check_method_of_manager():
    if request.method == "GET":
        return check_item()
    if request.method == "POST":
        return create_item()

@app.route("/manager/<int:id>", methods = ["GET", "DELETE"])
def check_method_of_manager_with_id(id):
    if request.method == "GET":
        return get_item_with_id(id)
    if request.method == "DELETE":
        return delete_item_with_id(id)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8888)
