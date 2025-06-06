import os
import subprocess
from barcode import Code128
from barcode.writer import ImageWriter

# Paths
barcode_list_file = 'barcode_list.txt'
barcode_dir = 'barcodes'
output_dir = 'generated_pdfs'
template_path = 'subject_info/main.tex'

# Ensure output dirs exist
os.makedirs(barcode_dir, exist_ok=True)
os.makedirs(output_dir, exist_ok=True)

# Read LaTeX template
with open(template_path, 'r') as f:
    template = f.read()

# Read barcode codes from file
with open(barcode_list_file, 'r') as f:
    codes = [line.strip() for line in f if line.strip()]

for uid in codes:
    # Generate barcode PNG if not already exists
    barcode_path = os.path.join(barcode_dir, f'barcode_{uid}.png')
    if not os.path.exists(barcode_path):
        barcode = Code128(uid, writer=ImageWriter())
        barcode.save(os.path.join(barcode_dir, f'barcode_{uid}'))

    # Replace ID in LaTeX template
    tex_content = template.replace('<<ID>>', uid)

    # Save .tex file
    tex_filename = os.path.join(output_dir, f'sub-{uid}.tex')
    with open(tex_filename, 'w') as tex_file:
        tex_file.write(tex_content)

    # Compile LaTeX to PDF
    subprocess.run([
        'pdflatex',
        '-output-directory', output_dir,
        tex_filename
    ], check=True)

    print(f"Generated PDF for ID {uid}")

	# Clean auxiliary files  
    extensions_to_clean = ['.aux', '.log', '.tex', '.out']
    for ext in extensions_to_clean:
        file_to_remove = os.path.join(output_dir, f'sub-{uid}{ext}')
        if os.path.exists(file_to_remove):
            os.remove(file_to_remove)