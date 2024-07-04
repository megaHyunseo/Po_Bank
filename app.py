from flask import Flask, render_template, request, redirect, url_for, jsonify
from config import Config
from models import db, IDCard
from ocr import extract_text_from_image
import traceback

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

distance_value = 100  # 초기 거리 값

@app.route('/')
def index():
    return render_template('index.html', distance=distance_value)

@app.route('/upload')
def upload_page():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return redirect(url_for('index'))
    
    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('index'))
    
    try:
        name, registration_number = extract_text_from_image(file)
        if not update_database(name, registration_number):  # 주민등록번호 중복 확인
            return redirect(url_for('db_view', error="이미 있는 주민번호입니다."))
    except Exception as e:
        print("오류:", e)
        traceback.print_exc()
        return render_template('upload.html', error="업로드 중 오류가 발생했습니다. 다시 시도해주세요.")
    
    return redirect(url_for('db_view'))

@app.route('/sensor', methods=['POST'])
def sensor():
    global distance_value
    distance_value = request.json.get('distance')
    if distance_value <= 10:
        return jsonify({"redirect": url_for('upload_page')})
    return jsonify({"status": "ok"})

@app.route('/distance')
def distance():
    return jsonify(distance=distance_value)

@app.route('/db')
def db_view():
    ids = IDCard.query.all()
    error = request.args.get('error')
    return render_template('db_view.html', ids=ids, error=error)

@app.route('/delete_db', methods=['POST'])
def delete_db():
    db.drop_all()
    db.create_all()
    return redirect(url_for('upload_page'))

def update_database(name, registration_number):
    existing_entry = IDCard.query.filter_by(registration_number=registration_number).first()
    if existing_entry:
        return False
    new_entry = IDCard(name=name, registration_number=registration_number)
    db.session.add(new_entry)
    db.session.commit()
    return True

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', use_reloader=False)
