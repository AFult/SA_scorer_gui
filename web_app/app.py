import os
from flask import Flask, render_template, request, redirect, url_for, session
from flask.ext.session import Session
from werkzeug.utils import secure_filename
import cPickle as pickle
import pandas as pd
from score_code import sa
import tempfile
import os
import json

ALLOWED_EXTENSIONS = set(['xlsx', 'xlsm', 'xlt'])

app = Flask(__name__)
sess = Session()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def build_scored_df(filename):
    df = pd.read_excel(filename, index_col = 0, header = 0)
    if df['pre_weight'].empty == False and \
       df['post_weight'].empty == False:
        weight_percentage = df['post_weight'] / df['pre_weight']
        weight_percentage.name = 'weight_percentage'

    scored = sa(df)

    scored = pd.concat([df['group'], weight_percentage, scored], axis=1)
    scored = scored.dropna(how = 'any', axis = 0)
    return scored

@app.route('/', methods=['GET','POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            print 'file not in request.files'
            print request.files
            return redirect(request.url)
        f = request.files['file']
        if f.filename == '':
            print 'no selected file'
            return redirect(request.url)
        if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)
            print 'saving file'
            UPLOAD_FOLDER = tempfile.mkdtemp()
            session['UPLOAD_FOLDER'] = UPLOAD_FOLDER
            session['filename'] = filename
            f.save(os.path.join(UPLOAD_FOLDER, filename))
            return redirect(url_for('results'))
    return render_template('home.html')

@app.route('/results', methods=['GET'])
def results():
    UPLOAD_FOLDER = session.get('UPLOAD_FOLDER')
    name = session.get('filename')
    scored_df = build_scored_df(UPLOAD_FOLDER + '/' + name)
    for f in os.listdir(UPLOAD_FOLDER):
        os.remove(UPLOAD_FOLDER + '/' + f)
    return render_template('results.html', name=name,
                           f = scored_df.to_html())



if __name__ == '__main__':
    app.secret_key = 'secretest of keys'
    app.config['SESSION_TYPE'] = 'filesystem'

    sess.init_app(app)

    app.run(host='0.0.0.0', debug=True)


# ================================================================
# ================================================================

# from flask import Flask, make_response, request
#
# app = Flask(__name__)
#
# def transform(text_file_contents):
#     return text_file_contents.replace("=", ",")
#
#
# @app.route('/')
# def form():
#     return """
#         <html>
#             <body>
#                 <h1>Transform a file demo</h1>
#
#                 <form action="/transform" method="post" enctype="multipart/form-data">
#                     <input type="file" name="data_file" />
#                     <input type="submit" />
#                 </form>
#             </body>
#         </html>
#     """
#
# @app.route('/transform', methods=["POST"])
# def transform_view():
#     file = request.files['data_file']
#     if not file:
#         return "No file"
#
#     file_contents = file.stream.read().decode("utf-8")
#
#     result = transform(file_contents)
#
#     response = make_response(result)
#     response.headers["Content-Disposition"] = "attachment; filename=result.csv"
#     return response
#
# if __name__ == '__main__':
#      app.run(host='0.0.0.0', port = 8080, debug=True)

# =========================================================
# =========================================================

# import os
# from flask import Flask, request, redirect, url_for
# from werkzeug.utils import secure_filename
#
# UPLOAD_FOLDER = 'file_uploads'
# ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
#
# app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#
# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
#
# @app.route('/', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         # check if the post request has the file part
#         if 'file' not in request.files:
#             flash('No file part')
#             return redirect(request.url)
#         file = request.files['file']
#         # if user does not select file, browser also
#         # submit a empty part without filename
#         if file.filename == '':
#             flash('No selected file')
#             return redirect(request.url)
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             return redirect(url_for('uploaded_file',
#                                     filename=filename))
#     return '''
#     <!doctype html>
#     <title>Upload new File</title>
#     <h1>Upload new File</h1>
#     <form action="" method=post enctype=multipart/form-data>
#       <p><input type=file name=file>
#          <input type=submit value=Upload>
#     </form>
#     '''
#
# if __name__ == '__main__':
#      app.run(host='0.0.0.0', port = 8080, debug=True)
