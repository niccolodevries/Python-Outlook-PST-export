import pypff
import os
import uuid
import filetype


# Function to extract email messages and attachments from a PST file
def extract_emails_and_attachments_from_pst(pst_file_path, output_dir):
    # Open the PST file
    pst_file = pypff.file()
    pst_file.open(pst_file_path)

    # Get the root folder
    root_folder = pst_file.get_root_folder()

    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Directory to save all extracted attachments
    all_attachments_dir = os.path.join(output_dir, "all_attachments")
    if not os.path.exists(all_attachments_dir):
        os.makedirs(all_attachments_dir)

    # Process the root folder
    process_folder(root_folder, output_dir, all_attachments_dir)

    # Close the PST file
    pst_file.close()


# Recursive function to process folders and extract emails and attachments
def process_folder(folder, output_dir, all_attachments_dir):
    # Process subfolders
    for subfolder in folder.sub_folders:
        subfolder_name = subfolder.name
        subfolder_path = os.path.join(output_dir, subfolder_name)
        if not os.path.exists(subfolder_path):
            os.makedirs(subfolder_path)
        process_folder(subfolder, subfolder_path, all_attachments_dir)

    # Process emails
    for message in folder.sub_messages:
        extract_email(message, output_dir, all_attachments_dir)


# Function to extract and save an email message and its attachments
def extract_email(message, output_dir, all_attachments_dir):
    # Extract message details with checks
    subject = message.subject if hasattr(message, 'subject') and message.subject else "No Subject"
    sender = message.sender_name if hasattr(message, 'sender_name') and message.sender_name else "No Sender"
    recipients = message.recipients if hasattr(message, 'recipients') else None
    recipient_names = ', '.join([recipient.name for recipient in recipients]) if recipients else "No Recipients"

    # Create a directory for this email
    email_dir = os.path.join(output_dir, subject.replace('/', '_').replace('\\', '_'))
    if not os.path.exists(email_dir):
        os.makedirs(email_dir)

    # Save the email body
    if hasattr(message, 'plain_text_body') and message.plain_text_body:
        body = message.plain_text_body.decode('utf-8', errors='ignore')
        body_file_path = os.path.join(email_dir, "body.txt")
    elif hasattr(message, 'html_body') and message.html_body:
        body = message.html_body.decode('utf-8', errors='ignore')
        body_file_path = os.path.join(email_dir, "body.html")
    elif hasattr(message, 'rtf_body') and message.rtf_body:
        body = message.rtf_body.decode('utf-8', errors='ignore')
        body_file_path = os.path.join(email_dir, "body.rtf")
    else:
        body = "No Body"
        body_file_path = os.path.join(email_dir, "body.txt")

    with open(body_file_path, 'w', encoding='utf-8') as f:
        f.write(body)

    # Save email metadata
    metadata_file_path = os.path.join(email_dir, "metadata.txt")
    with open(metadata_file_path, 'w', encoding='utf-8') as f:
        f.write(f"Subject: {subject}\n")
        f.write(f"Sender: {sender}\n")
        f.write(f"Recipients: {recipient_names}\n")

    # Save attachments
    try:
        if hasattr(message, 'attachments'):
            attachments_dir = os.path.join(email_dir, "attachments")
            if not os.path.exists(attachments_dir):
                os.makedirs(attachments_dir)
            for attachment in message.attachments:
                save_attachment(attachment, attachments_dir, all_attachments_dir, subject)
    except Exception as e:
        print(f"Error processing attachments for email '{subject}': {e}")


# Function to save an attachment
def save_attachment(attachment, email_attachments_dir, all_attachments_dir, subject):
    try:
        attachment_size = attachment.get_size()
        if attachment_size > 0:
            attachment_data = attachment.read_buffer(attachment_size)

            # Retrieve the original filename or use the email subject + unique identifier
            try:
                attachment_name = (attachment.get_long_filename() or
                                   attachment.get_short_filename())
            except Exception:
                attachment_name = None

            if not attachment_name:
                attachment_name = f"{subject.replace('/', '_').replace('\\', '_')}_{uuid.uuid4()}"

            # Ensure the attachment name is valid
            attachment_name = os.path.basename(attachment_name)

            # Guess the MIME type and use it to determine the file extension if missing
            kind = filetype.guess(attachment_data)
            extension = f".{kind.extension}" if kind and not attachment_name.endswith(f".{kind.extension}") else ''

            attachment_filename = attachment_name + extension

            # Save the attachment in the email's attachments directory
            attachment_path = os.path.join(email_attachments_dir, attachment_filename)
            with open(attachment_path, 'wb') as f:
                f.write(attachment_data)

            # Save the attachment in the global attachments directory
            global_attachment_path = os.path.join(all_attachments_dir, attachment_filename)
            with open(global_attachment_path, 'wb') as f:
                f.write(attachment_data)
        else:
            print(f"Attachment has invalid size: {attachment_size}")
    except Exception as e:
        print(f"Error processing attachment: {e}")


# Path to your PST file
pst_file_path = "file.pst"

# Directory to save the extracted emails and attachments
output_dir = "extracted_emails_and_attachments"

# Extract emails and attachments
extract_emails_and_attachments_from_pst(pst_file_path, output_dir)