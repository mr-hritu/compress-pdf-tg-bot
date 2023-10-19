
import os
import pyrogram
from PyPDF2 import PdfFileWriter, PdfFileReader

# Pyrogram API credentials
API_ID = 29943901
API_HASH = "1028f4e64a5ba57ec59f4587feeabc95"
BOT_TOKEN = "6660071929:AAFjXcut37ti05_AahCG7nvHdKRQDyUuBaI"

# Create a Pyrogram client instance
app = pyrogram.Client("pdf_compressor", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Handler for /start command
@app.on_message(pyrogram.filters.command("start"))
def start_command(client, message):
    client.send_message(message.chat.id, "Welcome! Send me a PDF file to compress.")

# Handler for receiving documents
@app.on_message(pyrogram.filters.document)
def handle_document(client, message):
    # Download the file
    file_path = client.download_media(message.document.file_id, file_name=message.document.file_name)
    
    # Compress the PDF file
    compressed_file_path = compress_pdf(file_path)
    
    # Send the compressed file back to the user
    client.send_document(message.chat.id, compressed_file_path)
    
    # Delete the local files
    os.remove(file_path)
    os.remove(compressed_file_path)

# Function to compress PDF file
def compress_pdf(file_path):
    output_file_path = f"compressed_{os.path.basename(file_path)}"
    with open(file_path, 'rb') as file:
        pdf_reader = PdfFileReader(file)
        pdf_writer = PdfFileWriter()

        # Copy each page and add it to the writer
        for page_num in range(pdf_reader.getNumPages()):
            page = pdf_reader.getPage(page_num)
            pdf_writer.addPage(page)

        # Set compression options
        pdf_writer.setCompressionOptions({
            'compressContentStreams': True,
            'objectCompression': True,
            'compressMetadata': True,
            'imageCompress': True,
            'imageQuality': 50  # Adjust the image quality as needed
        })

        # Write the compressed PDF file
        with open(output_file_path, 'wb') as output_file:
            pdf_writer.write(output_file)
    
    return output_file_path

# Start the client
app.run()