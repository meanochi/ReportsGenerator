# Attendance Report Modifier - Python Solution

## Project Overview

This Python application processes **PDF attendance reports**, identifies their type, applies **deterministic business rule transformations** to attendance times, and generates **modified PDF reports** with the same structure and formatting as the original.

### Objective
Given attendance reports in PDF format (of two different types), the application:
1. **Reads** the PDF and extracts text using OCR
2. **Classifies** the report type (Type A or Type B) based on data patterns
3. **Parses** the text into structured data, applying logical validations
4. **Modifies** the attendance times deterministically using business rules
5. **Generates** a new PDF preserving the original structure and style

---

## Implementation Summary

### ✅ Core Requirements Met

#### 1. **Report Type Identification**
- **Implementation**: `services/classifier.py` - `ReportClassifier` class
- **Strategy**: Data-pattern matching using date formats
  - Type A: Reports with **long-year dates** (DD/MM/YYYY) - e.g., "02/10/2022" (Nesher HR reports)
  - Type B: Reports with **short-year dates** (D/M/YY) - e.g., "1/9/22" (Employee card reports)
  - **Fallback**: Keyword matching as secondary classification method
- **Handling OCR Noise**: Robust to OCR errors in Hebrew text

#### 2. **Deterministic Business Rules**
- **Implementation**: `services/time_modifier.py` - `DeterministicTimeModifier` class
- **Modifications Applied**:
  - **Hash-based modification**: Each date generates unique, reproducible modifications using MD5 hash
  - **Time delta**: ±15 minute adjustments deterministically derived from date and salt ("in"/"out")
  - **Validation rules**:
    - ✓ **End time > Start time**: If violation occurs, end time is adjusted forward
    - ✓ **Reasonable working hours**: Maximum 12 hours per day
    - ✓ **Minimum work duration**: At least 1 hour enforced
- **Result**: Reliable, repeatable variations that maintain logical correctness

#### 3. **PDF Generation**
- **Implementation**: `services/pdf_generator_impl.py` - `PDFGeneratorImpl` class
- **Structure Preservation**:
  - **Type A** (Landscape): Full payroll report with 10 columns including overtime categories
    - Columns: Date | Day | Location | Entry | Exit | Break | Total Hours | Base 100% | Overtime 125% | Overtime 150%
    - Calculates correct hour categories based on work duration
  - **Type B** (Portrait): Simple employee card with 6 columns
    - Columns: Date | Day | Entry Time | Exit Time | Total Hours | Notes
  - **Styling**: Grid layout, colored headers, consistent formatting
  - **Hebrew Support**: RTL text rendering with font registration (Arial TTF)
  - **Calculated Fields**: 
    - Day of week (computed from date)
    - Total hours (calculated from times)
    - Overtime categories for Type A

---

## Architecture & Design Patterns

### Clean Architecture Layers
```
main.py
    ↓
services/pipeline.py (Orchestrator - Dependency Injection)
    ├─→ services/ocr_reader_impl.py (OCR Extraction)
    ├─→ services/classifier.py (Classification)
    ├─→ parsers/parser_factory.py + type_*_parser.py (Parsing)
    ├─→ services/time_modifier.py (Transformation)
    └─→ services/pdf_generator_impl.py (PDF Generation)
```

### Design Patterns Used
- **Dependency Injection**: Pipeline receives components via constructor
- **Strategy Pattern**: Factory creates type-specific parsers
- **Template Method**: Common parsing logic, type-specific implementations
- **DTO Pattern**: `AttendanceRow` and `AttendanceReport` for data transfer
- **Interface Segregation**: Each component implements a contract (IReportParser, ITimeModifier, etc.)

### Folder Structure
```
core/
  ├─ enums.py           # ReportType enum
  ├─ exceptions.py      # Custom exceptions
  ├─ models.py          # AttendanceReport, AttendanceRow DTOs

interfaces/
  ├─ modifier.py        # ITimeModifier contract
  ├─ parser.py          # IReportParser contract
  ├─ pdf_generator.py   # IPDFGenerator contract
  └─ pdf_reader.py      # IPDFReader contract

services/
  ├─ pipeline.py           # Main orchestrator
  ├─ classifier.py         # Report type classification
  ├─ ocr_reader_impl.py    # PDF text extraction
  ├─ time_modifier.py      # Business logic transformations
  └─ pdf_generator_impl.py # PDF output generation

parsers/
  ├─ parser_factory.py     # Factory for type-specific parsers
  ├─ type_a_parser.py      # Parser for Type A reports
  └─ type_b_parser.py      # Parser for Type B reports

utils/
  ├─ regex_helpers.py      # Date/time regex patterns
  ├─ time_utils.py         # Time conversion and hash-based deltas
  └─ validators.py         # Date validation logic
```

---

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Install Dependencies

```bash
pip install -r requirements.txt
```

**Dependencies:**
- `reportlab==4.0.8` - PDF generation
- `PyMuPDF==1.23.8` - PDF text extraction (OCR)

### Verify Installation

```bash
python -c "import fitz; import reportlab; print('Dependencies OK')"
```

---

## Usage Instructions

### Basic Usage
```bash
python main.py -i <input_pdf_path>
```
**Output**: Automatically saves as `<filename>_GENERATED.pdf` in the same directory

### With Custom Output Path
```bash
python main.py -i report.pdf -o modified_report.pdf
```

### Example Workflow
```bash
# Process a Type A report
python main.py -i attendance_2024_type_a.pdf

# Process a Type B report with custom output
python main.py -i employee_card.pdf -o updated_card.pdf
```

