import os
import sys
# import yaml
import shutil
from korapp import utils
# from pprint import pprint
# from korapp import kordir


def copy_sample_main():
    app_param = utils.get_app_param()
    app_name = app_param['app_name']
    brain = utils.get_brain_cwd()
    template = os.path.join(brain, "template")
    src = os.path.join(template, 'main.dart')
    dst = os.path.join('lib', 'main.dart')
    main = open(src).read()
    index = main.find('void main()')
    out = main[:index] + \
        f"import 'package:{app_name}/pages/home.dart';\n" + main[index:]
    with open(dst, "w") as text_file:
        text_file.write(out)
    src = os.path.join(template, 'theme.dart')
    # dst = os.path.join(app_name, 'lib')
    shutil.copy(src, 'lib')
    src = os.path.join(template, 'text_style.dart')
    dst = os.path.join('lib', 'pages')
    os.makedirs(dst, exist_ok=True)
    shutil.copy(src, dst)


copy_sample_main()
