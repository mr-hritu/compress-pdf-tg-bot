import telebot
from PyPDF2 import PdfReader, PdfWriter
import tempfile
import os

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot = telebot.TeleBot('6660071929:AAH6JvMfr3uNEEOVkR1YTZq7c5tPrx-Jc64')

@bot.message_handler(content_types=['document'])
def handle_document(message):
    # Download the PDF file
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    # Create a temporary file to save the downloaded file
    temp_file_path = tempfile.mktemp()
    with open(temp_file_path, 'wb') as temp_file:
        temp_file.write(downloaded_file)

    # Compress the PDF file
    compressed_file = compress_pdf(temp_file_path)

    # Send the compressed PDF file back to the user
    bot.send_document(message.chat.id, compressed_file)

def compress_pdf(file_path):
    # Create a PDF reader object
    pdf = PdfReader(file_path)

    # Create a PDF writer object
    pdf_writer = PdfWriter()

    # Iterate through each page of the PDF
    for page_number in range(len(pdf.pages)):
        # Compress the page by reducing the image quality
        page = pdf.pages[page_number]
        page.compressContentStreams()

        # Add the compressed page to the PDF writer
        pdf_writer.add_page(page)

    # Create a new file to store the compressed PDF
    compressed_file_path = tempfile.mktemp(suffix='.pdf')
    with open(compressed_file_path, 'wb') as compressed_file:
        # Write the compressed PDF to the file
        pdf_writer.write(compressed_file)

    # Remove the temporary file
    os.remove(file_path)

    # Return the path to the compressed PDF file
    return compressed_file_path

# Start the bot
bot.polling()