
import os
import PyPDF2
from telegram.ext import Updater, CommandHandler

def compress_pdf(update, context):
    # Get the PDF file sent by the user
    file = context.bot.getFile(update.message.document.file_id)
    file_path = file.download()

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
    context.bot.send_document(chat_id=update.effective_chat.id, document=open(output_path, 'rb'))
    
    # Remove temporary files
    os.remove(file_path)
    os.remove(output_path)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to the PDF compression bot!")

if __name__ == '__main__':
    TOKEN = '6660071929:AAH6JvMfr3uNEEOVkR1YTZq7c5tPrx-Jc64'
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('compress', compress_pdf))

    updater.start_polling()
    updater.idle()