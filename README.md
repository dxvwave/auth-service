
## Auth Service 🚀🔒

This microservice handles authentication for your app using FastAPI, JWT tokens, and a database.

### Features ✨
- 📝 User registration & login
- 🔑 Secure password hashing
- 🛡️ Custom JWT-based authentication
- 🔗 Easy integration with other services

### Quick Start ⚡
1. Install dependencies: `uv sync`
2. Run the service: `just run`
3. Visit `/docs` for interactive API docs

### Configuration ⚙️
Set your secrets and DB settings in `src/core/config.py`.

### How It Works
- Users register and log in via REST endpoints
- Passwords are hashed for security
- Authenticated users receive JWT tokens for access
- Tokens are verified on each request

---
Made for microservice architectures. Feel free to customize and extend! 💡
