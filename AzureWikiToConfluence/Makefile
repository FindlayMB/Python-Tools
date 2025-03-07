
# Used to make the markdown files ready to upload with mark
.PHONY: prepare
prepare: 
	@echo "Preparing markdown files..."
	python3 prepare-markdown.py
	@echo "Finished preparing!"

# Upload prepared markdown files to Confluence
.PHONY: upload
upload:
	@echo "Uploading markdown files..."
	mark -c mark.conf -f "output/**/*.md"
	@echo "Finished uploading!"
