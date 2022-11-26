from flask import Flask, render_template
from generator import activity_finder, time_generator

app = Flask(__name__) # holds the name of the current Python module


@app.route('/') 
    # This function fires when someone hits Base ("/") url
    # You pass the value '/' to @app.route() to signify that this function will respond to web requests for the URL /, which is the main URL.
def hello():
    return render_template('index.html')

@app.route('/yado') 
def hello2():
    activity= activity_finder()
    time = time_generator()
    return render_template('generated_activity.html', activity=activity, time=time)

if __name__ == '__main__':
   app.run()