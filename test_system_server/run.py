from flask import Flask, request, render_template
app=Flask(__name__)


@app.route("/")
def index():
    return render_template("/index.html", site_name='A_Appium System')


@app.route('/req_test')
def req_test():
    val = ''
    for key,value in request.args.items():
        val += " %s = %s <br>"%(key,value)
    return val


if __name__=='__main__':
    app.run(debug=True)
