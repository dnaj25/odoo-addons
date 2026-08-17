import 'package:flutter/material';
import 'api_service.dart';
import 'home_page.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    // Replace with your local Odoo server URL or deployment URL
    final api = ApiService(baseUrl: 'http://localhost:8069');

    return MaterialApp(
      title: 'Odoo Mobile Client',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        primarySwatch: Colors.indigo,
        useMaterial3: true,
      ),
      home: HomePage(api: api),
    );
  }
}
