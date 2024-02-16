from pyhtml2pdf import converter
import pdfkit

# converter.convert('localhost:8000', 'resume.pdf')
pdfkit.from_url('http://localhost:8000', 'resume.pdf')
