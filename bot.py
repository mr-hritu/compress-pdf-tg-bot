import os
from pyrogram import Client, filters
from PyPDF2 import PdfFileWriter, PdfFileReader

app = Client("compress_bot", bot_token="6660071929:AAH6JvMfr3uNEEOVkR1YTZq7c5tPrx-Jc64")

@app.on_message(filters.command("compress"))
def compress_pdf(client, message):
    # Download the PDF file
    file_info = message.document
    file_path = client.download_media(file_info)
    
    # Compress the PDF file
    input_pdf = PdfFileReader(file_path)
    output_pdf = PdfFileWriter()
    
    # Iterate through each page of the PDF file
    for page_num in range(input_pdf.getNumPages()):
        page = input_pdf.getPage(page_num)
        page.compressContentStreams()  # Compress the content streams of the page
        output_pdf.addPage(page)
    
    # Save the compressed PDF file
    output_path = "compressed.pdf"
    with open(output_path, 'wb') as output_file:
        output_pdf.write(output_file)
    
    # Send the compressed PDF file back to the user
    client.send_document(message.chat.id, output_path)
    
    # Delete the temporary files
    os.remove(file_path)
    os.remove(output_path)

app.run()