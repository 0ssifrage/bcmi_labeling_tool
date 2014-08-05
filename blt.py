import json
import os
from flask import Flask, render_template, Response, abort, g, request
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
    max_page = (len(imgs) - 1) / NUM_PER_PAGE + 1
    pimgs = imgs[(page_num - 1) * NUM_PER_PAGE: page_num * NUM_PER_PAGE]
    attrs = config.attributes

    db = get_db()
    img_v = []
    for img in pimgs:
        d = {}
        for attr in attrs:
            d[attr['id']] = 0

        cur = db.execute(
            'select value from attributes where imgname="%s"' % img
        )
        t = cur.fetchall()
        if t:
            v = json.loads(t[0][0])
            for attr_id in v:
                d[int(attr_id)] = v[attr_id]
        img_v.append({"img": img, "v": d})

    return render_template(
        'labeling.html', page_id=2, attrs=attrs, imgs=img_v,
        page_num=page_num, max_page=max_page
    )


@app.route('/region/<page_num>')
def region(page_num):
    NUM_PER_PAGE = 50

    page_num = int(page_num)
    imgs = os.listdir(config.image_folder)
    max_page = (len(imgs) - 1) / NUM_PER_PAGE + 1
    pimgs = imgs[(page_num - 1) * NUM_PER_PAGE: page_num * NUM_PER_PAGE]
    regs = config.regions

    db = get_db()
    img_v = []
    for img in pimgs:
        d = {}
        for reg in regs:
            d[reg['id']] = [[0, 0], [0, 0]]

        cur = db.execute('select value from regions where imgname="%s"' % img)
        t = cur.fetchall()
        if t:
            v = json.loads(t[0][0])
            for reg_id in v:
                d[int(reg_id)] = v[reg_id]
        img_v.append({"img": img, "v": d})

    return render_template(
        'region.html', page_id=4, regs=regs, imgs=img_v,
        page_num=page_num, max_page=max_page
    )


@app.route('/update', methods=['POST'])
def update():
    img = request.form['img']
    attr_id = request.form['attr_id']
    v_id = int(request.form['v_id'])
    db = get_db()
    cur = db.execute('select value from attributes where imgname="%s"' % img)
    t = cur.fetchall()
    if not t:
        cur = db.execute(
            'insert into attributes (imgname, imgpath, value) values(?, ?, ?)',
            [img, os.path.join(config.image_folder, img),
                json.dumps({attr_id: v_id})]
        )
        db.commit()
    else:
        v = json.loads(t[0][0])
        if v_id == 0:
            if attr_id in v:
                del v[attr_id]
            else:
                return 'done'
        else:
            v[attr_id] = v_id

        cur = db.execute(
            "update attributes set imgpath='%s', value='%s'"
            "where imgname='%s'" % (
                os.path.join(config.image_folder, img), json.dumps(v), img
            )
        )
        db.commit()
    return 'done'


@app.route('/result/<page_num>')
def result(page_num):
    NUM_PER_PAGE = 100

    page_num = int(page_num)
    imgs = os.listdir(config.image_folder)
    max_page = (len(imgs) - 1) / NUM_PER_PAGE + 1
    pimgs = imgs[(page_num - 1) * NUM_PER_PAGE: page_num * NUM_PER_PAGE]
    attrs = config.attributes
    attr_id_v = {}
    attr_id_name = {}
    for attr in attrs:
        attr_id_name[attr['id']] = attr['name']
        attr_id_v[attr['id']] = attr['value']
    db = get_db()

    img_v = []
    for img in pimgs:
        d = {}
        for attr in attrs:
            d[attr['id']] = '-'

        cur = db.execute(
            'select value from attributes where imgname="%s"' % img
        )
        t = cur.fetchall()
        if t:
            v = json.loads(t[0][0])
            for attr_id in v:
                d[int(attr_id)] = attr_id_v[int(attr_id)][v[attr_id]-1]
        img_v.append({"img": img, "v": d})

    return render_template(
        'result.html', page_id=3, attrs=attr_id_name, imgs=img_v,
        page_num=page_num, max_page=max_page
    )


@app.route('/image/<img_name>')
def image(img_name):
    img_path = os.path.join(config.image_folder, img_name)
    # print img_path
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
    app.run(debug=False, host=config.host, port=config.port)
