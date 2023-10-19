import os
import telebot
from PyPDF2 import PdfFileReader, PdfFileWriter

# Telegram bot token
TOKEN = '6660071929:AAH6JvMfr3uNEEOVkR1YTZq7c5tPrx-Jc64'

# Initialize the Telegram bot
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(content_types=['document'])
def handle_document(message):
    # Check if the received file is a PDF
    if message.document.mime_type == 'application/pdf':
        # Download the PDF file
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        file_name = message.document.file_name

        # Compress the PDF file
        compressed_file = compress_pdf(downloaded_file, file_name)

        # Send the compressed PDF file back to the user
        bot.send_document(message.chat.id, compressed_file)

        # Clean up the temporary files
        os.remove(downloaded_file)
        os.remove(compressed_file)

def compress_pdf(file_data, file_name):
    # Create a temporary file to store the compressed PDF
    compressed_file_name = 'compressed_' + file_name
    compressed_file_path = '/tmp/' + compressed_file_name

    # Load the PDF file
    pdf = PdfFileReader(file_data)

    # Create a new PDF writer
    pdf_writer = PdfFileWriter()

    # Iterate through each page of the PDF and add it to the writer
    for page_num in range(pdf.getNumPages()):
        page = pdf.getPage(page_num)
        page.compressContentStreams()  # Compress the content streams of the page
        pdf_writer.addPage(page)

    # Save the compressed PDF to the temporary file
    with open(compressed_file_path, 'wb') as output_file:
        pdf_writer.write(output_file)

    return compressed_file_path

# Start the bot
bot.polling()