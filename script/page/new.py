import os
import sys
import yaml
import stringcase
from pprint import pprint
from korapp import utils
from korapp import kordir


def get_model(model):
    model_file = os.path.join('.korapp', f'model_{model}.yaml')
    with open(model_file, 'r') as stream:
        result = yaml.load(stream, Loader=yaml.FullLoader)
    return result


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
        print("!!! new page require `model: ` branch")
        return
    model_class = utils.class_case(model)
    atts = get_model(model)
    out = \
        f'''
{utils.WARNING}
import 'package:flutter/material.dart';
import 'package:{app_name}/models/{model}.dart';
import 'package:{app_name}/models/{model}_db.dart';

class {page_class}Page extends StatefulWidget {{
  @override
  State<StatefulWidget> createState() {{
    return _{page_class}Page();
  }}
}}
  
class _{page_class}Page extends State<{page_class}Page> {{
  {model_class}DatabaseHelper db = {model_class}DatabaseHelper();
  {model_class} {model};
'''
    for att in atts:
        if att['name'] in ['id', 'createdAt']:
          continue
        out += f"	TextEditingController {att['name']}Controller = TextEditingController();\n"
    out += \
f'''
  @override
  Widget build(BuildContext context) {{
    TextStyle textStyle = Theme.of(context).textTheme.title;

    return WillPopScope(
      onWillPop: () {{
        // Write some code to control things, when user press Back navigation button in device navigationBar
        moveToLastScreen();
      }},

      child: Scaffold(
      appBar: AppBar(
        title: Text("New {model_class}"),
        leading: IconButton(icon: Icon(
            Icons.arrow_back),
            onPressed: () {{
              // Write some code to control things, when user press back button in AppBar
              moveToLastScreen();
            }}
        ),
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
        out += f"            new InputField(label: '{att['name']}', controller: {att['name']}Controller, keyboard: '{keyboard_type[att['type']]}', textStyle: textStyle),\n"
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
                  debugPrint("Save button clicked");
                  _save();
                }});
              }},
            ),
          ),

          Container(width: 5.0,),

          Expanded(
            child: RaisedButton(
              color: Theme.of(context).primaryColorDark,
              textColor: Theme.of(context).primaryColorLight,
              child: Text(
                'Cancel',
                textScaleFactor: 1.5,
              ),
              onPressed: () => moveToLastScreen()
            ),
          ),

        ],
      ),
    );
  }}

  void moveToLastScreen() {{
    Navigator.pop(context, true);
  }}

  void _save() async {{
    {model_class} {model} = new {model_class}();
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
    {model}.createdAt = DateTime.now().toIso8601String();
    await db.insertCcard({model});
    moveToLastScreen();
  }}

}}

class InputField extends StatelessWidget {{
  const InputField({{
    Key key,
    @required this.label,
    @required this.controller,
    @required this.keyboard,
    @required this.textStyle,
  }}) : super(key: key);

  final String label;
  final TextEditingController controller;
  final String keyboard;
  final TextStyle textStyle;


  @override
  Widget build(BuildContext context) {{
    return Padding(
        padding: EdgeInsets.only(top: 15.0, bottom: 15.0),
        child: TextField(
            controller: controller,
            keyboardType: keyboard=='number'
              ? TextInputType.number
              : TextInputType.text,
            style: textStyle,
            decoration: InputDecoration(
                labelText: label,
                labelStyle: textStyle,
                border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(5.0)
                )
            ),
        ),
    );
  }}
}}

'''

    filename = page_name+'.dart'
    dst = os.path.join('lib', 'pages', filename)
    with open(dst, "w") as text_file:
        text_file.write(out)
    return True
