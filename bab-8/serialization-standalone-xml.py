import xml.etree.ElementTree as ET

data = {
    'person': {
        'name': 'Alice',
        'age': '30',
        'email': 'alice@example.com'
    }
}

# Create the root element
root = ET.Element('root')

# Serialize dictionary into XML
person_elem = ET.SubElement(root, 'person')
for key, value in data['person'].items():
    child = ET.SubElement(person_elem, key)
    child.text = value

# Convert to XML string
tree = ET.ElementTree(root)
tree.write("output.xml")

# Optional: print as string
# xml_str = ET.tostring(root, encoding='unicode')
# print(xml_str)
#or 
ET.dump(root)

#Simple deserialization
tree = ET.parse('output.xml')
root = tree.getroot()

for person in root.findall('person'):
    name = person.find('name').text
    age = person.find('age').text
    email = person.find('email').text
    print(name, age, email)
