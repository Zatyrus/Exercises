## a script to format publication names to be useable as filenames
# make  bashable script

import argparse

# add parser for command line arguments
parser = argparse.ArgumentParser(description="Format publication names to be safe for use as filenames.")
parser.add_argument(
    "-n", "--name", type=str, required=True, help="Publication name to format."
)

def format_publication_name(pub_name: str) -> str:
    """
    Format a publication name to be safe for use as a filename.
    
    Args:
        pub_name (str): The original publication name.
        
    Returns:
        str: The formatted publication name. 
    """
    
    # Replace spaces with underscores
    formatted_name = pub_name.replace(" ", "_")
    
    # Remove characters that are not allowed in filenames
    invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    for char in invalid_chars:
        formatted_name = formatted_name.replace(char, "")
    
    # Truncate the name if it's too long (e.g., more than 255 characters)
    max_length = 255
    if len(formatted_name) > max_length:
        formatted_name = formatted_name[:max_length]
    
    return formatted_name

if __name__ == "__main__":
    args = parser.parse_args()
    formatted_name = format_publication_name(args.name)
    print(formatted_name)