from pyhtml2pdf import converter
import pdfkit

import http.server
import socketserver

import threading
import time

PORT = 8000
Handler = http.server.SimpleHTTPRequestHandler

def server():
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving on Port: {PORT}")
        httpd.serve_forever()

def save_as_pdf():
    pdfkit.from_url('http://localhost:8000', 'resume1.pdf')

if __name__ == "__main__":
    
    # Starting seperate thread for running the server
    server_thread = threading.Thread(target=server)
    server_thread.daemon = True
    server_thread.start()

    # Server startup delay
    time.sleep(2)

    save_as_pdf()