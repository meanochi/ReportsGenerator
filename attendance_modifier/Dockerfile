FROM python:3.10-slim

# 1. התקנת תלויות מערכת
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-heb \
    poppler-utils \
    libtesseract-dev \
    fonts-freefont-ttf \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 2. העתקת דרישות והתקנה (עם עקיפת SSL לנטפרי)
COPY requirements.txt .
RUN pip install --upgrade pip --trusted-host pypi.org --trusted-host files.pythonhosted.org
RUN pip install --no-cache-dir -r requirements.txt \
    --trusted-host pypi.org \
    --trusted-host pypi.python.org \
    --trusted-host files.pythonhosted.org

# 3. העתקת הקוד
COPY . .

# הערה: הסרנו את ה-pip install . כי אין קובץ setup.py

# 4. פקודת ההרצה
# וודאו ש-main.py נמצא בתוך תיקייה בשם reports_generator 
# אם הוא נמצא בתיקייה הראשית, שנו ל: ["python", "main.py"]
# במקום ה-ENTRYPOINT הקודם, נסי את זה:
ENTRYPOINT ["python", "main.py"]