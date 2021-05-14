#from io import StringIO
#
# from pdfminer.converter import TextConverter
# from pdfminer.layout import LAParams
# from pdfminer.pdfdocument import PDFDocument
# from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
# from pdfminer.pdfpage import PDFPage
# from pdfminer.pdfparser import PDFParser
import re
from collections import OrderedDict
#
#    output_string = StringIO()
#    with open('pwk.pdf', 'rb') as in_file:
#        parser = PDFParser(in_file)
#        doc = PDFDocument(parser)
#        rsrcmgr = PDFResourceManager()
#        device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
#        interpreter = PDFPageInterpreter(rsrcmgr, device)
#        for page in PDFPage.create_pages(doc):
#            interpreter.process_page(page)
#
#    with open('PWK-text.txt', 'w') as f:
#        print(output_string.getvalue(), file=f)
#


problems = OrderedDict()
psetName = ""
pset = []
gutter = []

with open('PWK-text.txt', 'r') as f:
    # Iterate over the output of the previously generated text file
    for i in f.readlines():
        # Begin by determining if we have selected an exercise name
        if not psetName:
            # Try to find an exercise
            if re.match(r'^\d{1,2}\.\d{1,2}\.\d{1,2}\.\d{1,2}.*Exercise|Exercises$', i):
                # Begin Problem Set - write out the name
                psetName = i
        else:
            # If it is not a subsection
            if re.match(r'^\d{1,2}\.\d{1,2}.*', i):
                # This indicates we have fully consumed the exercise
                # Append to the dictionary as the exercise ID
                problems[psetName] = pset
                # Blank the accumulator variables
                psetName = ""
                pset = []

            # If it is a numbered list, or the notice indicating reporting is optional
            if re.match(r'^.*Reporting.*', i):
                # Add to the list the numbered item or the reporting optional message
                pset.append(i)
            elif re.match(r'^\d\.\s\s.*', i):
                pset.append(i)
            else:
                #pset.append(i)
                # Remove Page Numbers
                if not re.match(r'^\d{1,2}\s\n', i):
                    # Remove Copyright notice
                    if not re.match(r'^Copyright\s.*', i):
                        # Remove OSID
                        if not re.match(r'^OS\-9898.*', i):
                            # Remove Course Name
                            if not re.match(r'^PWK\s2\.0\s\n$', i):
                                # Remove single newlines
                                if not re.match(r'^\n$', i):
                                    # Remove space single newlines
                                    if not re.match(r'^\s\n$', i):
                                        # Remove kali@kali
                                        if not re.match(r'^kali\@kali.*', i):
                                            pset.append(i)
                                        else:
                                            gutter.append(i)
# Return our ordered problem set
print(problems)
# Return any missing text
print(gutter)
# Return only the list of the exercises
for key, value in problems.items():
    print(key, value)


print(len(problems))

print(problems.keys())

# for key, value in problems.items():
#    with open(key, 'w') as question:
#        for m in value:
#            print(m, file=question)
