import 'package:flutter/material.dart';

class Colors {

  const Colors();


  static const Color appBarTitle = const Color(0xFFFFFFFF);
  static const Color appBarIconColor = const Color(0xFFFFFFFF);
  static const Color appBarDetailBackground = const Color(0xFFf7b600);
  static const Color appBarGradientStart = const Color(0xFF3383FC);
  static const Color appBarGradientEnd = const Color(0xFF00C6FF);

  //static const Color planetCard = const Color(0xFF434273);
  static const Color ccardCard = const Color(0xFFFFFFFF);
  static const Color planetCard = const Color(0xFFFFFFFF);
  // static const Color planetCard = const Color(0xeFF8685E5);
  //static const Color planetListBackground = const Color(0xFF3E3963);
  static const Color planetPageBackground = const Color(0xFF1a1f71);
  // static const Color planetPageBackground = const Color(0xFF736AB7);
  static const Color planetTitle = const Color(0xFF000000);
  static const Color planetLocation = const Color(0xFF000000);
  static const Color planetDistance = const Color(0xFF000000);

}

class Dimens {
  const Dimens();

  static const planetWidth = 100.0;
  static const planetHeight = 100.0;
}

class TextStyles {

  const TextStyles();

  static const TextStyle appBarTitle = const TextStyle(
    color: Colors.appBarTitle,
    fontFamily: 'Poppins',
    fontWeight: FontWeight.w600,
    fontSize: 36.0
  );

  static const TextStyle planetTitle = const TextStyle(
    color: Colors.planetTitle,
    fontFamily: 'Poppins',
    fontWeight: FontWeight.w600,
    fontSize: 24.0
  );

  static const TextStyle planetLocation = const TextStyle(
    color: Colors.planetLocation,
    fontFamily: 'Poppins',
    fontWeight: FontWeight.w300,
    fontSize: 14.0
  );

  static const TextStyle planetDistance = const TextStyle(
    color: Colors.planetDistance,
    fontFamily: 'Poppins',
    fontWeight: FontWeight.w300,
    fontSize: 12.0
  );


}
