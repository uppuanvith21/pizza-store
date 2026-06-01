from flask import Flask, render_template, request

app = Flask(__name__)

# Pizza menu data
PIZZAS = [
    {
        "id": "margherita",
        "name": "Margherita",
        "description": "Classic tomato, fresh mozzarella & basil",
        "price": 12.99,
        "emoji": "🍅"
    },
    {
        "id": "pepperoni",
        "name": "Pepperoni Blaze",
        "description": "Double pepperoni with smoky mozzarella",
        "price": 15.99,
        "emoji": "🔥"
    },
    {
        "id": "bbq_chicken",
        "name": "BBQ Chicken",
        "description": "Grilled chicken, BBQ sauce & red onions",
        "price": 16.99,
        "emoji": "🍗"
    },
    {
        "id": "veggie",
        "name": "Garden Veggie",
        "description": "Bell peppers, mushrooms, olives & spinach",
        "price": 13.99,
        "emoji": "🥗"
    },
]

SIZES = ["Small (8\")", "Medium (12\")", "Large (16\")", "XL (18\")"]
SIZE_MULTIPLIERS = {"Small (8\")": 0.8, "Medium (12\")": 1.0, "Large (16\")": 1.3, "XL (18\")": 1.6}

CRUSTS = ["Thin Crust", "Classic Hand-Tossed", "Stuffed Crust", "Gluten-Free"]
EXTRAS = ["Extra Cheese", "Jalapeños", "Mushrooms", "Olives", "Onions"]


@app.route("/")
def home():
    return render_template("index.html", pizzas=PIZZAS)


@app.route("/order", methods=["GET", "POST"])
def order():
    if request.method == "POST":
        # Get form data
        pizza_id = request.form.get("pizza")
        size = request.form.get("size")
        crust = request.form.get("crust")
        extras = request.form.getlist("extras")
        customer_name = request.form.get("name")
        phone = request.form.get("phone")

        # Find selected pizza
        selected_pizza = next((p for p in PIZZAS if p["id"] == pizza_id), None)

        # Conditional logic: calculate price
        if selected_pizza and size:
            base_price = selected_pizza["price"]
            multiplier = SIZE_MULTIPLIERS.get(size, 1.0)
            extras_cost = len(extras) * 1.50
            total_price = (base_price * multiplier) + extras_cost

            # Conditional: apply discount
            discount = 0
            discount_msg = ""
            if len(extras) >= 3:
                discount = total_price * 0.10
                discount_msg = "10% discount applied for 3+ toppings! 🎉"

            final_price = total_price - discount

            return render_template(
                "confirmation.html",
                pizza=selected_pizza,
                size=size,
                crust=crust,
                extras=extras,
                name=customer_name,
                phone=phone,
                base_price=base_price,
                total_price=total_price,
                discount=discount,
                discount_msg=discount_msg,
                final_price=final_price,
            )

    # GET request — show the order form
    return render_template("order.html", pizzas=PIZZAS, sizes=SIZES, crusts=CRUSTS, extras=EXTRAS)


@app.route("/menu")
def menu():
    return render_template("menu.html", pizzas=PIZZAS)


if __name__ == "__main__":
    app.run(debug=True)