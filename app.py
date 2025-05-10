from flask import Flask, render_template, request
import markdown
from main import conversar

app = Flask(__name__)

@app.route("/", methods = ["GET", "POST"])
def index():
    resposta = ''
    if request.method == "POST":
        user_input = request.form["user_input"]
        resposta = conversar(user_input)

    resposta = markdown.markdown(resposta)
    return render_template("index.html", resposta=resposta)

if __name__ == "__main__":
    app.run(debug=True)