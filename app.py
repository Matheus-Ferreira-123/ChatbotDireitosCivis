from flask import Flask, render_template, request, session, redirect, url_for
from pln_utils import conversar, GEMINI_API_KEY
import markdown
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route("/", methods=["GET", "POST"])
def chat():
    if "conversas" not in session:
        session["conversas"] = []
        session["conversas"].append({"tipo": "bot", "texto": "Olá, seja bem vindo! Eu sou um chatbot especializado em direitos civis brasileiros. Como eu poderia estar lhe ajudando?"})

    if request.method == "POST":
        user_input = request.form["user_input"]
        resposta = conversar(user_input)
        resposta = markdown.markdown(resposta)

        session["conversas"].append({"tipo": "usuario", "texto": user_input})
        session["conversas"].append({"tipo": "bot", "texto": resposta})
        session.modified = True
        return redirect(url_for('chat'))

    return render_template("index.html", conversas=session.get("conversas", []))

if __name__ == "__main__":
    app.run(debug=True)