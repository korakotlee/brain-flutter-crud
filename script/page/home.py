import os
import sys
import yaml
from pprint import pprint
from korapp import utils
from korapp import kordir

def gen(page_name, param, pages):
    page_class = utils.class_case(page_name)
    app_param = utils.get_app_param()
    app_name = app_param['app_name']
    # pprint(pages)
    model = ''
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
    if model == '':
        print("!!! home page require `model: ` branch")
        return False
    model_class = utils.class_case(model)
    fab_page_class = utils.class_case(fab_page)
    onpressed_page_class = utils.class_case(onpressed_page)
    out = \
f'''
import 'package:flutter/material.dart';
import 'package:sqflite/sqflite.dart';
import 'package:{app_name}/theme.dart' as Theme;
import 'package:{app_name}/models/ccard.dart';
import 'package:{app_name}/models/{model}_db.dart';
import 'package:{app_name}/pages/{model}_row.dart';
'''
    for page in pages:
        if page != 'home':
            out += f"import 'package:{app_name}/pages/{page}.dart';\n"
    out += \
f'''

class {page_class}Page extends StatefulWidget {{
  {page_class}Page({{Key key, this.title}}) : super(key: key);
  final String title;

  @override
  _{page_class}Page createState() => _{page_class}Page();
}}

class _{page_class}Page extends State<{page_class}Page> {{
  BuildContext context;
  {model_class}DatabaseHelper dbHelper = {model_class}DatabaseHelper();
  List<{model_class}> {model}s;
  int count = 0;

  void updateCardView() {{
    final Future<Database> dbFuture = dbHelper.init();
    dbFuture.then((database) {{
      Future<List<{model_class}>> listFuture = dbHelper.get{model_class}List();
      listFuture.then(({model}s) {{
        setState(() {{
          this.{model}s = {model}s;
          this.count = {model}s.length;
        }});
      }});
    }});
  }}

  void _new() {{
    Navigator.push(
        context,
        MaterialPageRoute(
            builder: (context) =>
                {fab_page_class}Page())).then((value) {{
      setState(() => updateCardView());
    }});
  }}

  void viewCard({model_class} card) {{
    Navigator.push(
            context,
            MaterialPageRoute(
                builder: (context) => {onpressed_page_class}Page(context, card, editCard)))
        .then((value) {{
      setState(() => updateCardView());
    }});
  }}

  void editCard({model_class} card) {{
    Navigator.push(
            context, MaterialPageRoute(builder: (context) => EditPage(card)))
        .then((value) {{
      if (value) {{
        setState(() {{
          updateCardView();
          _showAlertDialog('Status', 'Updated Successfully');
        }});
      }}
    }});
  }}

  void _showAlertDialog(String title, String message) {{
    AlertDialog alertDialog = AlertDialog(
      title: Text(title),
      content: Text(message),
    );
    showDialog(context: context, builder: (_) => alertDialog);
  }}

  @override
  Widget build(BuildContext context) {{
    if ({model}s == null) {{
      {model}s = List<{model_class}>();
      updateCardView();
    }}
    this.context = context;
    return Scaffold(
      appBar: AppBar(
        leading: Icon(Icons.filter_tilt_shift),
        title: Text(widget.title),
      ),
      body: homeBody(),
      backgroundColor: Theme.Colors.planetPageBackground,
      floatingActionButton: FloatingActionButton(
        onPressed: _new,
        tooltip: 'Add new',
        backgroundColor: Theme.Colors.appBarDetailBackground,
        child: Icon(Icons.add),
      ),
    );
  }}

  Widget homeBody() {{
    return ListView.builder(
      itemExtent: 160.0,
      itemCount: this.{model}s.length,
      itemBuilder: (_, index) => new CardRow(this.{model}s[index], viewCard),
    );
  }}
}}

'''

    filename = page_name+'.dart'
    dst = os.path.join('lib','pages',filename)
    with open(dst, "w") as text_file:
        text_file.write(out)
    return True
