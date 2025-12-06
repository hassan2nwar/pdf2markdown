# PDF to Markdown Converter

A robust Python utility for converting PDF documents into clean, well-formatted Markdown files. This tool intelligently preserves document structure, including headings, tables, and text formatting, making it ideal for documentation workflows, content migration, and archival purposes.

<p align="center"><img width="820" height="431" alt="image" src="https://github.com/user-attachments/assets/ea0458db-3da1-445f-82fe-934f540770ed" /></p>


## Features

- **Smart Text Extraction**: Utilizes `pdfplumber` for primary extraction with automatic fallback to `PyPDF2` for maximum compatibility
- **Structure Preservation**: Automatically detects and formats headings based on text patterns and formatting cues
- **Table Conversion**: Extracts and converts PDF tables into properly formatted Markdown tables
- **Batch Processing**: Convert multiple PDF files in a single operation
- **Clean Output**: Removes excessive whitespace and applies intelligent formatting rules
- **Error Handling**: Graceful error handling with detailed feedback for troubleshooting

## Installation

### Prerequisites

- Python 3.7 or higher

### Required Dependencies

Install the required packages using pip:

```bash
pip install PyPDF2 pdfplumber markdownify
```

## Usage

### Basic Usage

```python
from pdf_converter import PDFToMarkdownConverter

# Initialize the converter
converter = PDFToMarkdownConverter(output_dir="markdown_output")

# Convert a single PDF
converter.convert_pdf_to_markdown("document.pdf")
```

### Batch Conversion

```python
# Convert multiple PDFs
pdf_files = [
    "document1.pdf",
    "document2.pdf",
    "document3.pdf"
]

results = converter.convert_multiple_pdfs(pdf_files)
```

### Command Line Usage

Simply run the script directly:

```bash
python pdf_converter.py
```

Update the `pdf_files` list in the `main()` function with your PDF file paths.

## How It Works

1. **Text Extraction**: The converter first attempts to extract text using `pdfplumber`, which provides superior layout preservation
2. **Structure Analysis**: Text is analyzed to identify potential headings based on capitalization, length, and punctuation patterns
3. **Table Detection**: Tables are automatically detected and converted to Markdown table format
4. **Formatting**: Text is cleaned and formatted with appropriate Markdown syntax
5. **Output Generation**: Clean Markdown files are saved to the specified output directory

## Output Format

- Each PDF generates a corresponding `.md` file
- Multi-page documents include page separators (`---`)
- Headings are formatted with `##` or `###` based on detected hierarchy
- Tables maintain their structure with proper alignment
- Document title is automatically generated from the PDF filename

## Configuration

### Output Directory

Specify a custom output directory when initializing the converter:

```python
converter = PDFToMarkdownConverter(output_dir="custom_output")
```

### Heading Detection

The converter identifies headings based on:
- All-caps text under 10 words
- Lines ending with colons (under 80 characters)
- Text length and position within the document

## Error Handling

The tool includes comprehensive error handling:
- Automatic fallback from `pdfplumber` to `PyPDF2` if extraction fails
- Detailed error messages for missing files or conversion issues
- Conversion summary report showing success/failure status for each file

## Limitations

- Complex layouts may require manual formatting adjustments
- Scanned PDFs (images) require OCR preprocessing
- Embedded fonts and special characters may not always convert perfectly
- Multi-column layouts may need post-processing

## Use Cases

- Converting technical documentation to Markdown for version control
- Migrating content to static site generators (Jekyll, Hugo, etc.)
- Creating searchable text archives from PDF libraries
- Preparing documents for content management systems
- Generating readable backups of PDF content

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests for:
- Enhanced heading detection algorithms
- Improved table extraction
- Support for additional PDF features
- Performance optimizations

## License

This project is provided as-is for educational and commercial use.

## Acknowledgments

Built with:
- [pdfplumber](https://github.com/jsvine/pdfplumber) - PDF text and table extraction
- [PyPDF2](https://github.com/py-pdf/pypdf2) - Fallback PDF processing
- [markdownify](https://github.com/matthewwithanm/python-markdownify) - HTML to Markdown conversion utilities
