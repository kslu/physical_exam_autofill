import os
import json
import time
import sys
import pandas as pd
from google import genai
from google.genai import types
from PIL import Image
from dotenv import load_dotenv
from pdf2image import convert_from_path

# Load environment variables
load_dotenv()

# Checkbox Lookup Table: Maps field categories to their allowed options
CHECKBOX_OPTIONS = {
  "頭頸": [
    "正常", "斜頸", "異常腫塊", "甲狀腺腫", "林巴腺腫大", "其他"
  ],
  "眼部": [
    "正常", "斜視", "睫毛倒插", "眼球震顫", "眼瞼下垂", "其他"
  ],
  "耳鼻喉": [
    "正常", "耳膜破損", "外耳畸形", "耳前廔管", "鼻孔阻塞", "扁桃腺腫大",
    "過敏性鼻炎", "慢性鼻炎", "其他"
  ],
  "胸部": [
    "正常", "胸廓異常", "雞胸", "漏斗胸", "心肺疾病", "心雜音", "心律不整",
    "呼吸聲異常", "其他"
  ],
  "腹部": [
    "正常", "腹部異常腫塊", "疝氣", "其他"
  ],
  "脊柱四肢": [
    "正常", "脊柱側彎", "肢體畸形", "併指", "多指", "關節脫臼", "其他"
  ],
  "皮膚": [
    "正常", "疥瘡", "頭蝨", "寄生蟲", "濕疹", "異位性皮膚炎", "其他"
  ],
  "泌尿生殖": [
    "正常", "隱睪", "陰囊腫大", "包皮異常", "精索靜脈曲張", "其他"
  ],
  "尿液檢查": [
    "正常", "尿蛋白(±)", "尿蛋白(+)", "尿糖(±)", "尿糖(+)", "潛血(±)",
    "潛血(+)", "酸鹼度異常", "比重異常"
  ],
  "篩檢結果": [
    "通過", "未完成", "未通過"
  ],
  "NTU300立體圖": [
    "通過", "不通過", "不會看"
  ]
}

def get_extraction_schema():
  """
  Defines the JSON schema for Gemini to ensure consistent output structure.
  """
  fields = [
    '身體檢查結果_身分證字號', '身體檢查結果_身高(cm)',
    '身體檢查結果_體重(kg)', '身體檢查結果_腰圍(cm)',
    '身體檢查結果_頭頸檢查結果', '身體檢查結果_頭頸異常項目',
    '身體檢查結果_眼部檢查結果', '身體檢查結果_眼部異常項目',
    '身體檢查結果_耳鼻喉檢查結果', '身體檢查結果_耳鼻喉異常項目',
    '身體檢查結果_胸部檢查結果', '身體檢查結果_胸部異常項目',
    '身體檢查結果_腹部檢查結果', '身體檢查結果_腹部異常項目',
    '身體檢查結果_脊柱四肢檢查結果', '身體檢查結果_脊柱四肢異常項目',
    '身體檢查結果_皮膚檢查結果', '身體檢查結果_皮膚異常項目',
    '身體檢查結果_泌尿生殖檢查結果', '身體檢查結果_泌尿生殖異常項目',
    '身體檢查結果_尿液檢查初檢檢查結果', '身體檢查結果_尿液檢查初檢異常項目',
    '身體檢查結果_檢查結果', '身體檢查結果_身體檢查結果建議',
    '身體檢查結果_備註', '身體檢查結果_篩檢日期',
    '聽力檢查結果_篩檢結果', '聽力檢查結果_未通過-左耳',
    '聽力檢查結果_未通過-右耳', '聽力檢查結果_聽力檢查結果建議',
    '聽力檢查結果_備註', '聽力檢查結果_篩檢日期',
    '視力檢查結果_目前是否戴眼鏡矯治', '視力檢查結果_裸視視力',
    '視力檢查結果_眼鏡視力', '視力檢查結果_NTU300立體圖篩檢',
    '視力檢查結果_視力檢查結果建議', '視力檢查結果_備註',
    '視力檢查結果_篩檢日期'
  ]
  properties = {field: {"type": "STRING"} for field in fields}
  return {
    "type": "OBJECT",
    "properties": properties,
    "required": fields
  }

