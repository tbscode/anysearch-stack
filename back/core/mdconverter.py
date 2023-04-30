import os
import mistune
import pdfkit
from datetime import datetime

def convert_markdown(markdown_text: str, output_folder_path: str = '', output_file_name: str = 'report', output_format: str = 'pdf') -> str:
    
    """
    Convert markdown text to either PDF or HTML format.

    Args:
        markdown_text (str): The markdown text to be converted.
        output_folder_path (str): The path to the output folder where the converted file will be saved. Default is an empty string.
        output_file_name (str): The name of the output file. Default is 'report'.
        output_format (str): The desired output format, either 'pdf' or 'html'. Default is 'pdf'.

    Returns:
        str: The absolute path to the converted file.

    Raises:
        ValueError: If the specified output format is invalid.
    """

    html_text = mistune.html(markdown_text)
    timestamp = datetime.now().strftime("%H:%M:%S")
    output_file_path = os.path.join(output_folder_path, os.path.basename(output_file_name) + '_' + str(timestamp))
    if output_format == "pdf":
        pdfkit.from_string(html_text, output_file_path + '.pdf')
        return os.path.abspath(output_file_path + '.pdf')
    elif output_format == "html":
        with open(output_file_path + '.html', 'w') as f:
            f.write(html_text)
            return os.path.abspath(output_file_path + '.html')
    else:
         raise ValueError("Invalid output format. Please choose 'pdf' or 'html'.")
    

if __name__ == "__main__":
    with open("README.md", "r") as f:
        markdown_text = f.read()

    convert_markdown(markdown_text, output_folder_path='')
    convert_markdown(markdown_text,output_format='html', output_folder_path='')