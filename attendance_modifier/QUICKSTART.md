# Quick Start Guide

## 5-Minute Setup

### 1. Install Python packages
```bash
pip install -r requirements.txt
```

### 2. Run the application
```bash
# Process a PDF report
python main.py -i your_report.pdf

# With custom output location
python main.py -i your_report.pdf -o output_folder/modified.pdf
```

### 3. Check the output
- Find the generated PDF in the same folder (or at the specified path)
- Original name: `attendance_report.pdf`
- Generated name: `attendance_report_GENERATED.pdf`

---

## What Does It Do?

```
Input PDF (Type A or Type B)
    ↓
Extract text via OCR
    ↓
Identify report type (Type A or Type B)
    ↓
Parse attendance data
    ↓
Apply deterministic modifications to times
    ↓
Generate new PDF with modified data
    ↓
Output PDF (same structure, modified times)
```

---

## Example Commands

### Process a single report
```bash
python main.py -i C:\Reports\attendance_2024.pdf
```

### Process with custom output
```bash
python main.py -i report.pdf -o modified_report.pdf
```

### Batch processing (multiple files)
```bash
for file in *.pdf; do
    python main.py -i "$file"
done
```

---

## What Gets Modified?

### ✅ Times Modified
- **Entry times** (שעת כניסה): ±15 minutes (deterministic)
- **Exit times** (שעת יציאה): ±15 minutes (deterministic)

### ✅ Validations Applied
- End time is always after start time
- Maximum 12 hours working per day
- Minimum 1 hour working per day

### ✅ Structure Preserved
- Same number of columns
- Same column headers
- Same layout and styling
- Same calculations

### ❌ Not Modified
- Employee names/IDs (if extracted)
- Date values
- Report structure/format
- Original file

---

## Sample Output

### Type A Report (Landscape)
```
ג.ע. הנשר כח אדם בע"מ - דוח מעודכן

תאריך    יום    מקום    כניסה    יציאה    הפסקה    סה"כ    100%    125%    150%
1/10     שני    כללי    09:05    17:08    00:30    7.53    7.53    0.00    0.00
2/10     שלי    כללי    08:50    17:15    00:30    8.08    8.00    0.08    0.00
```

### Type B Report (Portrait)
```
כרטיס עובד לחודש - דוח מעודכן

תאריך    יום    כניסה    יציאה    סה"כ שעות    הערות
1/9      שני    08:35    16:40    8.08
2/9      שלי    09:10    17:05    7.92
```

---

## Troubleshooting

### Error: "Input file does not exist"
```bash
# Check file path
python main.py -i C:\full\path\to\file.pdf
```

### Error: "Could not determine report type"
- File might be corrupted
- OCR extraction failed
- Format not recognized (only Type A and B supported)

### Output file not created
- Check write permissions in output directory
- Ensure output path is valid
- Check disk space

### Hebrew text appears garbled
- Ensure Arial font is installed
- Check PDF viewer supports RTL text
- Try opening with different PDF viewer

---

## Output File Details

**Auto-generated filename**:
- Original: `report.pdf`
- Generated: `report_GENERATED.pdf`
- Location: Same as input file (unless `-o` specified)

**File size**:
- Usually slightly larger (PDF overhead)
- Content similar to original

**Timestamp**:
- Creation time = script execution time
- Modification time = script execution time

---

## Next Steps

1. **Review the generated PDF**
   - Compare with original
   - Verify modifications applied
   - Check formatting preserved

2. **Verify time modifications**
   - Original times → Modified times
   - All within valid ranges

3. **Check calculations**
   - Total hours recalculated
   - Overtime categories correct (Type A)

---

## Need Help?

- See [README.md](README.md) for full documentation
- See [REQUIREMENTS_VERIFICATION.md](REQUIREMENTS_VERIFICATION.md) for technical details
- Check source code comments for implementation details

---

## Key Features

✅ **Automatic report type detection** - Works with both Type A and Type B  
✅ **Deterministic modifications** - Same input = Same output (reproducible)  
✅ **Logical validation** - End time > Start time, max 12 hours/day  
✅ **Structure preservation** - PDF looks like original  
✅ **Hebrew support** - Proper RTL text rendering  
✅ **Error handling** - Clear error messages  
✅ **Flexible output** - Auto-generated or custom filename  

---

## System Requirements

- Python 3.8+
- 50 MB free disk space (for dependencies)
- PDF reader (to view output)
- Windows/Mac/Linux

---

**Ready to go!** Run `python main.py -i your_file.pdf` to get started.