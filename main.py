from flask import Flask, url_for, render_template, redirect, request
from getresult import result
import time
import json
import gensim.downloader as api
import gensim
import numpy as np
import pymorphy2
import zipfile
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'project'
CORS(app)


# text1 = 'сегодня в москве плохая погода'
# text2 = 'к вечеру в столице ожидается ураган'
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/result', methods=['POST'])
def testpath():
    f = dict(request.form, )
    text1, text2 = f['t1'], f['t2']
    return str(result(text1, text2))


if __name__ == '__main__':
    app.run(port=8080, host='192.168.31.102')
