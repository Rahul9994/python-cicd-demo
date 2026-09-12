from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello World! Python CI/CD Pipeline is working perfectly!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
