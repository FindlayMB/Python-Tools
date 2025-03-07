import re
import os

# REQUIRED: Set Space Key
SPACE_KEY = ""
# REQUIRED: Directory of the wiki that you cloned
INPUT_DIR = ""

OUTPUT_DIR = "output/"

# This is the initial relative path to the attachments
ATTACHMENT_DIR = f"../{INPUT_DIR}/.attachments"

URL_MAP = {"%2D": "-", "%3A": ":", "%3F": "<", "%3C": "?", "%3E": ">"}


def replace_url_map(input_str: str):
    """Remove any URL Mapping Characters from a string"""
    output_str = input_str
    for key, value in URL_MAP.items():
        output_str = output_str.replace(key, value)
    return output_str


def clean_file_content(file_content: str, attachment_path: str):
    """Clean up file content that will break mark and add some tags for mark"""
    # Make sure attachments are relative paths
    file_content = file_content.replace(".attachments", attachment_path)

    # Remove all excess paths in the inter-page link leaving only the name of the page
    # Ignore links that reference .attachments, the Graveyard, or the Archive
    file_content = re.sub(
        r"(\[[^\]]+\]\()\/(?!((\.\.\/)*\.attachments|Graveyard|Archive)\/)[^\)]*\/([^\/)]*\)?)\)(?!\/)",
        r"\1<ac:\4>)",
        file_content,
    )

    # Remove any excess escape characters and add <ac: > around the page name
    file_content = re.sub(
        r"(<ac:[^\\]*)(\\)([^\\]*)\\([^\\<]*>\))", r"\1\3\4", file_content
    )

    # Replace Azure table of sub pages with pagetree context for mark
    file_content = file_content.replace("[[_TOSP_]]", "<!-- Include: ac:pagetree -->")

    # Replace Azure table of contents with toc context for mark
    file_content = file_content.replace("[[_TOC_]]", "<!-- Include: ac:toc -->")

    # Replace %2D and %3A in the inter-page names
    file_content = re.sub(r"(<ac:[^>]*)(%2D)", r"\1-", file_content)
    file_content = re.sub(r"(<ac:[^>]*)(%3A)", r"\1:", file_content)

    return file_content


def add_mark_tags(
    input_dir: str, filename: str, parent_page: str, attachment_path: str
):
    """"""
    with open(input_dir + filename, "r", encoding="utf-8") as md_file:
        file_content = md_file.read()

    input_dir = input_dir.replace(INPUT_DIR, ".")

    if not os.path.exists(OUTPUT_DIR + input_dir):
        os.makedirs(OUTPUT_DIR + input_dir)

    # Clean page names
    page_name = replace_url_map(filename)
    parent_page_name = replace_url_map(parent_page)

    # Clean and add tags for mark
    file_content = clean_file_content(file_content, attachment_path)

    with open(OUTPUT_DIR + input_dir + filename, "w", encoding="utf-8") as output_file:
        output_file.write(f"<!-- Space: {SPACE_KEY} -->\n")
        if parent_page_name != "":
            output_file.write(f"<!-- Parent: {parent_page_name} -->\n")
        output_file.write(f"<!-- title: {page_name.replace('.md', '')} -->\n\n\n")
        output_file.write(file_content)

    print(f"Prepared {filename} for Confluence")


def search_files(input_dir: str, parent_page: str, attachment_path: str):
    """Start of the recursive method to find markdown files to convert"""
    directory = os.fsencode(input_dir)
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        # Ignore Graveyard
        if (
            filename == "Graveyard.md" or not filename.endswith(".md")
        ):
            continue

        add_mark_tags(input_dir, filename, parent_page, attachment_path)
        new_input_dir = f'{input_dir}/{filename.replace(".md", "")}/'

        if os.path.exists(new_input_dir):
            if not os.path.exists(OUTPUT_DIR + new_input_dir):
                os.makedirs(OUTPUT_DIR + new_input_dir)
            search_files(
                new_input_dir, filename.replace(".md", ""), "../" + attachment_path
            )


def main():
    search_files(INPUT_DIR+"/", "", ATTACHMENT_DIR)


if __name__ == "__main__":
    main()
