from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def calculation():
    result = 0
    error = ''
    # you may want to customize your GET... in this case not applicable
    if request.method=='POST':
        # get the form data
        first = request.form['first']
        second = request.form['second']
        if first and second:
            try:
                # do your validation or logic here...
                if int(first)>10 or int(first)<1:
                    raise ValueError
                result = int(first) + int(second)
            except ValueError:
                # you may pass custom error message as you like
                error = 'Please input integer from 1-10 only.'
    # you render the template and pass the context result & error
    return render_template('calculation.html', result=result, error=error)

if __name__ == "__main__":
    app.run(debug=True)

# def index():
#     return '<dd><input type=submit value=Load images>'
#
# https://stormpath.com/blog/build-a-flask-app-in-30-minutes
# http://hplgit.github.io/web4sciapps/doc/pub/._web4sa_flask017.html#___sec64
# https://realpython.com/blog/python/flask-by-example-updating-the-ui/
# http://hplgit.github.io/parampool/doc/pub/._pp003.html