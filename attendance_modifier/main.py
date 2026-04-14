import argparse
import sys
import os

from services.ocr_reader_impl import OCRReaderImpl
from services.pdf_generator_impl import PDFGeneratorImpl
from services.time_modifier import DeterministicTimeModifier
from services.pipeline import ReportProcessingPipeline
from core.exceptions import AttendanceAppError

def main():
    parser = argparse.ArgumentParser(description="Attendance PDF Modifier ETL Pipeline.")
    # השארנו את הקלט כחובה
    parser.add_argument("-i", "--input", required=True, help="Path to the original scanned PDF file.")
    # הפכנו את הפלט לאופציונלי (לא חובה). אם המשתמש ירצה לדרוס אותו, הוא יוכל.
    parser.add_argument("-o", "--output", required=False, help="Optional: Path to save the modified PDF file.")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input):
        print(f"Error: Input file '{args.input}' does not exist.")
        sys.exit(1)

    # --- יצירת נתיב הפלט האוטומטי ---
    if args.output:
        output_path = args.output
    else:
        # חילוץ התיקייה, שם הקובץ, והסיומת מתוך נתיב הקלט
        dir_name = os.path.dirname(args.input)
        base_name = os.path.basename(args.input)
        name, ext = os.path.splitext(base_name)
        
        # הרכבת השם החדש
        output_filename = f"{name}_GENERATED{ext}"
        
        # חיבור התיקייה המקורית עם השם החדש
        output_path = os.path.join(dir_name, output_filename) if dir_name else output_filename

    print(f"[*] Starting OCR process for: {args.input}. This might take a few seconds...")

    # --- Dependency Injection ---
    reader = OCRReaderImpl()
    modifier = DeterministicTimeModifier()
    generator = PDFGeneratorImpl()
    
    pipeline = ReportProcessingPipeline(reader, modifier, generator)
    
    try:
        pipeline.process(input_pdf_path=args.input, output_pdf_path=output_path)
        print(f"[+] Successfully generated modified PDF at: {output_path}")
        
    except AttendanceAppError as e:
        print(f"[-] Application Error: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"[-] Unexpected Error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()