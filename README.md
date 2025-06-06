## ⚙️ Installation & Setup

We recommend using a virtual environment to keep dependencies isolated:

```
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 📦 Required Python Packages

Install the required Python dependencies:

```
pip install python-barcode Pillow
```

### 🧰 System Requirements

Ensure you have a working LaTeX installation with `pdflatex` available in your system's PATH.

- **Linux**: `sudo apt install texlive-latex-base`
- **macOS**: Use MacTeX
- **Windows**: Use [MiKTeX](https://miktex.org/)

------

## 📝 Example `barcode_list.txt`

This file should contain one unique ID per line:

```
P001
P002
P003
P004
```

Save this as `barcode_list.txt` in the root directory of the project.

## 🚀 How to Run

1. Add your list of subject IDs in `barcode_list.txt`, one per line.
2. Run the script:

```
python gen_subject_pdf.py
```

1. Check the `generated_pdfs/` directory for your individual PDFs.

## 🗂️ Project Structure

```
├── barcode_list.txt           # List of IDs, one per line
├── barcodes/                  # Folder where barcode images will be saved
├── generated_pdfs/           # Output folder for generated PDFs
├── subject_info/
│   └── main.tex              # LaTeX template with placeholder <<ID>>
├── gen_subject_pdf.py                 # Main script 
```

------
