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
        print("!!! edit page require `model: ` branch")
        return
    model_class = utils.class_case(model)
    atts = page_utils.get_model(model)
    out = \
        f'''
{utils.WARNING}

import 'package:flutter/material.dart';
import 'package:{app_name}/models/{model}.dart';
import 'package:{app_name}/models/{model}_db.dart';
// import 'package:intl/intl.dart';

class {page_class}Page extends StatefulWidget {{
  {page_class}Page(this.{model});

  final {model_class} {model};

  @override
  State<StatefulWidget> createState() {{
    return _{page_class}Page(this.{model});
  }}
}}

class _{page_class}Page extends State<{page_class}Page> {{
  _{page_class}Page(this.{model});

  {model_class}DatabaseHelper db = {model_class}DatabaseHelper();

  String appBarTitle = "Edit";
  {model_class} {model};
'''
    for att in atts:
        if att['name'] in ['id', 'createdAt']:
            continue
        out += f"  TextEditingController {att['name']}Controller = TextEditingController();\n"
    out += \
        f'''

  @override
  void initState() {{

'''
    for att in atts:
        if att['name'] in ['id', 'createdAt']:
            continue
        if att['type'] == 'String':
            out += f"    {att['name']}Controller.text = {model}.{att['name']};\n"
        else:
            out += f"    {att['name']}Controller.text = {model}.{att['name']}.toString();\n"
    out += \
        f'''
  }}

  @override
  Widget build(BuildContext context) {{

    return WillPopScope(
        onWillPop: () {{
          moveToLastScreen();
        }},
        child: Scaffold(
          appBar: AppBar(
            title: Text(appBarTitle),
            leading: IconButton(
                icon: Icon(Icons.arrow_back),
                onPressed: () {{
                  moveToLastScreen();
                }}),
          ),
          body: Padding(
            padding: EdgeInsets.only(top: 15.0, left: 10.0, right: 10.0),
            child: ListView(
              children: <Widget>[

'''
    keyboard_type = {
        'String': 'text',
        'int': 'number',
        'double': 'number'
    }

    for att in atts:
        if att['name'] in ['id', 'createdAt']:
            continue
        out += f"                rowItem('{stringcase.titlecase(att['name'])}', {att['name']}Controller, '{keyboard_type[att['type']]}'),\n"
    out += \
        f'''
                buttons(),
              ],
            ),
          ),
        ));
  }}

  Widget buttons() {{
    return Padding(
      padding: EdgeInsets.only(top: 15.0, bottom: 15.0),
      child: Row(
        children: <Widget>[
          Expanded(
            child: RaisedButton(
              color: Theme.of(context).primaryColorDark,
              textColor: Theme.of(context).primaryColorLight,
              child: Text(
                'Save',
                textScaleFactor: 1.5,
              ),
              onPressed: () {{
                setState(() {{
                  // debugPrint("Save button clicked");
                  _save();
                }});
              }},
            ),
          ),
          Container(
            width: 5.0,
          ),
          Expanded(
            child: RaisedButton(
              color: Theme.of(context).primaryColorDark,
              textColor: Theme.of(context).primaryColorLight,
              child: Text(
                'Cancel',
                textScaleFactor: 1.5,
              ),
              onPressed: () {{
                setState(() {{
                  Navigator.pop(context, false);
                }});
              }},
            ),
          ),
        ],
      ),
    );
  }}

  Widget rowItem(label, controller, keyboard) {{
    TextStyle textStyle = Theme.of(context).textTheme.title;
    return Padding(
      padding: EdgeInsets.only(top: 15.0, bottom: 15.0),
      child: TextField(
        controller: controller,
        keyboardType: keyboard=='number'
            ? TextInputType.number
            : TextInputType.text,
        onChanged: null,
        style: textStyle,
        decoration: InputDecoration(
            labelText: label,
            labelStyle: textStyle,
            border:
                OutlineInputBorder(borderRadius: BorderRadius.circular(5.0))),
      ),
    );
  }}

  void moveToLastScreen() {{
    Navigator.pop(context, false);
  }}

  void _save() async {{
'''
    for att in atts:
        if att['name'] in ['id', 'createdAt']:
            continue
        if att['type'] == 'String':
            out += f"    {model}.{att['name']} = {att['name']}Controller.text;\n"
        else:
            out += f"    {model}.{att['name']} = {att['type']}.tryParse({att['name']}Controller.text);\n"
    out += \
        f'''

    ccard.createdAt = DateTime.now().toIso8601String();
    await db.updateCcard(ccard);
    Navigator.pop(context, true);
  }}
}}

'''

    filename = page_name+'.dart'
    dst = os.path.join('lib', 'pages', filename)
    with open(dst, "w") as text_file:
        text_file.write(out)
    return True
