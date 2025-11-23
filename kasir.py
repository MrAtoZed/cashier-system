import tkinter as tk

pricelist = {
    "Nasi Goreng": 15000,
    "Ayam Bakar": 20000,
    "Es Teh": 5000,
    "Es Jeruk": 7000
}

order = ["Nasi Goreng", "Es Teh"]
payment_status = "Belum Dibayar"

def calculate_total():
    return sum(pricelist[i] for i in order)

root = tk.Tk()
root.title("Display Order")
root.geometry("400x350")

# PRICE LIST
frame_price = tk.LabelFrame(root, text="Price List")
frame_price.pack(fill="x", padx=10, pady=5)

for item, price in pricelist.items():
    tk.Label(frame_price, text=f"{item} - Rp {price}").pack(anchor="w")
from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "secret123"    # sesi login

# ====================
# DATA
# ====================
users = {
    "admin": {"password": "admin123", "role": "admin"},
    "customer": {"password": "cus123", "role": "customer"}
}

pricelist = {
    "Nasi Goreng": 15000,
    "Ayam Bakar": 20000,
    "Es Teh": 5000,
    "Es Jeruk": 7000
}

order_status = {
    "table": None,
    "order": [],
    "payment_method": None,
    "payment_status": "Belum Dibayar"
}

# ====================
# ROUTES
# ====================

@app.route("/")
def home():
    return redirect("/login")

# -------- LOGIN ----------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        uname = request.form["username"]
        passwd = request.form["password"]

        if uname in users and users[uname]["password"] == passwd:
            session["user"] = uname
            role = users[uname]["role"]

            if role == "admin":
                return redirect("/admin")
            else:
                return redirect("/customer")

        return "Login gagal!"

    return render_template("login_page.html")


# -------- ADMIN PAGE ----------
@app.route("/admin")
def admin():
    if "user" not in session:
        return redirect("/login")
    if users[session["user"]]["role"] != "admin":
        return "Akses Ditolak"

    return render_template("admin_page.html", data=order_status)


# -------- CUSTOMER PAGE ----------
@app.route("/customer", methods=["GET", "POST"])
def customer():
    if "user" not in session:
        return redirect("/login")
    if users[session["user"]]["role"] != "customer":
        return "Akses Ditolak"

    if request.method == "POST":
        order_status["table"] = request.form["table"]
        order_status["payment_method"] = request.form["payment"]
        order_status["order"] = request.form.getlist("menu")
        order_status["payment_status"] = "Menunggu Pembayaran"

    return render_template(
        "customer_page.html",
        pricelist=pricelist,
        status=order_status
    )


# -------- LOGOUT ----------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


# -------- RUN SERVER ----------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
# ORDER SELECTED
frame_order = tk.LabelFrame(root, text="Order Dipilih")
frame_order.pack(fill="x", padx=10, pady=5)

for item in order:
    tk.Label(frame_order, text=f"- {item}").pack(anchor="w")

# STATUS PEMBAYARAN
frame_payment = tk.LabelFrame(root, text="Status Pembayaran")
frame_payment.pack(fill="x", padx=10, pady=5)

tk.Label(frame_payment, text=payment_status, fg="red").pack(anchor="w")

# ORDER PROCESS
frame_process = tk.LabelFrame(root, text="Order Process")
frame_process.pack(fill="x", padx=10, pady=5)

tk.Label(frame_process, text="Order in Process").pack(anchor="w")

# TOTAL BILL
frame_bill = tk.LabelFrame(root, text="Bill")
frame_bill.pack(fill="x", padx=10, pady=5)

total_bill = calculate_total()
tk.Label(frame_bill, text=f"Total: Rp {total_bill}", font=("Arial", 14, "bold")).pack(anchor="w")

root.mainloop()