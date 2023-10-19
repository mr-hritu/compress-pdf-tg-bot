import os
import PyPDF2
from pyrogram import Client, filters
from pyrogram.types import InputFile

# Create a Pyrogram client
api_id = "29943901"
api_hash = "1028f4e64a5ba57ec59f4587feeabc95"
bot_token = "6660071929:AAH6JvMfr3uNEEOVkR1YTZq7c5tPrx-Jc64"

app = Client("pdf_compressor_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

@app.on_message(filters.document)
def compress_pdf(client, message):
    # Get the PDF file sent by the user
    file_path = client.download_media(message)

    # Compress the PDF file
    output_path = os.path.splitext(file_path)[0] + "_compressed.pdf"
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfFileReader(file)
        pdf_writer = PyPDF2.PdfFileWriter()

        for page_num in range(pdf_reader.numPages):
            page = pdf_reader.getPage(page_num)
            page.compressContentStreams()  # Compress the content of each page
            pdf_writer.addPage(page)

        with open(output_path, 'wb') as output_file:
            pdf_writer.write(output_file)

    # Send the compressed PDF file back to the user
    client.send_document(message.chat.id, document=InputFile(output_path))

    # Remove temporary files
    os.remove(file_path)
    os.remove(output_path)

@app.on_message(filters.command("start"))
def start_command(client, message):
    client.send_message(message.chat.id, "Welcome to the PDF compression bot!")

# Run the bot
app.run()
