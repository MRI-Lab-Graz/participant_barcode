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

    # Read LaTeX template with explicit UTF-8 encoding for cross-platform compatibility
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()

    # Calculate relative path from output_dir to barcode_dir
    # This is needed because the template might have ../barcodes/ or ../../barcodes/
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
            
            # Use ABSOLUTE paths for barcode - more reliable with pdflatex
            # This works cross-platform as we normalize to forward slashes
            abs_barcode_path = os.path.abspath(os.path.join(barcode_dir, f'barcode_{uid}.png'))
            abs_barcode_path = abs_barcode_path.replace('\\', '/')
            
            # Replace barcode path patterns with absolute path
            tex_content = tex_content.replace('../barcodes/barcode_<<ID>>.png', abs_barcode_path)
            tex_content = tex_content.replace('../../barcodes/barcode_<<ID>>.png', abs_barcode_path)
            
            # Replace relative image paths with absolute paths
            template_dir = os.path.dirname(os.path.abspath(template_path))
            # Go up two levels: from latex/de/ or latex/en/ to subject_info/
            subject_info_dir = os.path.dirname(os.path.dirname(template_dir))
            # Normalize path for LaTeX (always use forward slashes)
            subject_info_dir = subject_info_dir.replace('\\', '/')
            
            # Replace the relative paths with absolute paths
            tex_content = tex_content.replace('../../psychologo.png', subject_info_dir + '/psychologo.png')
            tex_content = tex_content.replace('../../mrilab.png', subject_info_dir + '/mrilab.png')
            tex_content = tex_content.replace('../../unigrazlogo.png', subject_info_dir + '/unigrazlogo.png')

            # Save .tex file with explicit encoding and Unix line endings for LaTeX compatibility
            tex_filename = os.path.join(output_dir, f'sub-{uid}.tex')
            with open(tex_filename, 'w', encoding='utf-8', newline='\n') as tex_file:
                tex_file.write(tex_content)

            # Compile LaTeX to PDF
            env = os.environ.copy()
            sep = ';' if os.name == 'nt' else ':'
            env['TEXINPUTS'] = f".{sep}{env.get('TEXINPUTS', '')}"

            result = subprocess.run([
                'pdflatex',
                '-interaction=nonstopmode',
                '-output-directory', output_dir,
                tex_filename
            ], capture_output=True, env=env)

            # Check if PDF was actually created (pdflatex can return non-zero even on success with warnings)
            pdf_path = os.path.join(output_dir, f'sub-{uid}.pdf')
            if not os.path.exists(pdf_path):
                error_msg = result.stderr.decode('utf-8', errors='ignore') if result.stderr else 'PDF generation failed'
                raise Exception(f"PDF not created: {error_msg[:200]}")

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
