# Attendance Modifier

A small Python package for reading attendance PDF reports, classifying report types, modifying time values, and generating updated PDF output.

## Structure

- `core/` - data models, enums, and exceptions
- `interfaces/` - contract definitions for PDF readers, parsers, modifiers, and generators
- `services/` - implementations and the main pipeline
- `parsers/` - type-specific parser implementations and factory
- `utils/` - shared utilities for regex and time handling

## Usage

Run the application with:

```bash
python main.py
```
