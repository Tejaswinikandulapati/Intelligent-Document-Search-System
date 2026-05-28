from flask import Flask, render_template, request
import os

app = Flask(__name__)

UPLOAD_FOLDER = "documents"

# Create documents folder
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route("/", methods=["GET", "POST"])

def home():

    results = []

    message = ""

    keyword = ""

    if request.method == "POST":

        # Upload File
        uploaded = request.files.get("file")

        if uploaded and uploaded.filename != "":

            filepath = os.path.join(
                UPLOAD_FOLDER,
                uploaded.filename
            )

            uploaded.save(filepath)

            message = (
                "File Uploaded Successfully"
            )

        # Search Keyword
        keyword = request.form.get(
            "keyword",
            ""
        ).lower()

        if keyword != "":

            files = os.listdir(
                UPLOAD_FOLDER
            )

            for file in files:

                # Only TXT files
                if file.endswith(".txt"):

                    path = os.path.join(
                        UPLOAD_FOLDER,
                        file
                    )

                    with open(
                        path,
                        "r"
                    ) as f:

                        content = f.read()

                        lower_content = (
                            content.lower()
                        )

                        # Keyword Search
                        if keyword in lower_content:

                            highlighted = (
                                content.replace(

                                keyword,

                                f"<mark>{keyword}</mark>"

                                )
                            )

                            highlighted = (
                                highlighted.replace(

                                keyword.capitalize(),

                                f"<mark>{keyword.capitalize()}</mark>"

                                )
                            )

                            results.append({

                                "name": file,

                                "content": highlighted

                            })

        # No Result
        if keyword != "" and len(results) == 0:

            message = (
                "No matching documents found"
            )

    return render_template(

        "index.html",

        results=results,

        message=message

    )

if __name__ == "__main__":

    app.run(debug=True)