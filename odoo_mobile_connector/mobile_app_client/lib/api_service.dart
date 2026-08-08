import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  final String baseUrl;
  String? sessionId;

  ApiService({required this.baseUrl});

  Future<Map<String, dynamic>> _post(String path, Map<String, dynamic> params) async {
    final url = Uri.parse('$baseUrl$path');
    final headers = {
      'Content-Type': 'application/json',
      if (sessionId != null) 'Cookie': 'session_id=$sessionId',
    };

    final body = jsonEncode({
      'jsonrpc': '2.0',
      'method': 'call',
      'params': params,
    });

    try {
      final response = await http.post(url, headers: headers, body: body);
      if (response.statusCode == 200) {
        final decoded = jsonDecode(response.body);
        if (decoded['error'] != null) {
          return {'status': 'error', 'message': decoded['error']['message']};
        }
        return decoded['result'] ?? {'status': 'success'};
      } else {
        return {'status': 'error', 'message': 'HTTP Error: ${response.statusCode}'};
      }
    } catch (e) {
      return {'status': 'error', 'message': e.toString()};
    }
  }

  // Auth: Login
  Future<Map<String, dynamic>> login(String login, String password) async {
    final res = await _post('/mobile/api/v1/auth/login', {
      'login': login,
      'password': password,
    });
    if (res['status'] == 'success') {
      sessionId = res['session_id'];
    }
    return res;
  }

  // Get Homepage Data (Banners & Featured Products)
  Future<Map<String, dynamic>> getHomepage() async {
    return await _post('/mobile/api/v1/homepage', {});
  }

  // Get Products
  Future<Map<String, dynamic>> getProducts({String? categoryId, String? search}) async {
    return await _post('/mobile/api/v1/products', {
      if (categoryId != null) 'category_id': categoryId,
      if (search != null) 'search': search,
    });
  }

  // Add to or get Cart
  Future<Map<String, dynamic>> updateCart({int? productId, int? qty}) async {
    return await _post('/mobile/api/v1/cart', {
      if (productId != null) 'product_id': productId,
      if (qty != null) 'add_qty': qty,
    });
  }
}
