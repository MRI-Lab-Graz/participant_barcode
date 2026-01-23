# Participant Barcode Tool

A simple and efficient tool to generate participant information sheets (PDF) containing unique barcodes for study participants.

## 🚀 Quick Start: Web Interface (Recommended)

The easiest way to use this tool is through the graphical web interface.

### 1. Download Standalone Version
You can download the latest standalone executable for your operating system from the **[Releases](https://github.com/MRI-Lab-Graz/participant_barcode/releases)** page.
*   **Windows**: Download `ParticipantBarcodeTool-Windows.exe`
*   **macOS**: Download `ParticipantBarcodeTool-macOS-AppleSilicon`
*   **Linux**: Download `ParticipantBarcodeTool-Linux`

#### 🛡️ Windows Security Warning (Important!)
When running the Windows executable, you may see a "Windows protected your PC" SmartScreen warning. This is normal for unsigned executables. The software is safe and open source.

**To run the application:**
1. Click "More info"
2. Click "Run anyway"

**Why this happens:** Code signing certificates cost $100-400/year. As an open-source academic project, we haven't purchased one yet. You can verify the source code is safe by reviewing it on GitHub or running from source instead.

### 2. Run from Source
If you prefer running the script directly:
1.  **Install dependencies**:
    *   **Windows**: Double-click `install/install.bat`
    *   **macOS/Linux**: Run `bash install/install.sh`
2.  **Start the app**:
    ```bash
    python app.py
    ```
3.  Open your browser at `http://localhost:5000`.

---

## 📖 Using the Web Interface

1.  **Select LaTeX Template**: Choose a template from the dropdown (sourced from `subject_info/`).
2.  **Enter Participant IDs**:
    *   Type or paste IDs directly into the text area (one per line).
    *   **OR** upload a `.txt` file containing the IDs.
3.  **Generate**: Click "Generate PDFs". The tool will:
    *   Create unique Code128 barcodes.
    *   Embed them into the LaTeX template.
    *   Compile them into individual PDFs.
4.  **Download**: Once finished, you can browse and download the generated PDFs directly from the interface.

---

## 🧰 System Requirements

This tool requires **LaTeX** (specifically `pdflatex`) to be installed on your system to generate PDFs.

### Easy Installation (Recommended)

**Windows**: Run `install/install.bat` - it will:
- Install Python dependencies via UV
- Detect if LaTeX is missing
- Offer to automatically install TinyTeX (lightweight, ~100MB)
- TinyTeX is free, open source, and fully compatible

**macOS/Linux**: Run `bash install/install.sh` for automatic setup with UV

### Manual LaTeX Installation

If you prefer manual installation or the automatic installer fails:

*   **Windows**: Install [MiKTeX](https://miktex.org/) (free, open source) **OR** [TinyTeX](https://yihui.org/tinytex/)
*   **macOS**: Install [MacTeX](https://tug.org/mactex/).
*   **Linux**: `sudo apt install texlive-latex-base texlive-fonts-recommended`

<details>
<summary><b>Manual LaTeX Installation for Linux (if apt fails)</b></summary>

1. **Remove existing TeX Live packages**:
   ```bash
   sudo apt remove texlive* --purge
   sudo apt autoremove
   ```
2. **Download & Run Installer**:
   ```bash
   cd /tmp
   wget http://mirror.ctan.org/systems/texlive/tlnet/install-tl-unx.tar.gz
   tar -xzf install-tl-unx.tar.gz
   cd install-tl-*
   sudo ./install-tl
   ```
3. **Add to PATH** (e.g., in `~/.bashrc`):
   ```bash
   export PATH=/usr/local/texlive/2025/bin/x86_64-linux:$PATH
   ```
</details>

---

## 🖥️ Terminal Usage (Advanced)

For users who prefer the command line or want to automate the process:

1.  Add your list of subject IDs to `barcode_list.txt` (one per line).
2.  Run the generation script:
    ```bash
    python gen_subject_pdf.py
    ```
3.  The results will be stored in the `generated_pdfs/` directory.

---

## 🗂️ Project Structure

```
├── app.py                    # Main Flask application
├── gen_subject_pdf.py         # Script for CLI usage
├── pdf_generator.py           # Core logic for PDF generation
├── install/                  # Setup scripts and requirements
├── static/                   # Web interface CSS/Images
├── templates/                # Web interface HTML
├── subject_info/             # LaTeX templates (.tex)
├── barcodes/                 # Generated barcode images (temp)
└── generated_pdfs/           # Output folder for PDFs
```

---

## 📦 Build Executable Locally

If you want to build your own standalone version:

```bash
# Windows
pyinstaller --noconfirm --onefile --windowed --add-data "templates;templates" --add-data "static;static" --add-data "subject_info;subject_info" --name "ParticipantBarcodeTool" app.py

# macOS/Linux
pyinstaller --noconfirm --onefile --windowed --add-data "templates:templates" --add-data "static:static" --add-data "subject_info:subject_info" --name "ParticipantBarcodeTool" app.py
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Third-Party Dependencies
- **Python packages**: Flask (BSD-3-Clause), Waitress (ZPL), python-barcode (MIT), Pillow (HPND)
- **LaTeX**: Requires user-installed LaTeX distribution (MiKTeX/MacTeX/TeX Live) - separate license applies
- All third-party software maintains their respective licenses
