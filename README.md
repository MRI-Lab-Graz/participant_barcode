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

#### If Linux installation fails
##### 🔧 Manual Installation of TeX Live 2025

1. **Remove existing TeX Live packages (optional but recommended)**

```
sudo apt remove texlive* --purge
sudo apt autoremove
```

1. **Download the TeX Live installer**

```
cd /tmp
wget http://mirror.ctan.org/systems/texlive/tlnet/install-tl-unx.tar.gz
tar -xzf install-tl-unx.tar.gz
cd install-tl-*
```

1. **Run the installer**

```
sudo ./install-tl
```

This launches a **text-based GUI** installer. You can:

- Press `I` to install using default settings.
- It will install to `/usr/local/texlive/2025` by default.

> 💡 This may take a while (~2–4GB download).

1. **Add TeX Live binaries to your PATH**

Add this to your `~/.bashrc`, `~/.zshrc`, or equivalent:

```
export PATH=/usr/local/texlive/2025/bin/x86_64-linux:$PATH
```

Then reload your shell:

```
source ~/.bashrc  # or ~/.zshrc
```

1. **Verify installation**

```
pdflatex --version
```

You should see **TeX Live 2025** in the output.

------

### 🛠 Tip: Use `tlmgr` to manage packages

Once installed, you can update and manage LaTeX packages with:

```
sudo tlmgr update --self --all
```

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
