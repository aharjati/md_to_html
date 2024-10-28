### Markdown => HTML converter
This is a CLI application allowing user to convert markdown file into HTML file

## Pre-requisite:
- Python (at least 3.10) installed. The CLI application was tested with Python 3.11

## How to run
- Go to root folder (Same directory as README.md)
- Run "python md_to_html/cli.py convert md_to_html/test1.md md_to_html/test1.html"
- This should generate "md_to_html/test1.html" file

## How to run unit tests
- Go to root folder (Same directory as README.md)
- Run "python -m unittest discover -s tests"
- You should see unit test results
