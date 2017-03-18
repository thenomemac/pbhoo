import os

from flask import Flask, redirect, render_template, request, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from werkzeug.utils import secure_filename


# Flask extensions
bootstrap = Bootstrap()


app = Flask(__name__)


# Initialize flask extensions
bootstrap.init_app(app)


# env vars for tmp purposes
class Config(object):
    # DEBUG = False
    # TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY',
                                'superSecretDoNotUseOnOpenWeb')


# init config
app.config.from_object(Config)


def get_kits():
    kits = [{'display_name': 'kit_1', 'id': 1},
            {'display_name': 'kit_2', 'id': 2},
            {'display_name': 'kit_3', 'id': 3}]

    return kits


def get_kit_by_display_name(display_name):
    kits = get_kits()
    kit = next(kit for kit in kits if kit['display_name'] == display_name)

    return kit


class PhotoForm(FlaskForm):
    photo = FileField('photo', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')
    ])


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/choose_test_kit')
def choose_test_kit():
    kits = get_kits()
    return render_template('choose_test_kit.html', kits=kits)


@app.route('/need_test_kit')
def need_test_kit():
    return render_template('need_test_kit.html')


@app.route('/kit_instructions/<string:display_name>')
def kit_instructions(display_name):
    kit = get_kit_by_display_name(display_name)
    return render_template('kit_instructions.html', kit=kit)


@app.route('/kit_results/<string:display_name>', methods=['GET', 'POST'])
def kit_results(display_name):
    photo_form = PhotoForm()

    if request.method == 'POST':
        if photo_form.validate_on_submit():
            file = photo_form.photo.data
            filename = secure_filename(file.filename)
            # TODO: path should be updated before production
            file_path = os.path.join('data',
                                     'result_photos',
                                     filename)
            print(file_path)
            file.save(file_path)
            return redirect(url_for('index'))

    kit = get_kit_by_display_name(display_name)
    return render_template('kit_results.html', kit=kit, form=photo_form)
