# CV Boiler Analytics

This project provides a web-based analytics dashboard for analyzing CV boiler data. Users can upload Excel files containing boiler data, and the system will generate insights and visualizations.

## Data Format

The system expects Excel files with the following columns:

| **OESTEL FABRIKANT** | **Type prod**     | **TOESTEL**                                           | **Toestel type**     | **Opstel Postcode** |
|----------------------|-------------------|--------------------------------------------------------|-----------------------|----------------------|
| REMEHA               | CALENTA           | REMEHA HRC CALENTA 40C CW5                            | HR-KETEL COMBI        | 6093 CV              |
| INTERGAS             | HRE               | INTERGAS KK HRE 28/24 CW4 A 043317                    | HR-KETEL COMBI        | 6419 EE              |
| VAILLANT             | ECOTEC PLUS       | VAILLANT HRC ECOTEC PLUS VHR 25-30/5-5 CW4            | HR-KETEL COMBI        | 6049 GK              |
| ATAG                 | I SERIE           | ATAG I36EC CW5                                        | HR-KETEL COMBI        | 6374 GE              |
| ATAG                 | I SERIE           | ATAG I28C HR CW4                                      | HR-KETEL COMBI        | 6245 GV              |
| VAILLANT             | ECOTEC PLUS       | VAILLANT HRC ECOTEC PLUS VHR 25-30/5-5 CW4            | HR-KETEL COMBI        | 6042 VT              |
| VAILLANT             | ECOTEC PLUS       | VAILLANT HRC ECOTEC PLUS VHR 25-30/5-5 CW4            | HR-KETEL COMBI        | 6418 JA              |
| VAILLANT             | ECOTEC CLASSIC    | VAILLANT HRC ECOTEC CLASSIC VHR 2328/5-3              | HR-KETEL COMBI        | 6231 GZ              |
| ATAG                 | I SERIE           | ATAG I28C HR CW4                                      | HR-KETEL COMBI        | 6372 VH              |
| VAILLANT             | ECOTEC CLASSIC    | VAILLANT HRC ECOTEC CLASSIC VHR 2328/5-3              | HR-KETEL COMBI        | 6291 EE              |
| VAILLANT             | ECOTEC PLUS       | VAILLANT HRC ECOTEC PLUS VHR 25-30/5-5 CW4            | HR-KETEL COMBI        | 6418 TL              |
| VAILLANT             | ECOTEC CLASSIC    | VAILLANT HRC ECOTEC CLASSIC VHR 2328/5-3              | HR-KETEL COMBI        | 6301 HN              |
| VAILLANT             | ECOTEC CLASSIC    | VAILLANT HRC ECOTEC CLASSIC VHR 2834/5-3              | HR-KETEL COMBI        | 6042 XS              |
| VAILLANT             | ECOTEC CLASSIC    | VAILLANT HRC ECOTEC CLASSIC VHR 2834/5-3              | HR-KETEL COMBI        | 6165 TV              |
| ATAG                 | I SERIE           | ATAG I36EC CW5                                        | HR-KETEL COMBI        | 6417 EW              |
| ATAG                 | I SERIE           | ATAG I36C CW5                                         | HR-KETEL COMBI        | 6225 CP              |
| ATAG                 | I SERIE           | ATAG I36EC CW5                                        | HR-KETEL COMBI        | 6241 JB              |
| INTERGAS             | HRE               | INTERGAS KKHRE 3630 CW5 A 043327                      | HR-KETEL COMBI        | 6267 BA              |

## Prerequisites

### Using Docker (Recommended)
- Docker
- Docker Compose

### Manual Setup
- Python 3.9 or higher
- pip (Python package manager)
- Homebrew (for macOS users)

#### System Dependencies (Manual Setup)

##### macOS
```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install required system dependencies
brew install pango
```

##### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install -y \
    python3-cffi \
    python3-brotli \
    libpango-1.0-0 \
    libharfbuzz0b \
    libpangoft2-1.0-0
```

## Setup and Running

### Using Docker (Recommended)

1. Clone the repository:
```bash
git clone <repository-url>
cd -CV-Boiler-Analytics
```

2. Build and start the containers:
```bash
docker-compose up --build
```

3. Access the application:
   - Open your web browser and navigate to `http://localhost:5000`
   - Upload your Excel file through the web interface
   - View the generated analytics and visualizations
   - Download the analysis as a PDF report

### Manual Setup (Alternative)

1. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Access the application at `http://localhost:5000`

## Features

- Upload Excel files containing CV boiler data
- Automatic analysis of boiler distribution by postal code
- Statistical insights and visualizations
- Interactive dashboard interface
- Download analysis results as PDF reports

## Stopping the Application

### Docker
```bash
docker-compose down
```

### Manual Setup
Press `Ctrl+C` in the terminal where the application is running.

## Notes

- Maximum file upload size is 16MB
- Only Excel (.xlsx) files are supported
- Uploaded files are automatically processed and removed after analysis
- The application runs in production mode when using Docker
- PDF generation requires system-level dependencies (automatically handled in Docker)