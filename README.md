# PST Email and Attachment Extractor

This script extracts emails and attachments from a PST file. The emails are saved in individual folders with their body, metadata, and attachments. Additionally, all attachments are saved in a separate global directory.

## Requirements

- Python 3.x
- pypff
- filetype

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/pst-email-attachment-extractor.git
    cd pst-email-attachment-extractor
    ```

2. Install the required libraries:
    ```bash
    pip install pypff filetype
    ```

## Usage

1. Place your PST file in the project directory and rename it to `file.pst` or update the `pst_file_path` variable in the script to match your file name.

2. Run the script:
    ```bash
    python extract_emails_and_attachments.py
    ```

3. The extracted emails and attachments will be saved in the `extracted_emails_and_attachments` directory.

## Script Details

The script performs the following tasks:
1. Opens the PST file and retrieves the root folder.
2. Processes each folder recursively to extract emails and their attachments.
3. Saves each email in a directory named after the email's subject.
4. Saves the email body in plain text, HTML, or RTF format.
5. Saves the email metadata (subject, sender, recipients) in a text file.
6. Saves attachments in both the email's directory and a global `all_attachments` directory.

## Example

Here is an example structure of the output directory:

extracted_emails_and_attachments/
├── all_attachments/
│ ├── attachment_1.pdf
│ ├── attachment_2.jpg
│ └── ...
├── Email_Subject_1/
│ ├── body.txt
│ ├── metadata.txt
│ └── attachments/
│ ├── attachment_1.pdf
│ └── ...
├── Email_Subject_2/
│ ├── body.html
│ ├── metadata.txt
│ └── attachments/
│ ├── attachment_2.jpg
│ └── ...
└── ...

## License

This project is licensed under the MIT License.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss your ideas.
