from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import json
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def analyze_data(df):
    # Filter for CV boilers
    cv_boilers = df[df['Toestel type'].str.contains('KETEL', case=False, na=False)]
    
    # Analyze CV boiler distribution per postal code
    cv_by_postal = cv_boilers.groupby('Opstel Postcode').size().reset_index(name='cv_boiler_count')
    
    # Calculate statistics
    stats = {
        'total_cv_boilers': int(cv_by_postal['cv_boiler_count'].sum()),
        'avg_boilers_per_postal': float(cv_by_postal['cv_boiler_count'].mean()),
        'median_boilers_per_postal': float(cv_by_postal['cv_boiler_count'].median()),
        'total_postal_codes': len(cv_by_postal),
        'individual_boilers': int(len(cv_by_postal[cv_by_postal['cv_boiler_count'] == 1])),
        'estimated_cost': int(len(cv_by_postal[cv_by_postal['cv_boiler_count'] == 1]) * 800)
    }
    
    # Get top 10 postal codes
    top_10_postal = cv_by_postal.sort_values('cv_boiler_count', ascending=False).head(10)
    top_10_data = top_10_postal.to_dict('records')
    
    # Prepare distribution data for histogram
    distribution = cv_by_postal['cv_boiler_count'].value_counts().sort_index().to_dict()
    
    return {
        'stats': stats,
        'top_10_postal': top_10_data,
        'distribution': distribution
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and file.filename.endswith('.xlsx'):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            df = pd.read_excel(filepath)
            analysis_results = analyze_data(df)
            return jsonify(analysis_results)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            # Clean up the uploaded file
            if os.path.exists(filepath):
                os.remove(filepath)
    
    return jsonify({'error': 'Invalid file type'}), 400

if __name__ == '__main__':
    app.run(debug=True) 