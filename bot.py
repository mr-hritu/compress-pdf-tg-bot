import telebot
from PyPDF2 import PdfReader

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot = telebot.TeleBot('YOUR_BOT_TOKEN')

@bot.message_handler(content_types=['document'])
def handle_document(message):
    # Download the PDF file
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    # Compress the PDF file
    compressed_file = compress_pdf(downloaded_file)

    # Send the compressed PDF file back to the user
    bot.send_document(message.chat.id, compressed_file)

def compress_pdf(file):
    # Create a PDF reader object
    pdf = PdfReader(file)

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
    compressed_file = open('compressed.pdf', 'wb')

    # Write the compressed PDF to the file
    pdf_writer.write(compressed_file)

    # Close the file
    compressed_file.close()

    # Return the path to the compressed PDF file
    return 'compressed.pdf'

# Start the bot
bot.polling()