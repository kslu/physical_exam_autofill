# Setting Up a Python Virtual Environment

Using a virtual environment (venv) keeps the dependencies required by this project separate from your global Python installation.

## 1. Create the Virtual Environment

Open your terminal in the project directory and run:

### macOS / Linux
```bash
python3 -m venv venv
```

### Windows
```powershell
python -m venv venv
```

## 2. Activate the Virtual Environment

You must activate the environment every time you open a new terminal window.

### macOS / Linux
```bash
source venv/bin/activate
```

### Windows (Command Prompt)
```cmd
venv\Scripts\activate
```

### Windows (PowerShell)
```powershell
.\venv\Scripts\Activate.ps1
```

## 3. Install Dependencies

Once the environment is activated (you should see `(venv)` in your terminal prompt), install the required packages:

```bash
pip install google-genai Pillow python-dotenv pandas openpyxl pdf2image
```

**Note:** For PDF support, you also need to install `poppler`:
- macOS: `brew install poppler`
- Windows: [Instructions here](https://github.com/oschwartz10612/poppler-windows/releases/)

## 4. Run the Script

With the environment still active, run your batch task:

```bash
python batch_ocr.py input_folder results.xlsx
```

## 5. Deactivate

When you are finished, you can exit the virtual environment by typing:

```bash
deactivate
```
