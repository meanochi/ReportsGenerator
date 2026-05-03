# Attendance Modifier

Python project that reads scanned attendance PDFs, classifies report type, applies deterministic time transformations, and generates a new PDF in the same general format.

## Architecture (teacher-friendly structure)

```
attendance_modifier/
  src/
    domain/
      enums.py
      exceptions.py
      models.py
    app/
      contracts/
        modifier.py
        parser.py
        pdf_reader.py
        pdf_generator.py
      transformation/
        base_strategy.py
        type_a_strategy.py
        type_b_strategy.py
        validating_decorator.py
        observers.py
        transformation_service.py
      classifier.py
      pipeline.py
      modifier.py
    infra/
      parsers/
        base_parser.py
        type_a_parser.py
        type_b_parser.py
        parser_factory.py
      ocr_reader_impl.py
      pdf_generator_impl.py
  config/
    container.py
    rules.py
  utils/
    regex_helpers.py
    validators.py
    time_utils.py
  tests/
    unit/
    integration/
  main.py
```

There are no parallel legacy layers (`core/interfaces/services/parsers`) anymore. `src/*` is the single source of truth.

## Implemented patterns

- Dependency Injection (`config/container.py`)
- Strategy (`src/app/transformation/type_*_strategy.py`)
- Decorator (`src/app/transformation/validating_decorator.py`)
- Observer (`src/app/transformation/observers.py`)
- Registry (`src/infra/parsers/parser_factory.py`)
- Template Method (`src/infra/parsers/base_parser.py`)

## Requirements

- Python 3.10+
- Tesseract OCR + Poppler installed in the runtime environment
- Python dependencies from `requirements.txt`

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run

Basic:

```bash
python main.py -i path/to/input.pdf
```

Custom output:

```bash
python main.py -i path/to/input.pdf -o path/to/output.pdf
```

Optional deterministic seed set:

```bash
python main.py -i path/to/input.pdf --seed teamA
```

Get CLI help:

```bash
python main.py --help
```

## Test

```bash
pytest -q -c pytest.ini
```

Current status after migration: all tests pass.

## Docker

- Multi-stage Dockerfile included
- `.dockerignore` included
- Runtime image installs OCR system packages (`tesseract`, `poppler`)

Build:

```bash
docker build -t attendance-modifier .
```

Run:

```bash
docker run --rm -v /local/path:/data attendance-modifier -i /data/input.pdf -o /data/output.pdf
```
