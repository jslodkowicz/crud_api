# Simple Users CRUD API (FastAPI & JSON)

This is a minimal FastAPI application implementing a basic CRUD API for managing users. User data is stored in a file `users.json` (no external database required).

## Setup

1. **Clone this repository**
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   
3. **Create (if missing) an empty users.json file:**
 
json
   []
   
4. **Run the app**
 
bash
   uvicorn src.main:app --reload
   
5. The API will be available at [http://localhost:8000](http://localhost:8000)

## API Endpoints

| Method | Path          | Description        | Body Example (JSON)                                         | Response         |
|--------|---------------|-------------------|-------------------------------------------------------------|------------------|
| POST   | /users        | Create user       | { "name": "John Doe", "email": "john@example.com" }       | Created user     |
| GET    | /users        | List all users    | —                                                           | List of users    |
| GET    | /users/{id}   | Get single user   | —                                                           | The user         |
| PUT    | /users/{id}   | Update user       | { "name": "New Name", "email": "new@email.com" }          | Updated user     |
| DELETE | /users/{id}   | Delete user       | —                                                           | —                |
- All endpoints return JSON responses.
- Default port: 8000
- OpenAPI/docs UI: [http://localhost:8000/docs](http://localhost:8000/docs)

## Example: Create User

bash
curl -X POST "http://localhost:8000/users" \
     -H "Content-Type: application/json" \
     -d '{"name": "Alice", "email": "alice@email.com"}'

## Notes

- Users are stored as a JSON list in users.json. The file is created/updated automatically.
- On development/start, ensure the file exists and contains a valid JSON array [].
- After change, restart the server if you encounter issues.
