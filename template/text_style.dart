import 'package:flutter/material.dart';

class Style {
  static final baseTextStyle = const TextStyle(
    fontFamily: 'Poppins'
  );
  static final content = baseTextStyle.copyWith(
      // color: const Color(0xffb6b2df),
    fontSize: 24.0,
    fontWeight: FontWeight.w400
  );
  static final title = baseTextStyle.copyWith(
      // color: const Color(0xffb6b2df),
    color: Colors.black,
    fontSize: 24.0,
    fontWeight: FontWeight.w600
  );
  static final smallTextStyle = commonTextStyle.copyWith(
    fontSize: 9.0,
  );
  static final commonTextStyle = baseTextStyle.copyWith(
    color: const Color(0xffb6b2df),
    fontSize: 14.0,
    fontWeight: FontWeight.w400
  );
  static final headerTextStyle = baseTextStyle.copyWith(
    color: Colors.white,
    fontSize: 20.0,
    fontWeight: FontWeight.w400
  );
}