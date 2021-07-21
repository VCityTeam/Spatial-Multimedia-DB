import argparse
import lxml.etree as ET

def ParseCommandLine():
    # arg parse
    descr = '''A small utility that extracts all the buildings from a 
               set of CityGML (XML) files, blends them and serializes the
               result in a new CityGML (XML) file.'''
    parser = argparse.ArgumentParser(description=descr)
    parser.add_argument('--input',
                        nargs='+',
                        type=str,
                        help='CityGML input files')
    parser.add_argument('--output',
                        nargs='+',
                        default='output.gml',
                        type=str,
                        help='Resulting file.')
    return parser.parse_args()


def parse_and_simplify(file_path_name):
    parser = ET.XMLParser(remove_comments=True)
    parsed_file = ET.parse(file_path_name, parser)
    # Remove textures coordinates (currently not used by our
    # algorithms)
    # parsed_file.getroot().nsmap['app'] retrieves the namespace from
    # the parsed_file (defined in the root element)
    appearance = parsed_file.find("//app:appearanceMember",
                             namespaces={'app': parsed_file.getroot().nsmap['app']})
    if appearance is not None:
        appearance.getparent().remove(appearance)
    return parsed_file

if __name__ == '__main__':
    cli_args = ParseCommandLine()
    inputs = [ parse_and_simplify(filename)
               for filename in cli_args.input]
    # We recycle the first parsed input to become the output
    output = inputs[0]

    for city_object_member in inputs[1].findall(".//cityObjectMember",
                                                namespaces={None: inputs[1].getroot().nsmap[None]}):
        output.getroot().append(city_object_member)
    output.write(cli_args.output[0])
