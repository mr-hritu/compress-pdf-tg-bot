import os
from telegram.ext import Updater, CommandHandler
from PyPDF2 import PdfReader, PdfWriter

# Define the handler function for the /compress command
def compress_pdf(update, context):
    # Get the document file from the user
    document = context.bot.get_file(update.message.document.file_id)
    file_name = os.path.splitext(update.message.document.file_name)[0]

    # Download the document file
    document.download(f'{file_name}.pdf')

    # Compress the <link>PDF</link> file
    input_pdf = PdfReader(f'{file_name}.pdf')
    output_pdf = PdfWriter()

    for page in input_pdf.pages:
        page.compress_content_streams()
        output_pdf.add_page(page)

    # Save the compressed <link>PDF</link> file
    output_pdf.write(f'{file_name}_compressed.pdf')

    # Send the compressed <link>PDF</link> file back to the user
    context.bot.send_document(chat_id=update.message.chat_id, document=open(f'{file_name}_compressed.pdf', 'rb'))

    # Clean up temporary files
    os.remove(f'{file_name}.pdf')
    os.remove(f'{file_name}_compressed.pdf')

# Create an instance of the <link>Updater</link> class
updater = Updater('6660071929:AAH6JvMfr3uNEEOVkR1YTZq7c5tPrx-Jc64', use_context=True)

# Get the dispatcher to register handlers
dispatcher = updater.dispatcher

# Register the /compress command handler
dispatcher.add_handler(CommandHandler('compress', compress_pdf))

# Start the bot
updater.start_polling()