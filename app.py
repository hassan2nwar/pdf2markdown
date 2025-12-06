import os
import re
from pathlib import Path
try:
    import PyPDF2
    import pdfplumber
    from markdownify import markdownify as md
except ImportError:
    print("Required libraries not found. Install them with:")
    print("pip install PyPDF2 pdfplumber markdownify")
    exit(1)


class PDFToMarkdownConverter:
    """Convert PDF files to clean Markdown format."""
    
    def __init__(self, output_dir="markdown_output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def extract_text_with_formatting(self, pdf_path):
        """Extract text from PDF while preserving structure."""
        markdown_content = []
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    # Extract text with layout
                    text = page.extract_text()
                    
                    if text:
                        # Add page separator for multi-page docs
                        if page_num > 1:
                            markdown_content.append("\n---\n")
                        
                        # Process the text to improve markdown formatting
                        processed_text = self.process_text(text)
                        markdown_content.append(processed_text)
                    
                    # Extract tables if present
                    tables = page.extract_tables()
                    if tables:
                        for table in tables:
                            markdown_table = self.convert_table_to_markdown(table)
                            markdown_content.append(markdown_table)
        
        except Exception as e:
            print(f"Error with pdfplumber: {e}")
            # Fallback to PyPDF2
            return self.extract_with_pypdf2(pdf_path)
        
        return "\n\n".join(markdown_content)
    
    def extract_with_pypdf2(self, pdf_path):
        """Fallback method using PyPDF2."""
        markdown_content = []
        
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            for page_num, page in enumerate(pdf_reader.pages, 1):
                text = page.extract_text()
                
                if text:
                    if page_num > 1:
                        markdown_content.append("\n---\n")
                    
                    processed_text = self.process_text(text)
                    markdown_content.append(processed_text)
        
        return "\n\n".join(markdown_content)
    
    def process_text(self, text):
        """Clean and format text for markdown."""
        # Remove excessive whitespace
        text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
        
        # Detect and format headings (lines in ALL CAPS or with specific patterns)
        lines = text.split('\n')
        processed_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Convert potential headings
            if self.is_heading(line):
                # Determine heading level based on length and position
                if len(line) < 50 and line.isupper():
                    line = f"## {line.title()}"
                elif len(line) < 80 and ':' not in line:
                    line = f"### {line}"
            
            processed_lines.append(line)
        
        return '\n\n'.join(processed_lines)
    
    def is_heading(self, line):
        """Determine if a line is likely a heading."""
        # Check for common heading patterns
        if len(line) > 100:
            return False
        
        # All caps and short
        if line.isupper() and len(line.split()) <= 10:
            return True
        
        # Ends with colon (common in headings)
        if line.endswith(':') and len(line) < 80:
            return True
        
        return False
    
    def convert_table_to_markdown(self, table):
        """Convert extracted table to markdown format."""
        if not table or len(table) == 0:
            return ""
        
        markdown_table = []
        
        # Header row
        header = table[0]
        header_row = "| " + " | ".join(str(cell or "") for cell in header) + " |"
        markdown_table.append(header_row)
        
        # Separator
        separator = "|" + "|".join([" --- " for _ in header]) + "|"
        markdown_table.append(separator)
        
        # Data rows
        for row in table[1:]:
            data_row = "| " + " | ".join(str(cell or "") for cell in row) + " |"
            markdown_table.append(data_row)
        
        return "\n" + "\n".join(markdown_table) + "\n"
    
    def convert_pdf_to_markdown(self, pdf_path):
        """Main conversion function."""
        pdf_path = Path(pdf_path)
        
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        print(f"Converting: {pdf_path.name}")
        
        # Extract content
        markdown_content = self.extract_text_with_formatting(pdf_path)
        
        # Create output filename
        output_filename = pdf_path.stem + ".md"
        output_path = self.output_dir / output_filename
        
        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"# {pdf_path.stem}\n\n")
            f.write(markdown_content)
        
        print(f"✓ Created: {output_path}")
        return output_path
    
    def convert_multiple_pdfs(self, pdf_files):
        """Convert multiple PDF files."""
        results = []
        
        for pdf_file in pdf_files:
            try:
                output_path = self.convert_pdf_to_markdown(pdf_file)
                results.append((pdf_file, output_path, "Success"))
            except Exception as e:
                print(f"✗ Error converting {pdf_file}: {e}")
                results.append((pdf_file, None, f"Error: {e}"))
        
        return results


def main():
    """Example usage."""
    # Initialize converter
    converter = PDFToMarkdownConverter(output_dir="markdown_output")
    
    # List your PDF files here
    pdf_files = [
        '/workspaces/pdf2markdown/PDFs/cv.pdf'
    ]
    
    # Check which files exist
    existing_files = [f for f in pdf_files if Path(f).exists()]
    
    if not existing_files:
        print("No PDF files found!")
        print("Please update the pdf_files list with your actual PDF filenames.")
        return
    
    # Convert all PDFs
    print(f"Starting conversion of {len(existing_files)} PDF file(s)...\n")
    results = converter.convert_multiple_pdfs(existing_files)
    
    # Summary
    print("\n" + "="*50)
    print("CONVERSION SUMMARY")
    print("="*50)
    for pdf_file, output_path, status in results:
        print(f"{Path(pdf_file).name}: {status}")


if __name__ == "__main__":
    main()