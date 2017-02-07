import os
import numpy as np
import json
import pydotplus

import plotly.graph_objs as go
from plotly.offline import plot

from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

from imblearn.over_sampling import SMOTE
from scipy import stats
from flask import Flask, render_template, Markup, jsonify, request, redirect, flash, url_for
from werkzeug.utils import secure_filename

# from plotly.tools import FigureFactory as FF

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join( app.root_path, 'uploadedFiles' )
ALLOWED_EXTENSIONS = set(['txt'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Set session secret key
app.secret_key = 'some_secret'

classifier = None

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash( 'No file part' )
            return redirect( request.url )
        file = request.files[ 'file' ]
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect( request.url )
        if file and allowed_file( file.filename ) :
            filename = secure_filename( file.filename )
            file.save( os.path.join( app.config[ 'UPLOAD_FOLDER' ], filename ) )
            flash( 'File uploaded!' )
            return redirect( url_for( 'index', filename = filename ) )
    return


@app.route('/_predict')
def _predict() :
    inputdata = np.loadtxt( os.path.join( app.config[ 'UPLOAD_FOLDER' ], request.args[ 'filename' ] ) )

    global classifier

    Predicted_Crop = classifier.predict(inputdata).tolist()

    dictionary = { 1: 'Corn', 0: 'Not corn' }
    res = map( lambda flag: dictionary[ flag ] + ' ', Predicted_Crop )

    return jsonify( result = res )


@app.route('/_buildModel')
def _buildModel() :
    res = classify()
    global classifier
    classifier = res[0]
    return jsonify( score = res[1] )

def classify() :
    workingFolder = os.path.expanduser('~/fellowship_crops-master')
    os.chdir(workingFolder)

    data = np.load('grand_matrix.npy')
    col_headers = np.load('col_headers.npy')

    DATA = data[:, 3:]
    Crop = data[:, 1]

    Corn_ind = np.nonzero(Crop == 4)[0]
    DATA_for_corn = np.zeros(len(Crop))
    DATA_for_corn[Corn_ind] = 1

    msk = np.random.rand(len(Crop)) < 0.8
    trainDATA = DATA[msk, :]
    testDATA = DATA[~msk, :]
    trainCrop = DATA_for_corn[msk]
    testCrop = DATA_for_corn[~msk]

    # clf = skl.tree.DecisionTreeClassifier()
    clf = RandomForestClassifier( n_estimators = 100 )
    clf = clf.fit(trainDATA, trainCrop)
    predict_data = clf.predict(testDATA)

    dot_data = tree.export_graphviz(clf.estimators_[0], out_file=os.path.join(app.root_path, 'temp/Clf.dot'),
                                    feature_names=col_headers[3:],
                                    class_names=np.asarray(['corn', 'not corn']),
                                    filled=True, rounded=True,
                                    special_characters=True)

    graph = pydotplus.graph_from_dot_file( os.path.join( app.root_path, 'temp/Clf.dot' ) )
    pathToWrite = os.path.join(app.root_path, 'static/Clf.png')
    graph.write_png(pathToWrite)

    return clf, accuracy_score( testCrop, predict_data )


@app.route('/_getKSDist')
def _getKSDist( ) :
    # inpt = json.loads( request.args.get( 'inpt' ) )
    # do some stuff
    # inpt = jsonify( result = inpt )

    res = getKSDist()
    x = res[0]
    y = res[1]
    z = res[2]

    surface = go.Surface(x=x, y=y, z=z)
    data = go.Data([surface])
    layout = go.Layout(
        scene=go.Scene(
            xaxis=dict(range=[100, 350]),
            yaxis=dict(range=[-0.2, 0.2])
        ),
        title='Probability Density of Vegetative Index vs. Day of the Year'
    )
    fig = go.Figure(data=data, layout=layout)

    KSDist = plot(
        fig
        , output_type='div'
        , include_plotlyjs=False
        , show_link=False
    )
    KSDist = Markup( KSDist )

    return jsonify( result = KSDist )


def getKSDist( ) :
    # figure KS distributions
    workingFolder = os.path.expanduser('~/fellowship_crops-master')
    os.chdir(workingFolder)

    data = np.load('grand_matrix.npy')
    # channels = np.load('channels.npy')
    # col_headers = np.load('col_headers.npy')
    # crop_dict = np.load('crop_dict.npy')

    Corn_ind = np.nonzero(data == 4)[0]
    data_corn = data[Corn_ind, :]

    X = data_corn[:, 3]
    Y = data_corn[:, 0]
    Z = data_corn[:, 15]

    z1 = X  # time
    z2 = Z  # vegetative index

    pdfxi = stats.gaussian_kde(z1)
    xi = np.linspace(z1.min(), z1.max(), 100)
    px = pdfxi(xi)

    pdfyi = stats.gaussian_kde(z2)
    yi = np.linspace(z2.min(), z2.max(), 100)
    py = pdfyi(yi)

    xii, yii = np.meshgrid(xi, yi)
    pdfxii, pdfyii = np.meshgrid(px, py)

    pdfxyi = pdfxii * pdfyii

    m1 = np.meshgrid(xi, yi, pdfxyi)
    return xii, yii, pdfxyi


@app.route( "/", methods = [ 'GET', 'POST' ] )
def index():
    fn = ''
    if request.args and request.args[ 'filename' ] :
        fn = request.args[ 'filename' ]

    return render_template( 'index.html'
                            , uploaded = fn
                            )


if __name__ == "__main__" :
    app.run( debug = True, use_reloader = True )
    #app.run( host = '0.0.0.0', port = 9999 )

# https://stormpath.com/blog/build-a-flask-app-in-30-minutes
# http://hplgit.github.io/web4sciapps/doc/pub/._web4sa_flask017.html#___sec64
# https://realpython.com/blog/python/flask-by-example-updating-the-ui/
# http://hplgit.github.io/parampool/doc/pub/._pp003.html
# https://codepen.io/plotly/pres/wKpPvj
