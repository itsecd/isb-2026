from flask import Flask, render_template, jsonify
import subprocess
import os
import sys

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def run_script(mode):
    try:
       
        result = subprocess.run(
            [sys.executable, os.path.join(BASE_DIR, 'main.py'), mode],
            capture_output=True, 
            text=True, 
            timeout=60,
            cwd=BASE_DIR,  
            env=os.environ.copy() 
        )
        # Печатаем в консоль сервера для отладки
        print(f"Режим {mode}")
        print(f"STDOUT: {result.stdout}")
        print(f"STDERR: {result.stderr}")
        return {
            'success': result.returncode == 0,
            'output': result.stdout,
            'error': result.stderr if result.stderr else None
        }
    except subprocess.TimeoutExpired:
        return {'success': False, 'output': '', 'error': 'Операция заняла слишком много времени'}
    except Exception as e:
        return {'success': False, 'output': '', 'error': str(e)}

@app.route('/')
def index():
    return render_template('lab3app.html')

@app.route('/generate', methods=['POST'])
def generate_keys():
    return jsonify(run_script('-gen'))

@app.route('/encrypt', methods=['POST'])
def encrypt_file():
    return jsonify(run_script('-enc'))

@app.route('/decrypt', methods=['POST'])
def decrypt_file():
    return jsonify(run_script('-dec'))

@app.route('/check_files', methods=['GET'])
def check_files():
    files = ['initial_file.txt', 'encrypted.bin', 'decrypted.txt', 'symmetric_key.bin', 
             'nonce.bin', 'encrypted_symmetric_key.bin', 'public_key.pem', 'private_key.pem']
    return jsonify({f: os.path.exists(os.path.join(BASE_DIR, f)) for f in files})

if __name__ == '__main__':
    print("Открыть в браузере: http://127.0.0.1:5000")
    app.run(debug=False, host='127.0.0.1', port=5000)