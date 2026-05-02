# Beginner's Guide: Getting Started on macOS

Welcome! This guide will help you set up and run the Physical Exam OCR tool on your MacBook, even if you have never used the terminal or written code before.

---

## Step 1: Open the Terminal
The "Terminal" is where you will type commands.
1. Press `Command + Space` on your keyboard.
2. Type **Terminal** and press `Enter`.

---

## Step 2: Install Homebrew (The Package Manager)
Homebrew makes it easy to install software on a Mac.
1. Copy and paste the following command into your terminal and press `Enter`:
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
2. Follow the instructions on the screen (it may ask for your Mac password).
3. **Important:** After it finishes, look for a section called "Next steps" in the terminal. Copy and paste the 2-3 lines it provides to add Homebrew to your "PATH".

---

## Step 3: Install Python and PDF Support
Now we will install Python and a tool called "Poppler" that helps the script read PDF files.
1. In the terminal, type:
   ```bash
   brew install python poppler
   ```
2. Wait for the installation to finish.

---

## Step 4: Download the Project
1. If you received this project as a ZIP file, double-click it to unzip it.
2. In the terminal, type `cd ` (type "cd" followed by a space), then **drag the folder** containing this project from your Desktop/Downloads directly into the terminal window. It should look something like:
   ```bash
   cd /Users/yourname/Downloads/physical-exam-autofill
   ```
3. Press `Enter`.

---

## Step 5: Set Up the "Virtual Environment"
This creates a small, isolated "bubble" for the project so it doesn't interfere with other things on your Mac.
1. Type:
   ```bash
   python3 -m venv venv
   ```
2. "Activate" the bubble:
   ```bash
   source venv/bin/activate
   ```
   *(You should now see `(venv)` at the start of your terminal line.)*

---

## Step 6: Install the Requirements
Now we install the specific tools the script needs to "read" images and PDF files.
1. Type:
   ```bash
   pip install google-genai Pillow python-dotenv pandas openpyxl pdf2image
   ```

---

## Step 7: Add your Gemini API Key
1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey) and click **Create API Key**.
2. Copy the key (it starts with `AIza...`).
3. Back in the terminal, type:
   ```bash
   nano .env
   ```
4. Paste your key into the window so it looks like this:
   ```text
   GOOGLE_API_KEY=your_copied_key_here
   ```
5. Press `Control + O` then `Enter` to save, and `Control + X` to exit.

---

## Step 8: Run the Tool!
1. Put all your scanned images and PDF files into a folder named `my_scans`.
2. Run the script:
   ```bash
   python batch_ocr.py my_scans my_results.xlsx
   ```
3. When it's done, you will find a new file called `my_results.xlsx` in your project folder. You can open this with Excel or Numbers!

---

## Summary of Daily Use
Next time you want to use the tool:
1. Open Terminal.
2. `cd` into the folder.
3. `source venv/bin/activate`
4. `python batch_ocr.py input_folder output.xlsx`
