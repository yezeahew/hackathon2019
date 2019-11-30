from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO

def convert_pdf_to_txt(path_to_file):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams) ## removed codec?
    fp = open(path_to_file, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()

    return text


def search(query, file_name, line=False):
    file = open(file_name, 'r')
    query_words = query.split()
    return_lines = []

    for line in file:
        line = line.split('\n')
        
        if line != '':
            for words in line:
                words = ' '.join(words.split("/"))
                words = ' '.join(words.split('.'))
                words = ' '.join(words.split(')'))
                words = ' '.join(words.split('('))
                words = ' '.join(words.split('$'))
                words = ' '.join(words.split('!'))
                words = ' '.join(words.split('?'))
                words = ' '.join(words.split(':'))
                words = ' '.join(words.split(','))
                words = ' '.join(words.split('-'))
                words = words.split()
                for word in words:
                    for q in query_words:
                        if word.lower() == q.lower():
                            return_lines.append(line[0])
                            break
    if line:
        return return_lines
    return len(return_lines) > 0

