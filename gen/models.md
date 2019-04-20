## Models

### Sample

![GitHub Logo](https://github.com/korakotlee/img/raw/master/Screenshot%20from%202019-04-11%2006-14-23.png)

### Description
  Create model file for Flutter app. Specify the model name and attributes as
  `<name>: <attribute>`. if attribute is not specify then the default is String. Do not use `:` in name.
  Model files are under lib/models/ folder.
  Each model will generate 2 files; `lib/models/<name.dart>` for model class file and `lib/models/<name_db.dart>` for database helper file. 
  
### Data Types
  Valid Dart data types are:
  
  - int
  - double
  - String

  Be careful when you change the type of the existing database as there might be some conflict with the existing database.
  