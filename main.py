from flask import Flask, request, render_template, redirect, url_for, flash
import matplotlib.pyplot as plt
import numpy as np
import os
from flask_bootstrap import Bootstrap5
from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField, TimeField, SelectField, BooleanField, IntegerField, FloatField

app = Flask(__name__)
bs = Bootstrap5(app)
app.config["SECRET_KEY"] = "secret-key"

upload_folder_path = "static/uploads/"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = upload_folder_path


class ImageForm(FlaskForm):
    file = StringField("File Path")
    submit = SubmitField("Submit")


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def rgb_to_hex(rgb=None):
    if rgb:
        r, g, b = (int(channel * 255) for channel in rgb[:3])
        hex_color = f'#{r:02x}{g:02x}{b:02x}'
        return hex_color


def get_hex_order(img):
    reshaped_img = img.reshape(-1, img.shape[-1])
    unique_values, counts = np.unique(reshaped_img, axis=0, return_counts=True)

    all_values = []
    all_counts = []
    for value, count in zip(unique_values, counts):
        new_value = (float(value[0]), float(value[1]), float(value[2]))
        all_values.append(new_value)
        all_counts.append(int(count))

    old_values = {}
    for idx, num in enumerate(all_counts):
        old_values[idx] = num

    all_counts.sort()

    for i in range(len(all_counts)):
        for key, value in old_values.items():
            if all_counts[i] == value:
                old_values[key] = i

    sorted_colors = ["" for count in range(len(all_counts))]

    for color_val in all_values:
        for key, value in old_values.items():
            if all_values.index(color_val) == key:
                sorted_colors[value] = color_val

    sorted_colors.reverse()
    return sorted_colors[0:10]


@app.route("/", methods=["GET", "POST"])
def home_page():
    form = ImageForm()
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            img_path = upload_folder_path + filename
            img = plt.imread(img_path)
            sorted_hex = get_hex_order(img=img)
            hex_codes = [rgb_to_hex(rgb) for rgb in sorted_hex]
            return redirect(url_for('hex_result', img_path=img_path, hex_codes=hex_codes))
    return render_template('index.html', form=form)


@app.route("/hex-results", methods=["GET", "POST"])
def hex_result():
    img_path = request.args.get("img_path")
    hex_codes = request.args.getlist('hex_codes')
    return render_template("hex_page.html", img_path=img_path, hex_codes=hex_codes)


if __name__ == "__main__":
    app.run(debug=True)
