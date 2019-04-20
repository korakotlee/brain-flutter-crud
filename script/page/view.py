import os
# import sys
# import yaml
import stringcase
# from pprint import pprint
from korapp import utils
# from korapp import kordir
from . import page_utils


def gen(page_name, param):
    page_class = utils.class_case(page_name)
    app_param = utils.get_app_param()
    app_name = app_param['app_name']
    try:
        branch = param['node']['@TEXT']
        if branch.startswith('model:'):
            model = branch.split(':')[1]
            model = model.lstrip()
        else:
            model = ''
    except Exception:
        model = ''
    if model == '':
        print("!!! view page require `model: ` branch")
        return
    model_class = utils.class_case(model)
    atts = page_utils.get_model(model)
    out = \
        f'''
{utils.WARNING}
import 'package:flutter/material.dart';
import 'package:{app_name}/models/ccard.dart';
import 'package:{app_name}/models/ccard_db.dart';
import 'package:{app_name}/pages/text_style.dart';

class {page_class}Page extends StatelessWidget {{
  {page_class}Page(this.context, this.{model}, this.editCard);

  final {model_class}DatabaseHelper db = {model_class}DatabaseHelper();
  final BuildContext context;
  final {model_class} {model};
  final Function editCard;
  final double titleWidth = 132.0;

  @override
  Widget build(BuildContext context) {{
    return Scaffold(
      appBar: AppBar(
        title: Text('View {model_class} ${{this.{model}.id}}'),
      ),
      body: Padding(
        child: viewCard(),
        padding: EdgeInsets.only(top: 15.0, left: 10.0, right: 10.0),
      ),
    );
  }}

  Widget viewCard() {{
    return ListView(
      children: <Widget>[
'''
    for att in atts:
        if att['name'] in ['id', 'createdAt']:
            continue
        out += f"        rowItem('{stringcase.titlecase(att['name'])}', this.{model}.{att['name']}),\n"
    out += \
        f'''
        buttons(),
      ],
    );
  }}

  Widget buttons() {{
    return Padding(
      padding: EdgeInsets.only(top: 15.0, bottom: 15.0),
      child: Row(
        children: <Widget>[
          Expanded(
            child: RaisedButton(
              color: Theme.of(context).primaryColorDark,
              textColor: Colors.white,
              child: Text(
                'Edit',
                textScaleFactor: 1.5,
              ),
              onPressed: () {{
                editCard(this.{model});
              }},
            ),
          ),
          Container(
            width: 5.0,
          ),
          Expanded(
            child: RaisedButton(
                color: Colors.red[900],
                textColor: Colors.white,
                child: Text(
                  'Delete',
                  textScaleFactor: 1.5,
                ),
                onPressed: () => delete()),
          ),
        ],
      ),
    );
  }}

  Widget rowItem(label, item) {{
    return Row(children: <Widget>[
      SizedBox(
        width: titleWidth,
        child: Text(
          label,
          style: Style.title,
        ),
      ),
      Expanded(
        child: Text(item.toString(), style: Style.content),
      ),
    ]);
  }}

  void delete() {{
    showDialog(
        context: context,
        builder: (BuildContext context) {{
          return AlertDialog(
            title: Text('WARNING'),
            content: Text('Are you sure you want to delete this record?'),
            actions: <Widget>[
              FlatButton(
                child: Text('Yes'),
                onPressed: () {{
                  db.delete{model_class}(this.{model}.id).then((value) {{
                    Navigator.popUntil(context,
                        ModalRoute.withName(Navigator.defaultRouteName));
                  }});
                }},
              ),
              FlatButton(
                child: Text('Cancel'),
                onPressed: () {{
                  Navigator.of(context).pop();
                }},
              )
            ],
          );
        }});
  }}
}}



'''

    filename = page_name+'.dart'
    dst = os.path.join('lib', 'pages', filename)
    with open(dst, "w") as text_file:
        text_file.write(out)
    return True
