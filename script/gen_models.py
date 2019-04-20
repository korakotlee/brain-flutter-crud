import os
import sys
import stringcase
from korapp import utils

sys.path.insert(0, __file__)
import flutter_utils

# from __file__ import flutter_utils
# from pprint import pprint


def create_file(model_name, attributes):
    model = utils.class_case(model_name)
    out = "class %s {\n" % model
    atts = flutter_utils.get_attribute_list(attributes)
    utils.save_model(model_name, atts)
    for att in atts:
        out += f"  {att['type']} _{att['name']};\n"

    # constructor, has comma delim except the last one
    # out += f"\n  {model}("
    # for att in atts[:-1]:
    #     out += f"this._{att['name']}, "
    # out += f"this._{atts[-1]['name']}"
    # out += ");\n\n"
    # getter

    out += f"\n  {model}();\n"

    for att in atts:
        out += f"  {att['type']} get {att['name']} => _{att['name']};\n"
    out += "\n"
    # setter
    for att in atts:
        out += f"  set {att['name']}({att['type']} {att['name']}) " + "{ "
        out += f"this._{att['name']} = {att['name']}; " + "}\n"
    out += "\n"
    # toMap
    out += "  Map<String, dynamic> toMap() {\n"
    out += "    var map = Map<String, dynamic>();\n"
    out += "    if (id != null) {\n"
    out += "      map['id'] = _id;\n"
    out += "    }\n"
    for att in atts:
        if att['name'] == 'id':
            continue
        out += f"    map['{att['name']}'] = _{att['name']};\n"
    out += "    return map;\n"
    out += "  }\n"
    out += "\n"
    # fromMap
    out += f"  {model}.fromMap( Map<String, dynamic> map) " + "{\n"
    for att in atts:
        out += f"    this._{att['name']} = map['{att['name']}'];\n"
    out += "  }\n}\n"

    # done, output to file
    filename = stringcase.lowercase(model)+'.dart'
    dst = os.path.join('lib','models',filename)
    with open(dst, "w") as text_file:
        text_file.write(out)


# main
node_param = utils.get_node_param()
os.makedirs('lib/models', exist_ok=True)
models = node_param['node']['node']
if type(models) is list:
    for node in models:
        model_name = node['@TEXT']
        create_file(model_name, node['node'])
else:
    # pprint(models)
    model_name = models['@TEXT']
    create_file(model_name, models['node'])

