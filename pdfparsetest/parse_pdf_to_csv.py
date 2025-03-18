import pdfplumber
import re

# Opening the PDF file to extract data
with pdfplumber.open("data.PDF") as pdf:

    # Extract text from each page
    pages = []
    for page in pdf.pages:
        pages.append(page.extract_text())

    data = []

    # Combine two pages into one, as this dataset relies on two pages for each data entry
    page_num = 0
    while page_num < len(pages):
        data.append(pages[page_num] + pages[page_num + 1])
        page_num += 2

    # Write the data to a CSV file    
    text_file = open("Output.csv", "w")
    text_file.write("Analysis,Method,Result,Unit\n")

    for line in data:
        line = line.splitlines()

        # Remove the header and footer of the pdf, to only keep the data
        line = line[12:]
        x1 = line[:29]
        x2 = line[45:68]
        # Combine the two pages of pure data, no header or footer
        line = x1 + x2 

        # Remove the specific parts of the line
        del line[17]
        del line[47]

        # Remove the specific part "(as sum of Glucose, Fructose," as it is causing problems in the regex logic
        line[46] = re.sub(r"\(as sum of Glucose, Fructose,", "", line[46]).strip()

        # Regex pattern to do the computation
        pattern = re.compile(r"^(.+?)\s+([A-Z0-9\-&\(\) .]+?)\s+([<>]?\d*\.?\d*|---)\s*([\w%/]+)?$")

        # Check if the pattern matches the line
        for y in line:
            match = pattern.match(y)
            if match:
                nutrient, method, value, unit = match.groups()
                text_file.write(nutrient + "," + method + "," + value + "," + unit + "\n")
            else:
                print(f"Could not parse line: {y}")

    
    text_file.close()