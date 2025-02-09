from flask import Flask, request, jsonify

app = Flask(__name__)

class Product:
    def __init__(self, key, value):
        self.key = key 
        self.value = value 
        self.right = None 
        self.left = None 

class BSTProducts:
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
            raise ValueError("Duplicate products are not allowed") 

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
            return []
        else:
            return self._print_in_order(self.root, [])

    def _print_in_order(self, current, result):
        if current is not None:
            self._print_in_order(current.left, result)
            result.append({"id": current.key, "value": current.value})
            self._print_in_order(current.right, result)
        return result

class Order:
    def __init__(self, id, products):
        self.id = id
        self.products = products
        self.next = None

class LLOrders:
    def __init__(self): 
        self.head = None
    
    def add(self, id, products):
        new_node = Order(id, products)
        if self.head is None: 
            self.head = new_node
        else:
            current = self.head 
            while current.next: 
                current = current.next
            current.next = new_node 

    def find(self, id):
        current = self.head
        while current:
            if current.id == id:
                return current.products
            current = current.next
        return None

    def delete(self, id):
        if self.head is None:
            return 
        if self.head.id == id:
            self.head = self.head.next
            return 
        current = self.head
        while current.next:
            if current.next.id == id:
                current.next = current.next.next
                return
            current = current.next

bst = BSTProducts()
linkedlist = LLOrders()

@app.route("/add_product", methods=["POST"])
def add_product():
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
def get_products():
    products = bst.print_tree()
    return jsonify({"products": products}), 200

@app.route("/search_product/<int:id>", methods=["GET"])
def search(id):
    product_value = bst._search(bst.root, id)
    if product_value is not None:
        return jsonify({"message": "Product found", "id": id, "value": product_value}), 200
    else:
        return jsonify({"error": "Product not found"}), 404

@app.route("/add_order", methods=["POST"])
def add_order():
    data = request.get_json()

    try:
        order_id = int(data["id"])
        products = data.get("products", [])

        if not isinstance(products, list):
            return jsonify({"error": "The 'products' field must be a list"}), 400

        order_products = [] 

        for item in products:
            if not isinstance(item, dict):
                return jsonify({
                    "error": "Each item in 'products' must be a dictionary with 'product_id' and 'quantity'.",
                    "invalid_item": item
                }), 400

            if "product_id" not in item or "quantity" not in item:
                return jsonify({"error": "Each product must contain 'product_id' and 'quantity'"}), 400

            product_id = int(item["product_id"])
            quantity = int(item["quantity"])

            product_value = bst._search(bst.root, product_id)

            if product_value is None:
                return jsonify({"error": f"Product with ID {product_id} does not exist"}), 400

            order_products.append({"product_id": product_id, "quantity": quantity})

        linkedlist.add(order_id, order_products)

        print(f"Added order {order_id}: {order_products}")

        return jsonify({"message": "Order added successfully!", "order": order_products}), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except KeyError:
        return jsonify({"error": "Missing 'id' or 'products' in request"}), 400

@app.route("/get_orders", methods=["GET"])
def get_orders():
    orders = []
    current = linkedlist.head

    print("Fetching orders...")

    while current:
        orders.append({"order_id": current.id, "products": current.products})
        current = current.next

    print(f"Orders: {orders}")

    return jsonify({"orders": orders}), 200

@app.route("/search_order/<int:id>", methods=["GET"])
def search_order(id):
    order_data = linkedlist.find(id)
    if order_data is not None:
        return jsonify({"message": "Order found", "order_id": id, "products": order_data}), 200
    else:
        return jsonify({"error": "Order not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
