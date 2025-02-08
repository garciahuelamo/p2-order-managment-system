from flask import Flask, request, jsonify
import json

app = Flask(__name__)

class Product:
    def __init__(self, key, value):
        self.key = key 
        self.value = value 
        self.right = None 
        self.left = None 

class BST:
    def __init__(self):
        self.root = None
    
    def insert(self, key, value):
        if self.root is None:
            self.root = Product(key, value) 
        else:
            self._insert(self.root, key, value)
    
    def _insert(self, current, key, value):
        if key < current.key:
            if current.left is None:
                current.left = Product(key, value)
            else:
                self._insert(current.left, key, value)
        elif key > current.key:
            if current.right is None:
                current.right = Product(key, value)
            else:
                self._insert(current.right, key, value)
        else: 
            return ValueError("Duplicates products are not allowed") 
    
    def _search(self, current, key):
        if current is None:
            return None
        
        if key == current.key:
            return current.value
        elif key < current.key:
            return self._search(current.left, key)
        else:
            return self._search(current.right, key)
    
    def print_tree(self):
        if self.root is None:
            print("Tree is empty")
        else:
            print("Status in-order:")
            self._print_in_order(self.root)
    
    def _print_in_order(self, current):
        if current is None:
            self._print_in_order(current.left)
            print(f"Clave: {current.key}, Valor: {current.value}")
            self._print_in_order(current.right)

bst = BST()

@app.route("/add_product", methods=["POST"])
def add():
    data = request.get_json()
    try:
        key = int(data["id"])
        value = data["value"]
        bst.insert(key, value)
        return jsonify({"message": "Product added successfully!"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except KeyError:
        return jsonify({"error": "Missing 'id' or 'value' in request"}), 400

@app.route("/get_products", methods=["GET"])
def print_tree():
    bst.print_tree()  # Print the tree in-order in the console
    print(bst.print_tree)
    return jsonify({"message": "Tree structure printed to console"}), 200

@app.route("/search_product/<int:id>", methods=["GET"])
def search(id):
    product_value = bst._search(bst.root, id)
    try:
        if product_value is not None:
            return jsonify({"message": "Product found", "id": id, "value": product_value}), 200
        else:
            return jsonify({"error": "Product not found"}), 404
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except KeyError:
        return jsonify({"error": "Missing 'id' in request"}), 400

if __name__ == "__main__":
    app.run(debug=True)

