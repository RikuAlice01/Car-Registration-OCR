# Car-Registration-OCR 🚗🔍

An OCR system for reading Thai car license plates using FastAPI + EasyOCR. Supports image upload and automatically extracts the license plate number and province from the plate.

## ✅ Features

- Supports Thai and English languages
- Extracts text from license plate images using EasyOCR
- Detects license plate numbers (Thai characters + digits)
- Identifies the province from the text
- Provides a simple REST API

## 🛠️ Technologies Used

- [FastAPI](https://fastapi.tiangolo.com/)
- [EasyOCR](https://github.com/JaidedAI/EasyOCR)
- OpenCV
- PyTorch (with GPU support if available)

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/RikuAlice01/Car-Registration-OCR.git
cd Car-Registration-OCR
````

### 2. Create a Python Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Server

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### 5. Test the API with curl or Postman

```bash
curl -X POST "http://localhost:8000/ocr/car-plate" \
  -F "file=@path_to_your_image.jpg"
```

## 📄 Example Response

```json
{
  "full_text": "1กข 1234 กรุงเทพมหานคร",
  "fields": {
    "number_plate": "1กข 1234",
    "province": "กรุงเทพมหานคร"
  }
}
```

## 🧠 Notes

* This version does not crop the license plate area (can be improved using YOLO or other detection models)
* Can be extended to support multiple plates in one image

## 📁 Project Structure

```
Car-Registration-OCR/
├── main.py                # FastAPI main application
├── requirements.txt       # Project dependencies
├── README.md              # This file
└── thai_provinces.py      # List of all Thai provinces (if separated)
```

## 📜 License

MIT License

---

Made with ❤️ by Riku Alice