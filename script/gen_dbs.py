import os
import sys
import stringcase
from korapp import utils

sys.path.insert(0, __file__)
import flutter_utils


def create_file(model_name, attributes):
    app_param = utils.get_app_param()
    app_name = app_param['app_name']
    model = utils.class_case(model_name)
    model_file = stringcase.lowercase(model_name)
    model_var = stringcase.lowercase(model[0])+model[1:]
    atts = flutter_utils.get_attribute_list(attributes)
    out = \
f'''
import 'package:sqflite/sqflite.dart';
import 'dart:async';
import 'dart:io';
import 'package:path_provider/path_provider.dart';
import 'package:{app_name}/models/{model_file}.dart';

class {model}DatabaseHelper {{
  static {model}DatabaseHelper _databaseHelper;
  static Database _database;

  String table{model} = '{model_file}';
'''
    for att in atts:
        out += f"  String col{utils.class_case(att['name'])} = '{att['name']}';\n"
    out += \
f'''
  {model}DatabaseHelper._createInstance();

  factory {model}DatabaseHelper() {{
    if (_databaseHelper == null) {{
      _databaseHelper = {model}DatabaseHelper._createInstance();
    }}
    return _databaseHelper;
  }}

  Future<Database> get database async {{
    if (_database == null) {{
      _database = await init();
    }}
    return _database;
  }}

  Future<Database> init() async {{
    Directory dir = await getApplicationDocumentsDirectory();
    String path = dir.path + '{app_name}.db';
    var db = await openDatabase(path, version: 1, onCreate: _createDatabase);
    return db;
  }}

  void _createDatabase(Database db, int version) async {{
    await db.execute('CREATE TABLE $table{model}('
      '$colId INTEGER PRIMARY KEY AUTOINCREMENT, '
'''
    db_types = {
        'string': 'TEXT',
        'int': 'INTEGER',
        'bool': 'INTEGER',
        'double': 'REAL'
    }
    for att in atts[:-1]:
        att_name = utils.class_case(att['name'])
        if att_name == 'Id':
            continue
        out += f"      '$col{att_name} {db_types[att['type'].lower()]}, '\n"
    att = atts[-1]
    out += f"      '$col{utils.class_case(att['name'])} {db_types[att['type'].lower()]} ) '\n"
    out += "    );\n"
    out += \
f'''
  }}

  Future<{model}> get{model}(int id) async {{
    Database db = await this.database;
    var result = await db.query(table{model}, where: '$colId = ?',
      whereArgs: [id]);
    return {model}.fromMap(result[0]);
  }}

  Future<List<Map<String, dynamic>>> get{model}s() async {{
    Database db = await this.database;
    var result = await db.query(table{model});
    return result;
  }}

  Future<int> insert{model}({model} {model_var}) async {{
    Database db = await this.database;
    var result = await db.insert(table{model}, {model_var}.toMap());
    return result;
  }}

  Future<int> update{model}({model} {model_var}) async {{
    Database db = await this.database;
    var result = await db.update(table{model}, {model_var}.toMap(), where: '$colId = ?',
      whereArgs: [{model_var}.id]);
    return result;
  }}

  Future<int> delete{model}(int id) async {{
    Database db = await this.database;
    int result = await db.delete(table{model}, where: '$colId = ?',
      whereArgs: [id]);
    return result;
  }}

  Future<int> getCount() async {{
    Database db = await this.database;
    List<Map<String, dynamic>> x = await db.rawQuery('SELECT COUNT(*) FROM $table{model}');
    int result = Sqflite.firstIntValue(x);
    return result;
  }}

  Future<List<{model}>> get{model}List() async {{

  var {model_var}MapList = await get{model}s();
  int count = {model_var}MapList.length;

  List<{model}> {model_var}List = List<{model}>();
  for (int i = 0; i < count; i++) {{
    {model_var}List.add({model}.fromMap({model_var}MapList[i]));
  }}

  return {model_var}List;
}}


}}
'''

    # done, output to file
    filename = stringcase.lowercase(model)+'_db.dart'
    dst = os.path.join('lib','models',filename)
    with open(dst, "w") as text_file:
        text_file.write(out)


# main
node_param = utils.get_node_param()
os.makedirs('lib/models', exist_ok=True)

models = node_param['node']['node']
if type(models) is list:
    # multiple models
    for node in models:
        model_name = node['@TEXT']
        create_file(model_name, node['node'])
else:
    # single model
    model_name = models['@TEXT']
    create_file(model_name, models['node'])