def extract_data_from_image(client, img_obj, filename_ctx,
                           model_name='gemini-flash-latest',
                           max_retries=10):
  """
  Extracts data from an image object using structured output and lookups.
  """
  golden_example = {
    "身體檢查結果_身分證字號": "A123456789",
    "身體檢查結果_身高(cm)": "110",
    "身體檢查結果_體重(kg)": "20",
    "身體檢查結果_腰圍(cm)": "55",
    "身體檢查結果_頭頸檢查結果": "正常",
    "身體檢查結果_篩檢日期": "20260101",
    "視力檢查結果_裸視視力": "右眼:1.0, 左眼:1.0",
    "視力檢查結果_NTU300立體圖篩檢": "通過"
  }

  prompt = f"""
  You are a high-precision medical OCR agent.
  Use the following OPTION LOOKUP TABLE to identify selections on the form.

  {json.dumps(CHECKBOX_OPTIONS, ensure_ascii=False, indent=2)}

  GUIDELINES:
  1. Checkboxes: If '無明顯異常' or '正常' is checked, return '正常'.
  2. Specific Abnormality: If any other box is checked, return '異常'.
  3. Handwriting: Read handwritten numbers and IDs carefully.
  4. Dates: Convert ROC years to YYYYMMDD (e.g., 115 -> 2026).

  REFERENCE EXAMPLE:
  {json.dumps(golden_example, ensure_ascii=False, indent=1)}
  """

  config = types.GenerateContentConfig(
    response_mime_type="application/json",
    response_schema=get_extraction_schema()
  )

  wait_time = 30
  for attempt in range(max_retries):
    try:
      response = client.models.generate_content(
        model=model_name,
        contents=[prompt, img_obj],
        config=config
      )
      return json.loads(response.text)
    except Exception as e:
      if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
        print(f"  [Quota] Limit reached for {filename_ctx}. "
              f"Waiting {wait_time}s (Attempt {attempt+1}/{max_retries})...")
        time.sleep(wait_time)
        wait_time *= 2
      else:
        print(f"  [Error] Unexpected error for {filename_ctx}: {e}")
        break
  return None

def process_directory(input_dir, output_file, model_name, max_retries):
  api_key = os.getenv('GOOGLE_API_KEY')
  if not api_key:
    print("Error: GOOGLE_API_KEY not found.")
    return

  client = genai.Client(api_key=api_key)
  all_data = []
  img_ext = ('.jpg', '.jpeg', '.png', '.webp')
  pdf_ext = ('.pdf',)
  all_ext = img_ext + pdf_ext
  files = [f for f in os.listdir(input_dir) if f.lower().endswith(all_ext)]

  if not files:
    print(f"No supported files found in {input_dir}")
    return

  print(f"Found {len(files)} files in {input_dir}. Using model: {model_name}")

  for filename in files:
    file_path = os.path.join(input_dir, filename)
    print(f"Processing: {filename}...")

    if filename.lower().endswith(pdf_ext):
      try:
        pages = convert_from_path(file_path)
        print(f"  [PDF] Detected {len(pages)} pages.")
        for i, page in enumerate(pages):
          print(f"    Extracting Page {i+1}...")
          data = extract_data_from_image(client, page, f"{filename}_p{i+1}",
                                       model_name=model_name,
                                       max_retries=max_retries)
          if data:
            data['Source_File'] = f"{filename}_page_{i+1}"
            all_data.append(data)
            time.sleep(2)
      except Exception as e:
        print(f"  [Error] Could not process PDF {filename}: {e}")
    else:
      try:
        img = Image.open(file_path)
        data = extract_data_from_image(client, img, filename,
                                     model_name=model_name,
                                     max_retries=max_retries)
        if data:
          data['Source_File'] = filename
          all_data.append(data)
          print(f"  [Success] Data extracted for {filename}")
        time.sleep(2)
      except Exception as e:
        print(f"  [Error] Could not process image {filename}: {e}")

  if not all_data:
    print("No data extracted. Skipping file save.")
    return

  df_new = pd.DataFrame(all_data)
  if output_file.endswith('.xlsx'):
    if os.path.exists(output_file):
      try:
        df_existing = pd.read_excel(output_file)
        df_final = pd.concat([df_existing, df_new], ignore_index=True)
        df_final.to_excel(output_file, index=False)
        print(f"\nBatch complete! Appended to: {output_file}")
      except Exception as e:
        print(f"Error appending: {e}. Saving as new file.")
        df_new.to_excel(output_file, index=False)
    else:
      df_new.to_excel(output_file, index=False)
      print(f"\nBatch complete! Results saved to: {output_file}")
  else:
    if os.path.exists(output_file):
      try:
        with open(output_file, 'r', encoding='utf-8') as f:
          old_data = json.load(f)
        old_data.extend(all_data) if isinstance(old_data, list) \
          else [old_data] + all_data
        with open(output_file, 'w', encoding='utf-8') as f:
          json.dump(old_data, f, indent=4, ensure_ascii=False)
        print(f"\nBatch complete! Appended to: {output_file}")
      except Exception as e:
        print(f"Error appending JSON: {e}. Saving new.")
        with open(output_file, 'w', encoding='utf-8') as f:
          json.dump(all_data, f, indent=4, ensure_ascii=False)
    else:
      with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, indent=4, ensure_ascii=False)
      print(f"\nBatch complete! Saved to: {output_file}")

if __name__ == "__main__":
  import argparse
  parser = argparse.ArgumentParser(description="Batch OCR reports.")
  parser.add_argument("input_directory", help="Dir with images or PDFs.")
  parser.add_argument("output_file", nargs="?", default="results.xlsx",
                      help="Output file path (default: results.xlsx).")
  parser.add_argument("--lite", action="store_true", help="Use flash-lite.")
  parser.add_argument("--retries", type=int, default=5,
                      help="Number of retries for quota limits (default: 5).")
  args = parser.parse_args()

  model = "gemini-flash-lite-latest" if args.lite else "gemini-flash-latest"

  if not os.path.isdir(args.input_directory):
    print(f"Error: {args.input_directory} is not a directory.")
  else:
    process_directory(args.input_directory, args.output_file, model,
                      args.retries)
