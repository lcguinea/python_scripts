import subprocess

def compress_pdf(input_pdf_path, output_pdf_path):
    # Ghostscript command for PDF compression
    gs_command = [
        'gs',
        '-sDEVICE=pdfwrite',
        '-dCompatibilityLevel=1.4',
        '-dPDFSETTINGS=/screen',
        '-dNOPAUSE',
        '-dQUIET',
        '-dBATCH',
        f'-sOutputFile={output_pdf_path}',
        input_pdf_path
    ]

    # Run the Ghostscript command
    subprocess.run(gs_command, check=True)

# Example usage with absolute paths
input_pdf_path = '/Users/luisguinea/Downloads/REINICIA FESTIVAL.pdf'
output_pdf_path = '/Users/luisguinea/Downloads/REINICIA FESTIVAL_compressed.pdf'

compress_pdf(input_pdf_path, output_pdf_path)