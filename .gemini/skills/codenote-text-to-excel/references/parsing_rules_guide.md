# Parsing Rules Guide for Text-to-Excel Skill

This document explains how to define parsing rules for the `text-to-excel` skill to extract specific data from your input text and map it to an Excel spreadsheet. Since the structure of text extracted from PDFs can vary widely, defining clear parsing rules is crucial.

The `text_to_excel.py` script currently contains placeholder logic. To make it truly useful, you will need to enhance the `parse_text_to_excel` function in `scripts/text_to_excel.py` with specific logic tailored to your document types.

## General Approach

The parsing typically involves:
1.  **Identifying Data Points**: Using keywords, regular expressions, or positional information to locate the data you need (e.g., "Invoice Number:", "Total Amount:", "Date:").
2.  **Extracting Values**: Capturing the actual values associated with those data points.
3.  **Mapping to Excel**: Deciding which Excel cell (e.g., "A1", "B5") or range the extracted value should be placed into.

## Techniques for Data Extraction

### 1. Keyword-based Extraction

Useful for finding values immediately following a specific label.

**Example (Python implementation concept):**

```python
# In scripts/text_to_excel.py, within parse_text_to_excel function
invoice_number_match = re.search(r'Invoice Number:\s*(\S+)', text_content)
if invoice_number_match:
    sheet['B2'] = invoice_number_match.group(1)

total_amount_match = re.search(r'(Total Amount|合計金額):\s*([\d,\.]+)', text_content, re.IGNORECASE)
if total_amount_match:
    # Assuming the extracted value might need conversion to float
    sheet['C5'] = float(total_amount_match.group(2).replace(',', ''))
```

### 2. Regular Expressions (Regex)

Powerful for pattern matching, especially when data is not strictly tied to a keyword or has a specific format (e.g., dates, phone numbers, email addresses).

**Example (Python implementation concept):**

```python
# In scripts/text_to_excel.py
date_match = re.search(r'Date:\s*(\d{4}[-/]\d{2}[-/]\d{2})', text_content)
if date_match:
    sheet['A1'] = date_match.group(1)

# Extract all email addresses
email_addresses = re.findall(r'[\w\.-]+@[\w\.-]+', text_content)
for i, email in enumerate(email_addresses):
    sheet[f'F{i+1}'] = email
```

### 3. Line-by-Line Processing

For structured text where each line might represent a record or a specific piece of information.

**Example (Python implementation concept):**

```python
# In scripts/text_to_excel.py
for i, line in enumerate(text_content.splitlines()):
    if "Item Code:" in line:
        # Process line to extract item code and other details
        # For instance, split by space or tab
        parts = line.split()
        if len(parts) > 2:
            sheet[f'A{row_counter}'] = parts[2] # Example: Item Code
            # Increment row_counter and process other details
            row_counter += 1
```

## How to Apply Parsing Rules

1.  **Inspect Your Text Output**: Use the `pdf-to-text` skill to get sample text outputs from your specific forms/documents. Analyze their structure.
2.  **Identify Key Data**: Determine exactly what pieces of information you need to extract.
3.  **Develop Regex/Keywords**: Write regular expressions or identify keywords that reliably find your data points.
4.  **Modify `scripts/text_to_excel.py`**:
    *   Open `scripts/text_to_excel.py` for editing.
    *   Locate the `parse_text_to_excel` function.
    *   Add your custom parsing logic within the placeholder section (or create a new function for complex parsing).
    *   Ensure the extracted values are written to the correct cells in the `sheet` object.

## Example Scenario: Invoice Document

Imagine your PDF text output contains:

```
Invoice Number: INV-2023-001
Customer: John Doe
Date: 2023-10-26
---------------------------
Item: Laptop      Qty: 1   Price: 1200.00
Item: Mouse       Qty: 2   Price: 50.00
---------------------------
Subtotal: 1250.00
Tax (8%): 100.00
Total: 1350.00
```

Your `scripts/text_to_excel.py` might be extended with:

```python
# ... inside parse_text_to_excel function ...

# Header information
invoice_num = re.search(r'Invoice Number:\s*(\S+)', text_content)
if invoice_num: sheet['B1'] = invoice_num.group(1)

customer = re.search(r'Customer:\s*(.+)', text_content)
if customer: sheet['B2'] = customer.group(1)

date = re.search(r'Date:\s*(\d{4}-\d{2}-\d{2})', text_content)
if date: sheet['B3'] = date.group(1)

# Line items (more complex, might need multi-line regex or line-by-line processing)
# For simplicity, let's assume we can get total from here
total = re.search(r'Total:\s*([\d\.]+)', text_content)
if total: sheet['B7'] = float(total.group(1))

# ... rest of the script ...
```

Remember to import any necessary modules (like `re` for regular expressions) at the top of your script.
