from flask import Flask, request, render_template, redirect

app = Flask(__name__)

@app.get("/")
def index():
    """
    TODO: Render the home page provided under templates/index.html in the repository
    """
    return render_template("index.html")

@app.route("/search",methods=["GET","POST"])
def search():
    args = request.form["q"]
    if 'second' in request.form:
        return redirect (f"https://google.com/search?q={args}&btnI=1")
    return redirect(f"https://google.com/search?q= {args} ")

if __name__ == "__main__":
    app.run()