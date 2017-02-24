import xml.etree.ElementTree as ET
tree = ET.parse('actuator.xml')
root = tree.getroot()
print root
print root[0]
print root[0].tag
print root[1].attrib
print root[1].attrib.get('name')
print root[1][0]
print root[1][0][0]
print root[1][0][0].attrib