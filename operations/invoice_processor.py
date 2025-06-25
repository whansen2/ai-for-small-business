"""
Invoice Processor using OCR (pytesseract) for images and PDFs in data/invoices/
Extracts Vendor, Date, Total Amount and writes output to structured CSV.
"""
import pytesseract
from pdf2image import convert_from_path
import os
import re
from typing import List, Dict
from utils.file_io import write_csv

def extract_fields(text: str) -> Dict[str, str]:
    """Extract vendor, date, and total amount from invoice text."""
    vendor = re.search(r"Vendor: ([\w\s]+)", text)
    date = re.search(r"Date: ([\d-]+)", text)
    total = re.search(r"Total Amount: \$?([\d,\.]+)", text)
    return {
        "vendor": vendor.group(1).strip() if vendor else "",
        "date": date.group(1).strip() if date else "",
        "total_amount": total.group(1).strip() if total else ""
    }

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
