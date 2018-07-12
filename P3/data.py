import csv
import codecs
import pprint
import re
import xml.etree.cElementTree as ET

import cerberus

import schema


OSM_PATH = "data.osm"

NODES_PATH = "nodes.csv"
NODE_TAGS_PATH = "nodes_tags.csv"
WAYS_PATH = "ways.csv"
WAY_NODES_PATH = "ways_nodes.csv"
WAY_TAGS_PATH = "ways_tags.csv"

LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBLEM_CHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

SCHEMA = schema.schema

NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']


def shape_element(element, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS,
                  problem_chars=PROBLEM_CHARS, default_tag_type='regular'):
    """Clean and shape node or way XML element to Python dict"""

    node_attributes = {}
    way_attributes = {}
    way_nodes = []
    tags = []  # Handle secondary tags the same way for both node and way elements

    # YOUR CODE HERE
    if element.tag == 'node':
        for field in node_attr_fields:
            node_attributes[field] = element.get(field)
        for tag in element.findall('tag'):
            dictionary = {}
            key = tag.attrib['k']
            pattern = problem_chars.search(key)
            if pattern is not None:
                continue
            colon = key.find(':')
            if colon != -1:
                dictionary['key'] = key[colon + 1:]
                dictionary['type'] = key[:colon]
            else:
                dictionary['key'] = key
                dictionary['type'] = default_tag_type
            dictionary['value'] = tag.attrib['v']
            dictionary['id'] = element.attrib['id']
            tags.append(dictionary)
        return {'node': node_attributes, 'node_tags': tags}
    elif element.tag == 'way':
        for field in way_attr_fields:
            way_attributes[field] = element.get(field)
        for tag in element.findall('tag'):
            dictionary = {}
            key = tag.attrib['k']
            pattern = problem_chars.search(key)
            if pattern is not None:
                continue
            colon = key.find(':')
            if colon != -1:
                dictionary['key'] = key[colon + 1:]
                dictionary['type'] = key[:colon]
            else:
                dictionary['key'] = key
                dictionary['type'] = default_tag_type
            dictionary['value'] = tag.attrib['v']
            dictionary['id'] = element.attrib['id']
            tags.append(dictionary)
        nodes = element.findall('nd')
        for i in range(len(nodes)):
            dictionary = {'id': element.attrib['id'], 'node_id': nodes[i].get('ref'), 'position': i}
            way_nodes.append(dictionary)
        return {'way': way_attributes, 'way_nodes': way_nodes, 'way_tags': tags}


# ================================================== #
#               Helper Functions                     #
# ================================================== #
def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag"""

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


def validate_element(element, validator, s=SCHEMA):
    """Raise ValidationError if element does not match schema"""
    it = iter(validator.errors.items())
    if validator.validate(element, s) is not True:
        try:
            field, errors = next(it)
            message_string = "\nElement of type '{0}' has the following errors:\n{1}"
            error_string = pprint.pformat(errors)

            raise Exception(message_string.format(field, error_string))
        except StopIteration:
            pass


class UnicodeDictWriter(csv.DictWriter, object):
    """Extend csv.DictWriter to handle Unicode input"""

    def writerow(self, row):
        super(UnicodeDictWriter, self).writerow({
            k: v for k, v in row.items()
        })

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


def update(string, mapping):
    words = string.split()
    for w in range(len(words)):
        if words[w] in mapping:
            words[w] = mapping[words[w]]
    name = " ".join(words)
    return name



# ================================================== #
#               Main Function                        #
# ================================================== #
def process_map(file_in, validate):
    """Iteratively process each XML element and write to csv(s)"""

    with codecs.open(NODES_PATH, 'w') as nodes_file, \
            codecs.open(NODE_TAGS_PATH, 'w') as nodes_tags_file, \
            codecs.open(WAYS_PATH, 'w') as ways_file, \
            codecs.open(WAY_NODES_PATH, 'w') as way_nodes_file, \
            codecs.open(WAY_TAGS_PATH, 'w') as way_tags_file:

        nodes_writer = UnicodeDictWriter(nodes_file, NODE_FIELDS)
        node_tags_writer = UnicodeDictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
        ways_writer = UnicodeDictWriter(ways_file, WAY_FIELDS)
        way_nodes_writer = UnicodeDictWriter(way_nodes_file, WAY_NODES_FIELDS)
        way_tags_writer = UnicodeDictWriter(way_tags_file, WAY_TAGS_FIELDS)

        nodes_writer.writeheader()
        node_tags_writer.writeheader()
        ways_writer.writeheader()
        way_nodes_writer.writeheader()
        way_tags_writer.writeheader()

        validator = cerberus.Validator()

        for element in get_element(file_in, tags=('node', 'way')):
            el = shape_element(element)
            if el:
                if validate is True:
                    validate_element(el, validator)
                if element.tag == 'node':
                    nodes_writer.writerow(el['node'])
                    node_tags_writer.writerows(el['node_tags'])
                elif element.tag == 'way':
                    ways_writer.writerow(el['way'])
                    way_nodes_writer.writerows(el['way_nodes'])
                    way_tags_writer.writerows(el['way_tags'])


if __name__ == '__main__':
    # Note: Validation is ~ 10X slower. For the project consider using a small
    # sample of the map when validating.
    process_map(OSM_PATH, validate=False)
