from flask import Flask, jsonify
import numpy as np

app = Flask(__name__)

# Assume two matrices
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])


@app.route("/")
def home():
    print("Port Forwarding Tutorial ...")
    return jsonify({
        "message": "Linear Algebra using Flask + NumPy (Docker Learning) \
            port forwarding tutorial",
        "matrix_A": A.tolist(),
        "matrix_B": B.tolist(),
        "routes": [
            "/add",
            "/subtract",
            "/multiply",
            "/transpose",
            "/determinant",
            "/inverse"
        ]
    })


@app.route("/add")
def add():
    result = A + B
    return jsonify(result.tolist())


@app.route("/subtract")
def subtract():
    result = A - B
    return jsonify(result.tolist())


@app.route("/multiply")
def multiply():
    result = np.matmul(A, B)
    return jsonify(result.tolist())


@app.route("/transpose")
def transpose():
    result = A.T
    return jsonify(result.tolist())


@app.route("/determinant")
def determinant():
    result = np.linalg.det(A)
    return jsonify({"determinant": result})


@app.route("/inverse")
def inverse():
    result = np.linalg.inv(A)
    return jsonify(result.tolist())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
