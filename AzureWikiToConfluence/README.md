# Azure To Confluence Migration

Code written to migrate the wiki from Azure DevOps to Confluence

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Python Script

- Please update the constant `SPACE_KEY` to be the key of the space you want the wiki pages to be upload to.
- Then run the script, all the modified wiki pages will be stored in the output directory

## Tools

### Mark

- To upload the markdown files to Confluence we use a tool called [mark](https://github.com/kovetskiy/mark)
- Please follow the setups in their [GitHub](https://github.com/kovetskiy/mark) to install mark.

## Steps

1. Run the bash script `clone-wiki.sh` to clone the Azure DevOps wiki.

   - Might have to run `chmod +x clone-wiki.sh`
   - Make sure that you have your Azure Git credentials setup, otherwise the repo can't be cloned

2. Update the python script with the correct space key

   - `SPACE_KEY`: line 5, fix-markdown.py

3. Run the python script: `make format`

4. Update the mark.conf

   - Add your `username` (i.e. your Confluence email)
   - Add your `password`, which should be your Confluence API token
   - Add `base-url`: which is your Confluence wiki url

5. Run mark
   - Use the command: `mark -c mark.conf -f "output/**/*.md"`

## Notes

- If a page has a lot of images there is a chance it will fail to upload to confluence using Mark. As such please upload that page individually to ensure it works.
