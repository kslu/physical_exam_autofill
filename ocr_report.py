import os
import json
import sys
from google import genai
from PIL import Image
from dotenv import load_dotenv

# Import the optimized extraction logic from batch_ocr
try:
  from batch_ocr import extract_data_from_image
except ImportError:
  print("Error: Could not find batch_ocr.py. Please ensure it is in the "
        "same directory.")
  sys.exit(1)

# Load environment variables
load_dotenv()

def run_single_ocr(image_path):
  """
  Wrapper to run a single OCR task using the shared batch logic.
  """
  api_key = os.getenv('GOOGLE_API_KEY')
  if not api_key:
    print("Error: GOOGLE_API_KEY not found in .env file.")
    return

  client = genai.Client(api_key=api_key)

  # Check if file exists
  if not os.path.exists(image_path):
    print(f"Error: File not found at {image_path}")
    return

  print(f"Processing single file: {image_path}...")

  try:
    img = Image.open(image_path)
    result = extract_data_from_image(client, img, image_path)

    if result:
      print("\n--- Extraction Results ---")
      print(json.dumps(result, indent=4, ensure_ascii=False))
    else:
      print("\n[Failed] Could not extract data.")

  except Exception as e:
    print(f"Error: {e}")

if __name__ == "__main__":
  if len(sys.argv) < 2:
    print("Usage: python ocr_report.py <image_path>")
  else:
    run_single_ocr(sys.argv[1])
