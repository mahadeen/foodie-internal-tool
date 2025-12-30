from flask import Flask, render_template, request
from pathlib import Path
import order_analysis
import visualize

app = Flask(__name__)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        
        file = request.files.get("file")

        if not file or not file.filename.endswith(".json"):
            return "Invalid file", 400

        input_path = UPLOAD_DIR / "orders.json"
        file.save(input_path)

        # run analysis
        order_analysis.run_analysis(input_path)

        # generate charts
        visualize.generate_charts()

        return render_template("index.html", show_results=True)

    return render_template("index.html", show_results=False)

if __name__ == "__main__":
    app.run(debug=True)