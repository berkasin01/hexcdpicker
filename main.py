from flask import Flask, request, render_template, redirect, url_for, flash
import matplotlib.pyplot as plt
import numpy as np
import os
from flask_bootstrap import Bootstrap5
from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField, TimeField, SelectField, BooleanField, IntegerField, FloatField
from wtforms.validators import DataRequired
import sqlite3
from wtforms.validators import DataRequired, Length
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
bs = Bootstrap5(app)
app.config["SECRET_KEY"] = "secret-key"

upload_folder_path = "static/"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = upload_folder_path

class ImageForm(FlaskForm):
    file = StringField("File Path")
    submit = SubmitField("Submit")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def home_page():
    form = ImageForm()
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('download_file', name=filename))
    return render_template('index.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)


# img = plt.imread("static/McDonalds-Logo-1993.png")
# reshaped_img = img.reshape(-1, img.shape[-1])
# unique_values, counts = np.unique(reshaped_img, axis=0, return_counts=True)
#
# for value, count in zip(unique_values, counts):
#     print(f"Value: {value}, Count: {count}")
#
#
# def rgba_to_hex(rgb):
#     r, g, b = (int(channel * 255) for channel in rgb[:3])
#
#     hex_color = f'#{r:02x}{g:02x}{b:02x}'
#
#     return hex_color
#
#
# color = (0.9843137, 0.69803923, 0.04313726)
#
# print(rgba_to_hex(color))
