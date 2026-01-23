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
            
            # Replace relative barcode path with absolute path
            abs_barcode_dir = os.path.abspath(barcode_dir).replace(os.sep, '/')
            tex_content = tex_content.replace('../barcodes/', abs_barcode_dir + '/')
            
            # Replace relative image paths with absolute paths
            subject_info_dir = os.path.dirname(os.path.abspath(template_path))
            subject_info_dir = os.path.dirname(subject_info_dir)  # Go up two levels to subject_info/
            subject_info_dir = subject_info_dir.replace(os.sep, '/')
            
            # Replace the relative paths with absolute paths
            tex_content = tex_content.replace('../../psychologo.png', subject_info_dir + '/psychologo.png')
            tex_content = tex_content.replace('../../mrilab.png', subject_info_dir + '/mrilab.png')
            tex_content = tex_content.replace('../../unigrazlogo.png', subject_info_dir + '/unigrazlogo.png')

            # Save .tex file
            tex_filename = os.path.join(output_dir, f'sub-{uid}.tex')
            with open(tex_filename, 'w') as tex_file:
                tex_file.write(tex_content)

            # Compile LaTeX to PDF
            env = os.environ.copy()
            sep = ';' if os.name == 'nt' else ':'
            env['TEXINPUTS'] = f".{sep}{env.get('TEXINPUTS', '')}"

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
