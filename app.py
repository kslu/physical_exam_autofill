import streamlit as st
import os
import pandas as pd
from google import genai
from dotenv import load_dotenv
from batch_ocr import extract_data_from_image, CHECKBOX_OPTIONS
from pdf2image import convert_from_path
import time

# Load environment variables
load_dotenv()

st.set_page_config(page_title="Physical Exam OCR", page_icon="📋")

st.title("📋 Physical Exam Data Extractor")
st.markdown("""
Upload scanned images or PDFs of health reports to extract data into Excel.
""")

# Sidebar for Configuration
with st.sidebar:
  st.header("Settings")
  api_key = st.text_input("Gemini API Key",
                         value=os.getenv("GOOGLE_API_KEY", ""),
                         type="password")
  use_lite = st.checkbox("Use Lite Model (Save Quota)", value=False)
  retries = st.slider("Retry Attempts (on Quota Limit)", 1, 20, 5)

# File Uploader
uploaded_files = st.file_uploader("Choose images or PDFs",
                                 type=['jpg', 'jpeg', 'png', 'webp', 'pdf'],
                                 accept_multiple_files=True)

if uploaded_files:
  if not api_key:
    st.error("Please enter your Gemini API Key in the sidebar.")
  else:
    if st.button("Start Extraction"):
      client = genai.Client(api_key=api_key)
      model_name = "gemini-flash-lite-latest" if use_lite \
                   else "gemini-flash-latest"
      
      all_results = []
      progress_bar = st.progress(0)
      status_text = st.empty()
      
      for idx, uploaded_file in enumerate(uploaded_files):
        filename = uploaded_file.name
        status_text.text(f"Processing: {filename}...")
        
        # Save temp file
        with open(filename, "wb") as f:
          f.write(uploaded_file.getbuffer())
        
        try:
          if filename.lower().endswith(".pdf"):
            pages = convert_from_path(filename)
            for i, page in enumerate(pages):
              status_text.text(f"Extracting {filename} - Page {i+1}...")
              data = extract_data_from_image(client, page, 
                                           f"{filename}_p{i+1}",
                                           model_name=model_name,
                                           max_retries=retries)
              if data:
                data['Source_File'] = f"{filename}_page_{i+1}"
                all_results.append(data)
          else:
            from PIL import Image
            img = Image.open(filename)
            data = extract_data_from_image(client, img, filename,
                                         model_name=model_name,
                                         max_retries=retries)
            if data:
              data['Source_File'] = filename
              all_results.append(data)
              
        except Exception as e:
          st.error(f"Error processing {filename}: {e}")
        
        # Cleanup temp file
        if os.path.exists(filename):
          os.remove(filename)
          
        # Update progress
        progress_bar.progress((idx + 1) / len(uploaded_files))
        time.sleep(1) # Politeness
      
      status_text.text("Extraction Complete!")
      
      if all_results:
        df = pd.DataFrame(all_results)
        st.success(f"Successfully extracted {len(all_results)} records!")
        st.dataframe(df)
        
        # Download Link
        output_name = "extracted_data.xlsx"
        df.to_excel(output_name, index=False)
        with open(output_name, "rb") as f:
          st.download_button(
            label="📥 Download Excel Results",
            data=f,
            file_name=output_name,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
          )
        os.remove(output_name)
      else:
        st.warning("No data could be extracted.")
