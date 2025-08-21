/// Backend API base URL configured via --dart-define.
/// Falls back to the local development server when not provided.
const String baseUrl =
    String.fromEnvironment('BASE_URL', defaultValue: 'http://10.0.2.2:8000');
