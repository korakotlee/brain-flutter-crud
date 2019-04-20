import os
import sys
import yaml
from pprint import pprint
from korapp import utils
from korapp import kordir

node_param = utils.get_node_param()
os.makedirs('lib/pages', exist_ok=True)
pages = []
for node in node_param['node']['node']:
    page_name = node['@TEXT']
    pages.append(page_name)
for node in node_param['node']['node']:
    page_name = node['@TEXT']
    icon = utils.get_icon(node)
    if icon == 'gohome':
        from page import home
        result = home.gen(page_name, node, pages)
        if result:
            from page import model_row
            model_row.gen(page_name, node)
    elif icon == 'pencil':
        from page import new
        result = new.gen(page_name, node)
    elif icon == 'list':
        from page import view
        result = view.gen(page_name, node)
        # print('gen view')
    elif icon == 'edit':
        from page import edit
        result = edit.gen(page_name, node)
    else:
        from page import blank
        blank.gen(page_name, node)

