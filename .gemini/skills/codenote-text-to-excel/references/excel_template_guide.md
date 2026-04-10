# Excel Template Guide for Text-to-Excel Skill

This guide provides instructions on how to prepare an Excel template file for use with the `text-to-excel` skill. Using a pre-formatted template allows you to control the layout, styling, and formulas of your output Excel file, making the data extraction and presentation more consistent and professional.

## Why Use an Excel Template?

-   **Consistent Formatting**: Maintain company branding, specific fonts, colors, and cell styles.
-   **Pre-defined Formulas**: Embed formulas (e.g., sums, averages, lookups) that automatically update when data is inserted.
-   **Structured Layout**: Ensure extracted data lands in specific, intended cells, making the output immediately usable.
-   **Charts and Graphs**: Include pre-configured charts that dynamically update with the imported data.

## How to Prepare Your Template

1.  **Create Your Base Excel File**: Start with a new Excel workbook or an existing one that has the desired layout, sheets, and formatting.
2.  **Define Data Placement**: Decide exactly where the extracted text data should go. For example, if you're extracting an "Invoice Number", you might want it in cell `B2` of "Sheet1".
3.  **Use Meaningful Sheet Names**: If your workbook has multiple sheets, give them descriptive names (e.g., "Invoice Summary", "Line Items", "Analytics") to make it easier to target specific sheets in your parsing logic within `scripts/text_to_excel.py`.
4.  **Avoid Hardcoded Data (for dynamic parts)**: Do not fill in the cells that are meant to receive data from the text parsing. Leave them blank or use placeholder text that your script can overwrite.
5.  **Save as `.xlsx`**: Save your template file in the `.xlsx` format. This is the standard for `openpyxl` and modern Excel files.

## Integrating the Template with `text_to_excel.py`

When running the `text_to_excel.py` script, you will specify your template file using the `--template` argument.

**Example Command:**

```bash
python scripts/text_to_excel.py 
    input.txt 
    output.xlsx 
    --template my_invoice_template.xlsx
```

## Modifying `scripts/text_to_excel.py` for Template Usage

When the `text_to_excel.py` script loads a template, it maintains all existing sheets, formatting, and formulas. Your parsing logic in the script will then need to:

1.  **Select the Correct Sheet**: If your template has multiple sheets, ensure your Python script targets the correct sheet to write data.

    ```python
    # In scripts/text_to_excel.py
    # Select a specific sheet by name
    if 'Invoice Summary' in workbook.sheetnames:
        sheet = workbook['Invoice Summary']
    else:
        # Fallback or error handling if sheet not found
        sheet = workbook.active
    ```

2.  **Write to Specific Cells**: Instead of simply appending data, you will write to the exact cells you've designated in your template.

    ```python
    # Example: Writing extracted data to pre-defined cells
    sheet['B2'] = invoice_number
    sheet['C5'] = total_amount
    ```

By following this guide, you can create robust Excel templates that work seamlessly with your text parsing logic to produce highly customized and professional reports.
