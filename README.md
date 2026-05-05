# Physical Exam OCR Extraction Script

**New to software?** Check out our [BEGINNER_GUIDE.md](./BEGINNER_GUIDE.md) for a step-by-step tutorial on setting everything up on your Mac.

---

This tool uses the Google Gemini API to extract structured data from scanned physical examination reports into Excel spreadsheets or JSON dictionaries.

## Prerequisites

1.  **Python 3.9+** installed.
2.  **Gemini API Key**: Obtain one from [Google AI Studio](https://aistudio.google.com/app/apikey).
3.  **Poppler**: Required for PDF support.
    - macOS: `brew install poppler`
    - Windows: Download from [poppler for Windows](https://github.com/oschwartz10612/poppler-windows/releases/) and add to PATH.

## Setup

For a clean installation, it is recommended to use a Python Virtual Environment. See [SETUP_VENV.md](./SETUP_VENV.md) for detailed instructions.

1.  **Install Dependencies**:
    ```bash
    pip install google-genai Pillow python-dotenv pandas openpyxl pdf2image
    ```

2.  **Configure API Key**:
    Create a file named `.env` in the same directory as the script and add your key:
    ```text
    GOOGLE_API_KEY=your_api_key_here
    ```

## Usage

### Batch Processing (Recommended)
Process an entire folder of images and save the results directly to an Excel file:
```bash
python batch_ocr.py input_folder output_results.xlsx
```
- **Optional**: Add `--lite` to use the `gemini-flash-lite-latest` model to save
  on daily quota.
- **Automatic Quota Handling**: This script automatically catches
  `RESOURCE_EXHAUSTED` (429) errors, waits for the limit to reset, and retries.
- **Excel Output**: Generates a spreadsheet with headers matching the New
  Taipei City health report format.

### Single File Quick Test
Extract data from one image and print it to the terminal:
```bash
python ocr_report.py sample.jpeg
```
- **Optional**: Add `--lite` to use the lite model.

## Features
- **Excel Integration**: Direct output to `.xlsx` using pandas.
- **ROC Date Conversion**: Automatically converts Taiwan ROC years (e.g., 115) to standard YYYYMMDD (2026).
- **Handwriting Support**: Optimized with Gemini Flash to handle handwritten marks and stamps.
- **Robustness**: Built-in exponential backoff for handling API rate limits.
