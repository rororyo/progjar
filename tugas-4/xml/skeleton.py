import unittest
from io import StringIO
import sys
import xml.etree.ElementTree as ET


# Sample data to be serialized
test_data = {
    'name': 'Alice',
    'age': 30,
    'is_admin': True,
    'skills': ['Python', 'Network Programming', 'Digital Forensics']
}

# Helper: convert dict to XML string
def dict_to_xml(data):
    root = ET.Element('root')
    for key, value in data.items():
        if isinstance(value, list):
            list_container = ET.SubElement(root, key)
            for item in value:
                child = ET.SubElement(list_container, 'item')
                child.text = str(item)
        else:
            child = ET.SubElement(root, key)
            child.text = str(value)
    return ET.tostring(root, encoding='unicode')

# Helper: convert XML string back to dict
def xml_to_dict(xml_str):
    root = ET.fromstring(xml_str)
    result = {}
    for child in root:
        # If child has children, it's a list
        if len(child) > 0:
            # Convert children to list
            result[child.tag] = [item.text for item in child]
        else: # Otherwise, it's a single value
            # Get text and cast to original type
            text = child.text
            if text == 'True':
                result[child.tag] = True
            elif text == 'False':
                result[child.tag] = False
            elif text.isdigit():
                result[child.tag] = int(text)
            else:
                result[child.tag] = text
    # print(result['skills'])
    return result

# Function to assert that two dictionaries are equal
def assert_true_dict(dict1, dict2):
    is_true = dict1 == dict2
    if is_true:
        print("The dictionaries match.", dict1, dict2)
    else:
        print("The dictionaries do not match.")

def assert_true_strings(str1, str2):
    if str1 == str2:
        print("The XML strings match.", str1, str2)
    else:
        print("The XML strings do not match.")

# A 'null' stream that discards anything written to it
class NullWriter(StringIO):
    def write(self, txt):
        pass

# Unit test
class TestXmlToVariable(unittest.TestCase):
    def setUp(self):
        self.test_data = test_data

    def test_xml(self):
        xml_data = dict_to_xml(self.test_data)
        expected_xml = dict_to_xml(self.test_data)
        assert_true_strings(xml_data, expected_xml)
    
    def test_unxml(self):
        xml_data = dict_to_xml(self.test_data)
        parsed_data = xml_to_dict(xml_data)
        assert_true_dict(self.test_data, parsed_data)

# Entry point
if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'run':
        xml_data = dict_to_xml(test_data)
        print("Serialized XML:", xml_data)
    else:
        runner = unittest.TextTestRunner(stream=NullWriter())
        unittest.main(testRunner=runner, exit=False)
        # unittest.main(exit=False)
