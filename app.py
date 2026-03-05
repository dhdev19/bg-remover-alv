from flask import Flask, render_template, request
from rembg import remove
from PIL import Image
import os

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["image"]
        input_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(input_path)

        output_path = os.path.join(app.config["UPLOAD_FOLDER"], "output.png")

        input_image = Image.open(input_path)
        output_image = remove(input_image)
        output_image.save(output_path)

        return render_template("index.html", output_image=output_path)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
