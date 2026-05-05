# Beginner's Guide: Getting Started on Windows

This guide will help you set up and run the Physical Exam OCR tool on your
Windows computer. No coding experience is required!

---

## Step 1: Install Python
Python is the "engine" that runs the script.
1. Visit [python.org](https://www.python.org/downloads/).
2. Click the yellow **Download Python** button.
3. Open the file you just downloaded.
4. **IMPORTANT:** Check the box at the bottom that says **"Add Python to PATH"**.
5. Click **Install Now**.

---

## Step 2: Install Poppler (For PDF Support)
This tool allows the script to read PDF files.
1. Go to the [Poppler for Windows page](https://github.com/oschwartz10612/poppler-windows/releases/).
2. Download the latest `.zip` file (e.g., `poppler-24.xx.x.zip`).
3. Right-click the downloaded file and select **Extract All**.
4. Move the extracted folder to your `C:\` drive and rename it to `poppler`.
   (You should now have a folder at `C:\poppler`).
5. **Add to System PATH:**
   - Press the `Windows Key` and type **"Environment Variables"**.
   - Select **"Edit the system environment variables"**.
   - Click the **Environment Variables** button at the bottom.
   - Under "System variables", find **Path**, select it, and click **Edit**.
   - Click **New** and type: `C:\poppler\Library\bin`
   - Click **OK** on all windows to save.

---

## Step 3: Open the Project Folder
1. If you received this as a ZIP file, right-click and **Extract All**.
2. Open the extracted folder.
3. In the address bar at the top of the folder window, type `powershell` and
   press **Enter**. A blue window will open.

---

## Step 4: Create a Virtual Environment
This creates a clean workspace for the project.
1. In the blue PowerShell window, type:
   ```powershell
   python -m venv venv
   ```
2. **Activate the workspace:**
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```
   *If you get an "Execution Policy" error, run this command first, then try again:*
   `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

---

## Step 5: Install Requirements
Type this command to install the necessary libraries:
```powershell
pip install google-genai Pillow python-dotenv pandas openpyxl pdf2image
```

---

## Step 6: Add your API Key
1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey) and click
   **Create API Key**. Copy the key.
2. Back in your project folder (in Windows Explorer), right-click and create a
   **New > Text Document**.
3. Name the file exactly `.env` (make sure there is no `.txt` at the end).
4. Open it with Notepad and paste:
   `GOOGLE_API_KEY=your_key_here`
5. Save and close.

---

## Step 7: Run the Tool!
Put your images in a folder (e.g., `my_scans`) and run:
```powershell
python batch_ocr.py my_scans results.xlsx
```
Check your folder for a new file named `results.xlsx`!

---

## Summary of Daily Use
Every time you want to use the tool:
1. Open the folder and type `powershell` in the address bar.
2. Type: `.\venv\Scripts\Activate.ps1`
3. Type: `python batch_ocr.py input_folder output.xlsx`
