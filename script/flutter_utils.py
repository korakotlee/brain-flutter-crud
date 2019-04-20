import stringcase
from korapp import utils


def get_attribute_list(attributes):
    atts = [
        {'name': 'id', 'type': 'int'},
        {'name': 'createdAt', 'type': 'String'}
        ]
    # convert mm data type to Dart data type
    data_types = {
        'String': 'String',
        'Int': 'int',
        'Double': 'double',
        'bool': 'bool'
    }
    for attribute in attributes:
        try:
            aname, atype = attribute['@TEXT'].split(':')
            atype = atype.lstrip()
            atype = stringcase.titlecase(atype)
            atype = data_types[atype]
        except ValueError:
            aname = attribute['@TEXT']
            atype = 'String'
        aname = stringcase.lowercase(aname)
        aname = utils.to_camel_case(aname)
        atts.append({'name': aname, 'type': atype})
    return atts
