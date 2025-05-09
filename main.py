from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from rapidfuzz import process
import easyocr
import numpy as np
import cv2
import re
import torch

app = FastAPI()

# ตรวจสอบ CUDA
print("CUDA Available:", torch.cuda.is_available())
if torch.cuda.is_available():
    print("GPU Name:", torch.cuda.get_device_name(0))

# โหลด EasyOCR Reader ครั้งเดียว
reader = easyocr.Reader(['th', 'en'], gpu=torch.cuda.is_available())

@app.post("/ocr/car-plate")
async def ocr_car_plate(file: UploadFile = File(...)):
    image = await file.read()
    npimg = np.frombuffer(image, np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    # อ่าน OCR
    results = reader.readtext(img)

    # ดึงข้อความมา
    texts = [text[1] for text in results]

    # (ตัวอย่างง่าย) แปลงผลลัพธ์เป็น JSON
    response = {
        "full_text": " ".join(texts),
        "fields": extract_fields(texts)
    }
    return JSONResponse(content=response)

def match_province(text):

    provinces = [
        "กรุงเทพมหานคร", "กระบี่", "กาญจนบุรี", "กาฬสินธุ์", "กำแพงเพชร", "ขอนแก่น",
        "จันทบุรี", "ฉะเชิงเทรา", "ชลบุรี", "ชัยนาท", "ชัยภูมิ", "ชุมพร", "เชียงราย", "เชียงใหม่",
        "ตรัง", "ตราด", "ตาก", "นครนายก", "นครปฐม", "นครพนม", "นครราชสีมา", "นครศรีธรรมราช",
        "นครสวรรค์", "นนทบุรี", "นราธิวาส", "น่าน", "บึงกาฬ", "บุรีรัมย์", "ปทุมธานี", "ประจวบคีรีขันธ์",
        "ปราจีนบุรี", "ปัตตานี", "พระนครศรีอยุธยา", "พะเยา", "พังงา", "พัทลุง", "พิจิตร", "พิษณุโลก",
        "เพชรบุรี", "เพชรบูรณ์", "แพร่", "พรรคใต้", "ภูเก็ต", "มหาสารคาม", "มุกดาหาร", "แม่ฮ่องสอน",
        "ยะลา", "ยโสธร", "ร้อยเอ็ด", "ระนอง", "ระยอง", "ราชบุรี", "ลพบุรี", "ลำปาง", "ลำพูน",
        "เลย", "ศรีสะเกษ", "สกลนคร", "สงขลา", "สตูล", "สมุทรปราการ", "สมุทรสงคราม", "สมุทรสาคร",
        "สระแก้ว", "สระบุรี", "สิงห์บุรี", "สุโขทัย", "สุพรรณบุรี", "สุราษฎร์ธานี", "สุรินทร์",
        "หนองคาย", "หนองบัวลำภู", "อ่างทอง", "อำนาจเจริญ", "อุดรธานี", "อุตรดิตถ์", "อุทัยธานี",
        "อุบลราชธานี"
    ]

    # คืนค่าจังหวัดที่ใกล้เคียงที่สุด และคะแนน
    match, score, _ = process.extractOne(text, provinces, score_cutoff=80)  # 0-100
    return match if match else None

# ดึงข้อมูลเฉพาะออกมาอย่างง่าย
def extract_fields(texts):
    if isinstance(texts, list):
        text = " ".join(texts)
    else:
        text = texts

    text = text.lower().replace('\n', ' ').replace('|', '1').replace('ฺ', '').replace(']', 'l')

    # ป้ายทะเบียน
    plate_regex = r"(\d{0,3}[ก-ฮ]{1,2}\s?\d{1,4})"
    match = re.search(plate_regex, text)
    number_plate = match.group(1).replace(" ", "") if match else None

    # หา province แบบ fuzzy
    province = match_province(text)

    return {
        "number_plate": number_plate,
        "province": province
    }