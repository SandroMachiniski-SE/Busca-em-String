from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

comparator = SearchComparator()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/search', methods=['POST'])
def search():
    try:
        data = request.json
        text = data.get('text', '')
        pattern = data.get('pattern', '')
        step_by_step = data.get('step_by_step', False)

        if not text or not pattern:
            return jsonify({'error': 'Texto e padrão são obrigatórios'}), 400

        results = comparator.search_all(text, pattern, step_by_step)
        comparison = comparator.compare_performance(results)

        return jsonify({
            'results': results,
            'comparison': {
                'fastest': comparison['fastest']['algorithm'],
                'fastest_time': comparison['fastest']['time_ms'],
                'least_comparisons': comparison['least_comparisons']['algorithm'],
                'least_comparisons_count': comparison['least_comparisons']['comparisons']
            }
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/upload', methods=['POST'])
def upload():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Nenhum arquivo enviado'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'Arquivo vazio'}), 400

        if not file.filename.endswith('.txt'):
            return jsonify({'error': 'Apenas arquivos .txt são permitidos'}), 400

        content = file.read().decode('utf-8')
        return jsonify({'content': content, 'filename': file.filename})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)