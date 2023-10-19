import os
from pyrogram import Client, filters
from PyPDF2 import PdfReader, PdfWriter

# Replace 'YOUR_API_ID' and 'YOUR_API_HASH' with your Telegram API credentials
app = Client("compress_bot",bot_token="6660071929:AAH6JvMfr3uNEEOVkR1YTZq7c5tPrx-Jc64", api_id=29943901, api_hash="1028f4e64a5ba57ec59f4587feeabc95")

@app.on_message(filters.document)
def handle_document(client, message):
    # Check if the received file is a PDF
    if message.document.mime_type == 'application/pdf':
        # Download the PDF file
        file_name = message.document.file_name
        downloaded_file = client.download_media(message)

        # Save the downloaded file locally
        with open(file_name, 'wb') as f:
            f.write(downloaded_file)

        # Compress the PDF file
        compressed_file_name = 'compressed.pdf'
        compress_pdf(file_name, compressed_file_name)

        # Send the compressed PDF file back to the user
        client.send_document(
            chat_id=message.chat.id,
            document=compressed_file_name,
            caption='Compressed PDF'
        )

        # Clean up the local files
        os.remove(file_name)
        os.remove(compressed_file_name)

def compress_pdf(input_file, output_file):
    pdf_reader = PdfReader(input_file)
    pdf_writer = PdfWriter()

    # Copy each page of the input PDF to the output PDF
    for page in pdf_reader.pages:
        pdf_writer.add_page(page)

    # Compress the output PDF by removing unnecessary objects
    pdf_writer.compress()

    # Save the compressed PDF to the output file
    with open(output_file, 'wb') as f:
        pdf_writer.write(f)

# Start the bot
app.run()