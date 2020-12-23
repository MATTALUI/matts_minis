import uuid
import os
import shutil
from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    request
)

from models import (
    session,
    Mini,
    Color,
    ColorTypes,
    Image
)

app = Flask(__name__)

try:
    os.environ['FLASK_ENV']
    os.environ['FLASK_RUN_PORT']
except KeyError:
    raise Exception('\n\nYou seem to be missing required ENV variables.Be sure to run "source ./env.sh"')

# @app.before_request
# def check_session():
#     print('======================')
#     print('checking session')
#     print('======================')

def reset_mini_images(mini):
    # Get rid of old images
    for image in mini.images:
        session.delete(image)
    if os.environ['FLASK_ENV'] == 'development':
        target_dir = os.path.join(app.root_path, "static/minis/"+str(mini.id)+"/images")
        try:
            shutil.rmtree(target_dir) # could throw if new mini; doesn't have images saved yet
        except:
            pass # Who cares?
    else:
        pass # TODO: Use S3 for storage for-realsies
    # Save new ones
    for uploaded_image in request.files.getlist('images'):
        key=str(uuid.uuid4())
        image = Image(mini_id=mini.id, key=key)
        if os.environ['FLASK_ENV'] == 'development':
            target_dir = os.path.join(app.root_path, "static/minis/"+str(mini.id)+"/images")
            os.makedirs(target_dir, exist_ok=True)
            uploaded_image.save(os.path.join(target_dir, key+".jpg"))
        else:
            pass # TODO: Use S3 for storage for-realsies
        session.add(image)
    session.commit()
def reset_mini_colors(mini):
    mini.colors = []
    for color_id in request.form.getlist('colors'):
        color = Color.objects().get(color_id)
        mini.colors.append(color)
    session.add(mini)
    session.commit()


##############################################################################
# ROOT PATH
##############################################################################
@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('minis_index'))

##############################################################################
# MINIS ROUTES
##############################################################################
def mini_params():
    return {
        "date": request.form["date"],
        "figure_type": request.form["figure_type"],
        "nickname": request.form["nickname"],
        "description": request.form["description"],
        "retro": request.form["retro"]
    }
@app.route('/minis/', methods=['GET'])
def minis_index():
    return render_template('minis.html', minis=Mini.objects().all())
@app.route('/minis/', methods=['POST'])
def minis_create():
    mini = Mini(**mini_params())
    reset_mini_colors(mini)
    reset_mini_images(mini)
    return redirect(url_for('minis_show', mini_id=mini.id))
@app.route('/minis/new/', methods=['GET'])
def minis_new():
    return render_template(
        'mini_form.html',
        colors=Color.objects().all(),
        mini=Mini()
    )
@app.route('/minis/<int:mini_id>/', methods=['GET'])
def minis_show(mini_id=None):
    return render_template('mini.html', mini=Mini.objects().get(mini_id))
@app.route('/minis/<int:mini_id>/', methods=['POST'])
def minis_update(mini_id=None):
    mini = Mini.objects().get(mini_id)
    mini.update(**mini_params())
    session.add(mini)
    session.commit()
    reset_mini_colors(mini)
    print(len(request.form.getlist('images')))
    if len(request.form.getlist('images')):
        reset_mini_images(mini)
    return redirect(url_for('minis_show', mini_id=mini.id))
@app.route('/minis/<int:mini_id>/edit/', methods=['GET'])
def minis_edit(mini_id=None):
    return render_template(
        'mini_form.html',
        mini=Mini.objects().get(mini_id),
        colors=Color.objects().all(),
    )

##############################################################################
# COLORS ROUTES
##############################################################################
@app.route('/colors/', methods=['GET'])
def colors_index():
    colors = Color.objects().all()
    colors.sort(key=lambda c: c.display_name)
    color_groups = {}
    for color in colors:
        if color.brand in color_groups:
            color_groups[color.brand].append(color)
        else:
            color_groups[color.brand] = [color]
    return render_template('colors.html', colors=colors, color_groups=color_groups)
@app.route('/colors/', methods=['POST'])
def colors_create():
    session.add(Color(**request.form))
    session.commit()
    return redirect(url_for('colors_index'))
@app.route('/colors/new/', methods=['GET'])
def colors_new():
    return render_template('color_form.html', ColorTypes=ColorTypes, color=Color())
@app.route('/colors/<int:color_id>/', methods=['GET'])
def colors_show(color_id=None):
    return render_template('color.html', color=Color.objects().get(color_id))
@app.route('/colors/<int:color_id>/edit/', methods=['GET'])
def colors_edit(color_id=None):
    return render_template('color_form.html', ColorTypes=ColorTypes, color=Color.objects().get(color_id))

##############################################################################
# ERROR ROUTES
##############################################################################
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html')
