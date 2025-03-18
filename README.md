# Flutter Backend Template

A robust, scalable Python backend template designed for Flutter applications with built-in AI capabilities.

## Features

- **FastAPI Backend**: High-performance, easy-to-use, fully async API framework
- **Authentication**: JWT-based authentication with role-based access control
- **Database Integration**: Async SQLAlchemy with support for multiple databases (PostgreSQL, MySQL, SQLite)
- **AI Capabilities**: 
  - OpenAI integration for LLM features
  - Support for custom models (Hugging Face, etc.)
  - Statistical analysis tools
- **Flutter-Ready**: CORS configured for Flutter web and mobile apps
- **Vite Integration**: Ready to connect with Vite-based frontends
- **Scalable Architecture**: Modular design with clear separation of concerns

## Quick Start

### Prerequisites

- Python 3.8+
- Pip package manager

### Installation

1. Clone the repository

```bash
git clone https://github.com/yourusername/flutter-backend-template.git
cd flutter-backend-template
```

2. Create a virtual environment

```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory

```
SECRET_KEY=your_secret_key_here
DATABASE_URL=sqlite:///./app.db
OPENAI_API_KEY=your_openai_api_key_here
```

5. Start the server

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.

## API Documentation

Once the server is running, you can access the automatically generated API documentation:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Project Structure

```
.
├── app/                    # Application package
│   ├── ai/                 # AI modules
│   │   ├── llm/            # Large Language Models integration
│   │   ├── custom_models/  # Custom ML models
│   │   └── statistical/    # Statistical models
│   ├── api/                # API endpoints
│   │   └── v1/             # API version 1
│   ├── core/               # Core functionality
│   ├── db/                 # Database modules
│   ├── models/             # Database models
│   ├── schemas/            # Pydantic schemas
│   ├── services/           # Business logic
│   └── utils/              # Utility functions
├── config/                 # Configuration files
├── tests/                  # Test modules
├── .env                    # Environment variables (create this)
├── main.py                 # Application entry point
└── requirements.txt        # Project dependencies
```

## API Usage Examples

### Authentication

#### Register a new user

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","username":"testuser","password":"password123","full_name":"Test User"}'
```

#### Get an access token

```bash
curl -X POST "http://localhost:8000/api/v1/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=password123"
```

### Using AI Features

#### Get available AI models

```bash
curl -X GET "http://localhost:8000/api/v1/ai/models" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

#### Generate chat completion

```bash
curl -X POST "http://localhost:8000/api/v1/ai/chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "messages": [
      {"role": "system", "content": "You are a helpful assistant"},
      {"role": "user", "content": "Hello, who are you?"}
    ],
    "model": "gpt-3.5-turbo",
    "temperature": 0.7,
    "max_tokens": 150
  }'
```

## Connecting with Flutter

1. Add the `http` package to your Flutter project:

```bash
flutter pub add http
```

2. Make API calls from your Flutter app:

```dart
import 'dart:convert';
import 'package:http/http.dart' as http;

Future<String> getAccessToken(String username, String password) async {
  final response = await http.post(
    Uri.parse('http://localhost:8000/api/v1/auth/token'),
    headers: {'Content-Type': 'application/x-www-form-urlencoded'},
    body: {
      'username': username,
      'password': password,
    },
  );

  if (response.statusCode == 200) {
    final data = json.decode(response.body);
    return data['access_token'];
  } else {
    throw Exception('Failed to get token');
  }
}
```

## Integrating with Vite Frontend

1. Ensure CORS is properly configured (already done in template)
2. Use API calls from your Vite-based frontend:

```javascript
async function login(username, password) {
  const formData = new FormData();
  formData.append('username', username);
  formData.append('password', password);
  
  const response = await fetch('http://localhost:8000/api/v1/auth/token', {
    method: 'POST',
    body: formData,
  });
  
  if (response.ok) {
    const data = await response.json();
    return data.access_token;
  } else {
    throw new Error('Failed to login');
  }
}
```

## Database Management

### Using Different Databases

By default, the template uses SQLite. To use other databases:

1. Uncomment the appropriate driver in `requirements.txt` and install it:
```bash
# For PostgreSQL
pip install psycopg2-binary

# For MySQL
pip install pymysql
```

2. Update your `.env` file with the correct database URL:
```
# PostgreSQL
DATABASE_URL=postgresql://user:password@localhost/dbname

# MySQL
DATABASE_URL=mysql+pymysql://user:password@localhost/dbname
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.