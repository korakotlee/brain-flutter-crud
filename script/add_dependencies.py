import os
import sys
from korapp import utils
# import yaml
# print('*** add_dependencies')

packages = '''
  sqflite: any
  path_provider: 0.5.0+1
  intl: ^0.15.7
  font_awesome_flutter: any
  shared_preferences: ^0.4.3

'''
app_name = sys.argv[1]
brain = utils.get_brain(app_name)
src = os.path.join(app_name, 'pubspec.yaml')
# src = 'pubspec.yaml'
pubspec = open(src).read()
index = pubspec.find('dev_dependencies:')
out = pubspec[:index] + packages + pubspec[index:]
with open(src, "w") as text_file:
    text_file.write(out)
