import os
import sys
import yaml
from pprint import pprint
from korapp import utils
from korapp import kordir

def gen(page_name, param):
    page_class = utils.class_case(page_name)
    app_param = utils.get_app_param()
    app_name = app_param['app_name']
    # pprint(pages)
    model = ''
    displays = []
    for node in param['node']:
        if node['@TEXT'].startswith('model:'):
            model = node['@TEXT'].split(':')[1]
            model = model.lstrip()
        if node['@TEXT'].startswith('fab:'):
            fab_page = node['@TEXT'].split(':')[1]
            fab_page = fab_page.lstrip()
        if node['@TEXT'].lower().startswith('onpressed:'):
            onpressed_page = node['@TEXT'].split(':')[1]
            onpressed_page = onpressed_page.lstrip()
        if node['@TEXT'].lower().startswith('display'):
            for display in node['node']:
                displays.append(display['@TEXT'])
    if model == '':
        print("!!! home page require `model: ` branch")
        return
    model_class = utils.class_case(model)
    fab_page_class = utils.class_case(fab_page)
    onpressed_page_class = utils.class_case(onpressed_page)
    out = \
f'''
import 'package:flutter/material.dart';
import 'package:{app_name}/models/ccard.dart';
import 'package:{app_name}/theme.dart' as Theme;

class CardRow extends StatelessWidget {{
  final {model_class} {model};
  final Function viewCard;

  CardRow(this.{model}, this.viewCard);

  @override
  Widget build(BuildContext context) {{
    final {model}Card = new Container(
      margin: const EdgeInsets.only(left: 8.0, right: 8.0),
      decoration: new BoxDecoration(
        color: Theme.Colors.ccardCard,
        shape: BoxShape.rectangle,
        borderRadius: new BorderRadius.circular(8.0),
        boxShadow: <BoxShadow>[
          new BoxShadow(
              color: Colors.black,
              blurRadius: 10.0,
              offset: new Offset(0.0, 10.0))
        ],
      ),
      child: new Container(
        margin: const EdgeInsets.only(top: 16.0, left: 128.0),
        constraints: new BoxConstraints.expand(),
        child: new Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: <Widget>[
'''
    for display in displays:
        out += f"            new Text({model}.{display}, style: Theme.TextStyles.planetTitle),\n"
    out += \
f'''
          ],
        ),
      ),
    );

    return new Container(
      height: 120.0,
      margin: const EdgeInsets.only(top: 16.0, bottom: 8.0),
      child: new FlatButton(
        onPressed: () => viewCard({model}),
        child: new Stack(
          children: <Widget>[
            {model}Card,
          ],
        ),
      ),
    );
  }}

}}
'''

    filename = model+'_row'+'.dart'
    dst = os.path.join('lib','pages',filename)
    with open(dst, "w") as text_file:
        text_file.write(out)
    return True
