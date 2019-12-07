import textract
from lxml import etree


def generate_xpaths(source_file):
    """
    @description - Lazy solution with lxml library.
                   Returns absolute path for every element in xml tree.
    @param [in] source_file|str - path to the pdf file containing xml string.
    @return list[str] - list with every found path
    """
    source_string = textract.process(source_file, method='pdfminer').decode('utf-8')
    root = etree.fromstringlist(source_string.splitlines()).getroottree()
    xpaths = [root.getelementpath(element) for element in root.iter()]
    return xpaths


if __name__ == '__main__':
    xpaths = generate_xpaths('stringsource.pdf')
    print("\n\n".join(xpaths))
    print(len(xpaths))
