
import os
from pyrogram import Client, filters
from PyPDF2 import PdfReader, PdfWriter

# Replace 'YOUR_API_ID' and 'YOUR_API_HASH' with your Telegram API credentials
app = Client("compress_bot", api_id=29943901, api_hash="1028f4e64a5ba57ec59f4587feeabc95", bot_token="6660071929:AAFjXcut37ti05_AahCG7nvHdKRQDyUuBaI")

# Function to handle documents
@app.on_message(filters.document)
def handle_document(client, message):
    # Download the document
    file_path = client.download_media(message)
    
    # Compress the document
    compressed_file_path = compress_document(file_path)
    
    # Send the compressed document back
    client.send_document(message.chat.id, compressed_file_path)
    
    # Clean up the files
    os.remove(file_path)
    os.remove(compressed_file_path)

def compress_document(file_path):
    # Compress the document using PyPDF2 library
    output_path = file_path.replace(".pdf", "_compressed.pdf")
    with open(file_path, 'rb') as input_file, open(output_path, 'wb') as output_file:
        reader = PdfReader(input_file)
        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)
        writer.set_compression(True)
        writer.write(output_file)
    return output_path

# Start the bot
app.run()