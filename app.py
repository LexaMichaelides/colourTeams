import os
import sortleadersandstudents as algo
import createsummaries as summary
from flask import Flask, render_template, request, redirect, flash, send_file, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
results_path = os.path.join(app.root_path, 'results', 'sorted_output.csv')
result_summary_path = os.path.join(app.root_path, 'results', 'summary_output.csv')

@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':

        if 'student_data' not in request.files and 'leader_data' not in request.files and 'sorted_leader_data' not in request.files:
            flash('No file part')
            return render_template('upload.html')

        elif 'leader_data' in request.files:
            leader_file = request.files['leader_data']

            if leader_file.filename == '':
                flash('No Selected File')
                return render_template('upload.html')

            else:
                while True:
                    try:
                        result = algo.create_leader_groups(leader_file)
                        result.to_csv(results_path, index = False)
                        resultSummary = summary.create_leader_summary(result)
                        resultSummary.to_csv(result_summary_path, index = False)
                        return redirect('/download')
                    except:
                        continue
                    break

        elif 'student_data' in request.files and 'sorted_leader_data' in request.files:
            student_file = request.files['student_data']
            sorted_leader_file = request.files['sorted_leader_data']

            if student_file.filename == '' and leader_file.filename == '' and sorted_leader_file.filename == ''  :
                flash('No Selected File')
                return render_template('upload.html')

            else:
                result = algo.create_first_year_groups(student_file, sorted_leader_file)
                result.to_csv(results_path, index = False)
                resultSummary = summary.create_first_year_summary(result)
                resultSummary.to_csv(result_summary_path, index = False)
                return redirect('/download') 

    return render_template('upload.html')

@app.route('/download', methods=['GET', 'POST'])
def download():
    if request.method == 'POST':
        if request.form['download_button'] == 'result':
             return send_file(results_path)
        elif request.form['download_button'] == 'summary':
             return send_file(result_summary_path)

    return render_template('download.html')

if __name__ == '__main__':
    app.run(debug=False)