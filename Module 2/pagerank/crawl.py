import sys
import os
import re

pages = dict()
directory = sys.argv[1]

# Extract all links from HTML files
for filename in os.listdir(directory):
    if not filename.endswith(".html"):
        continue
    with open(os.path.join(directory, filename)) as f:
        contents = f.read()
        links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
        print(filename, links)
        pages[filename] = set(links) - {filename}
        print(pages)

# Only include links to other pages in the corpus
for filename in pages:
    pages[filename] = set(
        link for link in pages[filename]
        if link in pages
    )
print("filtered", pages)