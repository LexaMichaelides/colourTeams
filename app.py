import os
import sortleaders as leaderAlgo
import sortstudents as studentAlgo
import createsummaries as summary
from datetime import datetime
from flask import Flask, render_template, request, redirect, flash, send_file, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
results_path = os.path.join(app.root_path, 'results', 'sorted_output.csv')
result_summary_path = os.path.join(app.root_path, 'results', 'summary_output.csv')

@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'student_data' not in request.files and 'sorted_leader_data_to_summary' not in request.files and 'leader_data' not in request.files and 'sorted_leader_data' not in request.files:
            flash('No Files Selected')
            return render_template('upload.html')
            
        elif 'leader_data' in request.files:
            leader_file = request.files['leader_data']

            if leader_file.filename == '':
                flash('No Leader Data file uploaded')
                return render_template('upload.html')

            else:
                while True:
                    try:
                        leaderdf = leaderAlgo.create_leader_groups(leader_file, int(request.form['team_numbers']), int(request.form['SEteam_numbers']))
                        leaderdf.to_csv(results_path, index = False)
                        resultSummary = summary.initial_leader_summary(leaderdf)
                        resultSummary.to_csv(result_summary_path, index = False)
                        return redirect('/leader_download')
                    except:
                        continue
                    break
        
        elif 'sorted_leader_data_to_summary' in request.files:
            sorted_leader_data_to_summary = request.files['sorted_leader_data_to_summary']
            
            if sorted_leader_data_to_summary.filename == '':
                flash('No Leader Data file uploaded')
                return render_template('upload.html')
            else:
                leader_summary = summary.create_leader_summary(sorted_leader_data_to_summary)
                leader_summary.to_csv(result_summary_path, index = False)
                return redirect('/leader_summary_download')
        
        elif 'student_data' in request.files or 'leader_data' in request.files:
            student_file = request.files['student_data']
            sorted_leader_file = request.files['sorted_leader_data']

            if student_file.filename == '' and sorted_leader_file.filename == '':
                flash('No First Year Data and Leader Data files uploaded')
                return render_template('upload.html')
            
            if student_file.filename == '':
                flash('No First Year Data file uploaded')
                return render_template('upload.html')

            if sorted_leader_file.filename == ''  :
                flash('No Leader Data file uploaded')
                return render_template('upload.html')
            
            else:
                result = studentAlgo.create_first_year_groups(student_file, sorted_leader_file)
                result.to_csv(results_path, index = False)
                resultSummary = summary.create_first_year_summary(result)
                resultSummary.to_csv(result_summary_path, index = False)
                return redirect('/first_year_download') 

    return render_template('upload.html')

@app.route('/leader_download', methods=['GET', 'POST'])
def leader_download():
    if request.method == 'POST':
        if request.form['download_button'] == 'back':
            return redirect('/')
        if request.form['download_button'] == 'result':
            result_file_name = 'sorted_leader_data_' + datetime.utcnow().strftime("%Y%m%d-%H%M%S") + '.csv'
            return send_file(results_path, mimetype='text/csv', attachment_filename=result_file_name, as_attachment=True)
        elif request.form['download_button'] == 'summary':
            summary_file_name = 'leader_summary_' + datetime.utcnow().strftime("%Y%m%d-%H%M%S") + '.csv'
            return send_file(result_summary_path, mimetype='text/csv', attachment_filename=summary_file_name, as_attachment=True)

    return render_template('download.html')

@app.route('/first_year_download', methods=['GET', 'POST'])
def first_year_download():
    if request.method == 'POST':
        if request.form['download_button'] == 'back':
            return redirect('/')
        if request.form['download_button'] == 'result':
            result_file_name = 'sorted_first_year_data_' + datetime.utcnow().strftime("%Y%m%d-%H%M%S") + '.csv'
            return send_file(results_path, mimetype='text/csv', attachment_filename=result_file_name, as_attachment=True)
        elif request.form['download_button'] == 'summary':
            summary_file_name = 'first_year_summary_' + datetime.utcnow().strftime("%Y%m%d-%H%M%S") + '.csv'
            return send_file(result_summary_path, mimetype='text/csv', attachment_filename=summary_file_name, as_attachment=True)

    return render_template('download.html')

@app.route('/leader_summary_download', methods=['GET', 'POST'])
def leader_summary_download():
    if request.method == 'POST':
        if request.form['download_button'] == 'back':
            return redirect('/')
        if request.form['download_button'] == 'summary':
            summary_file_name = 'updated_leader_summary_' + datetime.utcnow().strftime("%Y%m%d-%H%M%S") + '.csv'
            return send_file(result_summary_path, mimetype='text/csv', attachment_filename=summary_file_name, as_attachment=True)

    return render_template('leader_summary_download.html')

if __name__ == '__main__':
    app.run(debug=False)