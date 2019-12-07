import textract
import xml.etree.ElementTree as ET


def _check_unique_xpath(root, element, previous_xpath):
    """
    @description - Forms list of xpaths with every non-empty attribute
                   Checks if one of these xpaths can be used to uniquely identify given element in tree
    @param [in] root|xml.etree.ElementTree.Element - root element of the given xml tree
    @param [in] element|xml.etree.ElementTree.Element - current element to check for unique Xpaths
    @param [in] previos_xpath|str - Xpath of the prvious element in tree
    @return str or None - unique xpath if any, else None   
    """
    tag_xpath = './/' + element.tag
    skip_list = ['index', 'class']
    check_dict = {attr: value for attr,value in element.attrib.items() if value and attr not in skip_list}
    xpath_candidates = [tag_xpath + '[@{0}="{1}"]'.format(attr, check_dict[attr]) for attr in check_dict]
    for xpath in xpath_candidates:
        if len(root.findall(xpath)) == 1:
            return xpath
    return None


def generate_xpaths(source_file):
    """
    @description - Generate unique Xpaths for the given source xml
                   Attemps to generate Xpath with the use of element attributes
    @param [im] source_file|str - path to PDF source file
    @return list[str] - list of generated Xpaths
    """
    source_string = textract.process(source_file, method='pdfminer').decode('utf-8')
    root = ET.fromstringlist(source_string.splitlines())
    xpaths = []
    prev_xpath = None
    for element in root.iter():
        if prev_xpath:
            unique_xpath = _check_unique_xpath(root, element, prev_xpath)
            if unique_xpath:
                xpath = unique_xpath
            else:
                xpath = prev_xpath + '/' + element.tag
                if element.attrib['index'] != '0':
                    xpath = xpath + '[{}]'.format(element.attrib['index'])
        else:
            xpath = '.'
        xpaths.append(xpath)
        prev_xpath = xpath
    return xpaths

       
if __name__ == '__main__':
    xpaths = generate_xpaths('stringsource.pdf')
    print('\n\n'.join(xpaths))
    print(len(xpaths))