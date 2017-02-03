from flask import Flask, render_template, Markup, request

import json
import plotly
from plotly.offline import plot
import plotly.graph_objs as go

import pandas as pd
import numpy as np

app = Flask(__name__)
app.debug = True

@app.route("/", methods=['GET', 'POST'])
def index():
    x, y = np.mgrid[-2 * np.pi:2 * np.pi:300j, -2:2:300j]

    # x = np.linspace(0, 10, 10)
    # y = np.linspace(0, 10, 10)
    # xGrid, yGrid = np.meshgrid(x, y)
    # userinput1 = 1  # Want user to input these variables
    # userinput2 = 2
    # userinput3 = 3
    # zGrid = lambda x1, y1: (x1 ** userinput1 + y1 ** userinput2) + userinput3 ** userinput3
    # surface = go.Surface(x=xGrid, y=yGrid, z=zGrid(xGrid, yGrid))
    # data = go.Data([surface])
    # fig = go.Figure(data=data)

    div_test = plot(
        # fig,
        {
            "data": [
                go.Surface(
                    x=x,
                    y=y,
                    z=-np.cos(x)+y**2/2
                )
            ],#go.Scatter(x=[1, 2, 3], y=[3, 1, 6])],
            "layout": go.Layout( title = 'Hello World' ) # Surface, Scene
        },
        output_type = 'div',
        include_plotlyjs = False,
        show_link = False
        # ,image_height = 400
        # ,image_width = 400
    )

    # result = 0
    # error = ''
    # # you may want to customize your GET... in this case not applicable
    # if request.method=='POST':
    #     # get the form data
    #     first = request.form['first']
    #     second = request.form['second']
    #     if first and second:
    #         try:
    #             # do your validation or logic here...
    #             if int(first)>10 or int(first)<1:
    #                 raise ValueError
    #             result = int(first) + int(second)
    #         except ValueError:
    #             # you may pass custom error message as you like
    #             error = 'Please input integer from 1-10 only.'
    # # you render the template and pass the context result & error

    rng = pd.date_range('1/1/2011', periods=7500, freq='H')
    ts = pd.Series(np.random.randn(len(rng)), index=rng)

    graphs = [
        dict(
            data=[
                dict(
                    x=[1, 3, 5],
                    y=[10, 50, 30],
                    type='bar'
                ),
            ],
            layout=dict(
                title='second graph'
            )
        ),
        dict(
            data=[
                dict(
                    x=ts.index,  # Can use the pandas data structures directly
                    y=ts
                )
            ]
        )
        # ,dict(
        #     data=[
        #         dict(
        #             x=[1, 2, 3],
        #             y=[10, 20, 30],
        #             type='scatter'
        #         ),
        #     ],
        #     layout=dict(
        #         title='first graph'
        #     )
        # )
    ]

    # Add "ids" to each of the graphs to pass up to the client
    # for templating
    ids = ['Tab{}Content'.format(i) for i, _ in enumerate(graphs)]

    # Convert the figures to JSON
    # PlotlyJSONEncoder appropriately converts pandas, datetime, etc
    # objects to their JSON equivalents
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)
    print( ids )

    return render_template('index.html',
                           ids = ids,
                           graphJSON = graphJSON,
                           div_test = Markup( div_test )
                           )


if __name__ == "__main__":
    app.run(debug=True)
    #app.run(host='0.0.0.0', port=9999)

# def index():
#     return '<dd><input type=submit value=Load images>'
#
# https://stormpath.com/blog/build-a-flask-app-in-30-minutes
# http://hplgit.github.io/web4sciapps/doc/pub/._web4sa_flask017.html#___sec64
# https://realpython.com/blog/python/flask-by-example-updating-the-ui/
# http://hplgit.github.io/parampool/doc/pub/._pp003.html
# https://codepen.io/plotly/pres/wKpPvj
# http://stackoverflow.com/questions/40595002/plotly-js-responsive-graph-in-div
# https://plot.ly/javascript/responsive-fluid-layout/
