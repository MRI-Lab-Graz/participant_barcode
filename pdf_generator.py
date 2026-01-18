import os
import subprocess
from barcode import Code128
from barcode.writer import ImageWriter

def generate_pdfs(codes, template_path, output_dir, barcode_dir='barcodes'):
    """
    Generate PDFs for a list of codes using a LaTeX template.
    """
    # Ensure output dirs exist
    os.makedirs(barcode_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    # Read LaTeX template
    with open(template_path, 'r') as f:
        template = f.read()

    # Calculate relative path from output_dir to barcode_dir
    # This is needed because the template might have ../barcodes/
    # but we might be in a nested output folder.
    rel_barcode_dir = os.path.relpath(barcode_dir, output_dir)
    # Ensure it ends with a slash and uses forward slashes for LaTeX
    rel_barcode_dir = rel_barcode_dir.replace(os.sep, '/')
    if not rel_barcode_dir.endswith('/'):
        rel_barcode_dir += '/'

    results = []
    for uid in codes:
        try:
            # ... (generate barcode PNG)
            barcode_path = os.path.join(barcode_dir, f'barcode_{uid}.png')
            if not os.path.exists(barcode_path):
                barcode = Code128(uid, writer=ImageWriter())
                barcode.save(os.path.join(barcode_dir, f'barcode_{uid}'))

            # Replace ID and update barcode path in template
            tex_content = template.replace('<<ID>>', uid)
            # Replace the ../barcodes/ (or whatever is there) with our calculated path
            # We look for the pattern used in the template: \includegraphics[height=1.5cm]{../barcodes/barcode_<<ID>>.png}
            # Actually, to be safe, let's just replace ../barcodes/
            tex_content = tex_content.replace('../barcodes/', rel_barcode_dir)

            # Save .tex file
            tex_filename = os.path.join(output_dir, f'sub-{uid}.tex')
            with open(tex_filename, 'w') as tex_file:
                tex_file.write(tex_content)

            # Compile LaTeX to PDF
            # Add template directory to TEXINPUTS so it can find images (logo, etc.)
            env = os.environ.copy()
            template_dir = os.path.dirname(os.path.abspath(template_path))
            # In TEXINPUTS, . means current dir, and : is the separator on Unix ( ; on Windows)
            sep = ';' if os.name == 'nt' else ':'
            env['TEXINPUTS'] = f".{sep}{template_dir}{sep}{env.get('TEXINPUTS', '')}"

            subprocess.run([
                'pdflatex',
                '-interaction=nonstopmode',
                '-output-directory', output_dir,
                tex_filename
            ], check=True, capture_output=True, env=env)

            results.append({'id': uid, 'status': 'success'})

            # Clean auxiliary files  
            extensions_to_clean = ['.aux', '.log', '.tex', '.out']
            for ext in extensions_to_clean:
                file_to_remove = os.path.join(output_dir, f'sub-{uid}{ext}')
                if os.path.exists(file_to_remove):
                    os.remove(file_to_remove)
        except Exception as e:
            results.append({'id': uid, 'status': 'error', 'message': str(e)})
    
    return results
