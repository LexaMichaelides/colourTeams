import os
import pandas as pd
import sortleadersandstudents as algo

from flask import Flask, render_template, request, redirect, flash, send_file
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
results_path = os.path.join(app.root_path, 'results', 'sorted_output.csv')


def get_data(leader_file_path, student_file_path):

    while True:
        try:
            leader_data = algo.create_leader_groups(leader_file_path)
        except:
            continue
        break

    student_data = algo.create_student_groups(student_file_path)

    combined_data = pd.merge(leader_data, student_data, how='outer', on=['id', 'last_name', 'first_name', 'program', 'gender', 'email', 'watIam', 'group'])

    combined_data.to_csv(results_path, index = False)


@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':

        if 'student_data' not in request.files or 'leader_data' not in request.files:
            flash('No file part')
            return render_template('upload.html')

        student_file = request.files['student_data']
        leader_file = request.files['leader_data']

        if student_file.filename == '' or leader_file.filename == '' :
            flash('No Selected File')
            return render_template('upload.html')

        else:

            get_data(leader_file, student_file)
            return redirect('/download')

    return render_template('upload.html')


@app.route('/download', methods=['GET', 'POST'])
def download():
    if request.method == 'POST':
        return send_file(results_path)

    return render_template('download.html')


if __name__ == '__main__':
    app.run(debug=False)