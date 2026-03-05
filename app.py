from flask import Flask, render_template, request, send_file
from rembg import remove
from PIL import Image
import os
from io import BytesIO

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["image"]
        input_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(input_path)

        # Process image
        input_image = Image.open(input_path)
        output_image = remove(input_image)
        
        # Save output to bytes in memory instead of disk
        output_bytes = BytesIO()
        output_image.save(output_bytes, format="PNG")
        output_bytes.seek(0)
        
        # Delete input file
        os.remove(input_path)
        
        # Send file as download
        return send_file(
            output_bytes,
            mimetype="image/png",
            as_attachment=True,
            download_name="output.png"
        )

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
