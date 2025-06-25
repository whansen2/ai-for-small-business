"""
Invoice Processor using OCR (pytesseract) for images and PDFs in data/invoices/
Extracts Vendor, Date, Total Amount and writes output to structured CSV.
"""
import pytesseract
from pdf2image import convert_from_path
import os
import re
from typing import Dict
from utils.file_io import write_csv

def extract_fields(text: str) -> Dict[str, str]:
    """Extract vendor, date, and total amount from invoice text using robust line-by-line parsing. Preserves original formatting."""
    fields = {"vendor": "", "date": "", "total_amount": ""}
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        # Case-insensitive and flexible matching
        if line.lower().startswith("vendor"):
            parts = line.split(":", 1)
            if len(parts) > 1:
                fields["vendor"] = parts[1].strip()
        elif line.lower().startswith("date"):
            parts = line.split(":", 1)
            if len(parts) > 1:
                fields["date"] = parts[1].strip()
        elif "total amount" in line.lower():
            parts = line.split(":", 1)
            if len(parts) > 1:
                # Remove $ only, preserve commas and decimals
                value = parts[1].replace("$", "").strip()
                fields["total_amount"] = value
    return fields

def process_invoice_file(filepath: str) -> Dict[str, str]:
    """Process a single invoice file (image, PDF, or text)."""
    ext = os.path.splitext(filepath)[1].lower()
    text = ""
    if ext in [".png", ".jpg", ".jpeg"]:
        text = pytesseract.image_to_string(filepath)
    elif ext == ".pdf":
        images = convert_from_path(filepath)
        for img in images:
            text += pytesseract.image_to_string(img)
    elif ext == ".txt":
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()
    else:
        raise ValueError(f"Unsupported file type: {ext}")
    return extract_fields(text)

def process_invoices(input_dir: str, output_csv: str) -> None:
    """Process all invoice files in a directory and write results to CSV."""
    results = []
    for fname in os.listdir(input_dir):
        if fname.lower().endswith((".png", ".jpg", ".jpeg", ".pdf", ".txt")):
            fpath = os.path.join(input_dir, fname)
            fields = process_invoice_file(fpath)
            fields["filename"] = fname
            results.append(fields)
    if results:
        fieldnames = ["filename", "vendor", "date", "total_amount"]
        write_csv(output_csv, results, fieldnames)
        print(f"Processed {len(results)} invoices. Results saved to {output_csv}")
    else:
        print("No invoice files found.")

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Invoice Processor")
    parser.add_argument("--input_dir", type=str, default="data/invoices", help="Directory with invoice files")
    parser.add_argument("--output_csv", type=str, default="invoices_processed.csv", help="Output CSV file")
    args = parser.parse_args()
    process_invoices(args.input_dir, args.output_csv)

if __name__ == "__main__":
    main()
