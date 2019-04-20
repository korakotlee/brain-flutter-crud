import os
import sys
import yaml
from pprint import pprint
from korapp import utils
from korapp import kordir

def gen(page_name, param):
    # pprint(param)
    src = os.path.join(kordir.template, 'page.dart')
    code = open(src).read()
    result = code.replace("{{page_name}}", utils.class_case(page_name))
    filename = page_name+'.dart'
    dst = os.path.join('lib','pages',filename)
    with open(dst, "w") as text_file:
        text_file.write(result)
