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

def run_single_ocr(image_path, model_name, max_retries):
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

  print(f"Processing single file: {image_path} using model: {model_name}...")

  try:
    img = Image.open(image_path)
    result = extract_data_from_image(client, img, image_path,
                                   model_name=model_name,
                                   max_retries=max_retries)

    if result:
      print("\n--- Extraction Results ---")
      print(json.dumps(result, indent=4, ensure_ascii=False))
    else:
      print("\n[Failed] Could not extract data.")

  except Exception as e:
    print(f"Error: {e}")

if __name__ == "__main__":
  import argparse

  parser = argparse.ArgumentParser(description="Single-file OCR test.")
  parser.add_argument("image_path", help="Path to the image file.")
  parser.add_argument("--lite", action="store_true",
                      help="Use the gemini-flash-lite-latest model.")
  parser.add_argument("--retries", type=int, default=5,
                      help="Number of retries for quota limits (default: 5).")

  args = parser.parse_args()

  model = "gemini-flash-lite-latest" if args.lite else "gemini-flash-latest"
  run_single_ocr(args.image_path, model, args.retries)