### Example Output
```
[*] Starting OCR process for: attendance_2024.pdf. This might take a few seconds...
[+] Successfully generated modified PDF at: attendance_2024_GENERATED.pdf
```

---

## Technical Details

### How Classification Works

**Data-Driven Approach** (Primary):
1. Extract all date patterns from OCR text
2. Count long-year format occurrences (DD/MM/YYYY)
3. Count short-year format occurrences (D/M/YY)
4. Compare: whichever format appears more frequently determines type

**Keyword Fallback** (if patterns are inconclusive):
- Type A: "ג.ע. הנשר" or "הנשר כח אדם"
- Type B: "כרטיס עובד"

### How Modification Works

**Deterministic Algorithm**:
```
For each attendance row:
  1. Extract date from row
  2. Create hash: MD5(date + "_in") → delta_in_minutes
  3. Create hash: MD5(date + "_out") → delta_out_minutes
  4. Apply deltas: new_time = original_time ± delta
  5. Validate: end_time > start_time (adjust if needed)
  6. Validate: working_hours ≤ 12 (cap if exceeded)
  7. Store: original and new times in row object
```

**Key Features**:
- ✓ **Deterministic**: Same input always produces same output
- ✓ **Repeatable**: Modifications based on date, not random values
- ✓ **Reversible**: Can audit original vs. modified times
- ✓ **Safe**: Logical validations prevent invalid scenarios

### How PDF Generation Works

**Type-Specific Table Generation**:
1. Create appropriate table structure (landscape for Type A, portrait for Type B)
2. Build rows from modified attendance data
3. Calculate derived fields (day of week, total hours, overtime categories)
4. Apply consistent styling (grid, headers, fonts)
5. Register Hebrew fonts for proper RTL rendering
6. Export to PDF file

**Data Preservation**:
- Original structure and column order maintained
- Calculated fields match original report style
- Header formatting and table styling preserved

---

## Requirements Verification Checklist

### ✅ Functional Requirements
- [x] **Identification of report type** - Implemented in `classifier.py` using data-pattern matching
- [x] **Applying sensible changes** - Implemented in `time_modifier.py` with deterministic business rules
  - [x] Correct start/end times (end > start)
  - [x] Valid working hours (≤12 hours/day)
  - [x] Minimum 1 hour work duration
- [x] **Creating new report** - Implemented in `pdf_generator_impl.py`
  - [x] PDF structure preserved (headings, columns, order)
  - [x] Style maintained (grid, fonts, formatting)
  - [x] Data replaced with variations
  - [x] Sums and calculations updated

### ✅ Technical Requirements
- [x] **Language**: Python only (no external languages)
- [x] **Python version**: 3.8+ compatible
- [x] **No external dependencies**: Only standard libraries + specified packages
- [x] **Error handling**: Custom exceptions with meaningful messages
- [x] **Logging**: Clear console output for user feedback

### ✅ Deliverables
- [x] **Source code** - Full implementation with clean architecture
- [x] **README with running instructions** - This file
- [x] **Structured codebase** - Well-organized, documented, maintainable
- [x] **Design patterns** - SOLID principles applied throughout

---

## Error Handling

The application includes robust error handling:

- **ClassificationError**: Raised when report type cannot be determined
- **ParsingError**: Raised when text parsing fails
- **AttendanceAppError**: Base exception for all application errors

### Example Error Scenarios
```bash
# Missing input file
$ python main.py -i nonexistent.pdf
Error: Input file 'nonexistent.pdf' does not exist.

# Unrecognizable report format
$ python main.py -i corrupted.pdf
[-] Application Error: Could not determine report type. Patterns and keywords not found.

# Unexpected error
$ python main.py -i bad_pdf.pdf
[-] Unexpected Error occurred: [error details]
```

---

## Testing & Validation

### Manual Testing Steps
1. Test with Type A report: `python main.py -i type_a_sample.pdf`
2. Test with Type B report: `python main.py -i type_b_sample.pdf`
3. Verify output PDF exists and is readable
4. Validate time modifications are applied
5. Confirm structure and formatting preserved
6. Check Hebrew text renders correctly

---

## Notes for Interview/Discussion

### Key Thinking & Design Decisions

1. **Classification Strategy**:
   - Chose data-pattern matching over keyword search to handle OCR noise
   - Date format frequency is more reliable than keyword accuracy in Hebrew OCR text

2. **Deterministic Modification**:
   - Used hash-based approach for reproducibility
   - Ensures same date always produces same modification
   - Allows auditing of original vs. modified data
   - Maintains business rule constraints (logical validity)

3. **Architecture**:
   - Clean separation of concerns (parsing, classification, modification, generation)
   - Dependency injection for testability
   - Interface-based contracts for extensibility
   - DTO pattern for data transfer

4. **PDF Generation**:
   - Two separate table structures for different report types
   - Calculated fields (day of week, hour categories) derived from data
   - Hebrew text support with proper RTL handling
   - Preserved original styling and formatting conventions

5. **Error Handling**:
   - Custom exception hierarchy for clear error categorization
   - User-friendly error messages
   - Graceful failure with exit codes

---

## Future Enhancements

Potential improvements:
- Add more report type support (extensible parser factory)
- Configuration file for business rules (JSON/YAML)
- Validation report generation (before/after comparison)
- Batch processing of multiple PDFs
- Logging to file for audit trail
- Unit tests with sample data
- Performance optimization for large reports

---

## Contact & Support

For questions about implementation details or design decisions, refer to the source code comments (including Hebrew technical documentation) throughout the codebase.
