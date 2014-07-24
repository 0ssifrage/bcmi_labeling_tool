import json
import os
from flask import Flask, render_template, Response, abort, g
from sqlite3 import dbapi2 as sqlite3
import config


app = Flask(__name__)
app.config.update(
    DATABASE=os.path.join(app.root_path, 'blt.db'),
    DEBUG=True
)


def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/')
def index():
    return render_template('index.html', page_id=1)


@app.route('/labeling/<page_num>')
def labeling(page_num):
    NUM_PER_PAGE = 50

    page_num = int(page_num)
    imgs = os.listdir(config.image_folder)
    pimgs = imgs[(page_num - 1) * NUM_PER_PAGE: page_num * NUM_PER_PAGE]
    return render_template(
        'labeling.html', page_id=2, attrs=config.attributes, imgs=pimgs
    )


@app.route('/result')
def result():
    imgs = os.listdir(config.image_folder)
    return render_template(
        'result.html', page_id=3, attrs=config.attributes, imgs=imgs
    )


@app.route('/image/<img_name>')
def image(img_name):
    img_path = os.path.join(config.image_folder, img_name)
    print img_path
    if os.path.exists(img_path):
        ext = img_name.split(".")[-1]
        c_type = {
            "bmp": "image/bmp",
            "png": "image/png",
            "jpg": "image/jpeg",
            "jpeg": "image/jpeg",
            "gif": "image/gif",
            "ico": "image/x-icon"
        }
        img = open(img_path, "rb").read()
        return Response(img, mimetype=c_type[ext])
    else:
        abort(404)


if __name__ == '__main__':
    app.run()
