from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
import numpy as np
import json
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from weasyprint import HTML
import tempfile
import shutil

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Create a directory for temporary PDFs
PDF_TEMP_DIR = os.path.join(app.config['UPLOAD_FOLDER'], 'temp_pdfs')
os.makedirs(PDF_TEMP_DIR, exist_ok=True)

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

def generate_pdf(analysis_results):
    # Create a unique filename for the PDF
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    pdf_filename = f'cv_analysis_{timestamp}.pdf'
    pdf_path = os.path.join(PDF_TEMP_DIR, pdf_filename)
    
    # Render the HTML template with the analysis results
    html_content = render_template('report.html',
                                 stats=analysis_results['stats'],
                                 top_10_postal=analysis_results['top_10_postal'],
                                 distribution=analysis_results['distribution'],
                                 timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    # Generate PDF from HTML
    HTML(string=html_content).write_pdf(pdf_path)
    return pdf_path

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
            
            # Generate PDF
            pdf_path = generate_pdf(analysis_results)
            
            # Add PDF path to response
            analysis_results['pdf_path'] = os.path.basename(pdf_path)
            
            return jsonify(analysis_results)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            # Clean up the uploaded file
            if os.path.exists(filepath):
                os.remove(filepath)
    
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/download-pdf/<filename>')
def download_pdf(filename):
    try:
        pdf_path = os.path.join(PDF_TEMP_DIR, filename)
        if not os.path.exists(pdf_path):
            return jsonify({'error': 'PDF file not found'}), 404
            
        return send_file(
            pdf_path,
            as_attachment=True,
            download_name='cv_boiler_analysis.pdf',
            mimetype='application/pdf'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        # Clean up the PDF file after sending
        if os.path.exists(pdf_path):
            os.remove(pdf_path)

# Cleanup function to remove old PDF files
def cleanup_old_pdfs():
    try:
        for filename in os.listdir(PDF_TEMP_DIR):
            file_path = os.path.join(PDF_TEMP_DIR, filename)
            # Remove files older than 1 hour
            if os.path.getmtime(file_path) < (datetime.now().timestamp() - 3600):
                os.remove(file_path)
    except Exception as e:
        print(f"Error cleaning up PDFs: {e}")

if __name__ == '__main__':
    # Clean up old PDFs before starting
    cleanup_old_pdfs()
    app.run(debug=True) 