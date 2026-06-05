# Walkthrough: Python FastAPI + Prisma Backend Workspace Setup

I have successfully initialized and configured your Python backend workspace inside the `AWD30716-SHARKHUB-BACKEND` directory. The project is fully integrated with your Supabase database and is structured following a clean, decoupled MVC architecture using SOLID principles.

---

## What Was Accomplished

1. **Virtual Environment & Dependencies**:
   - Created a local Python virtual environment (`.venv`).
   - Installed `fastapi`, `uvicorn`, `prisma`, `pydantic`, `pydantic-settings`, and `python-dotenv` via [requirements.txt](file:///C:/Users/andre/Desktop/ESPE/SEMESTRE%205/WEB%20AVANZADO/Group%20Repository/AWD30716-SHARKHUB-BACKEND/requirements.txt).

2. **Supabase Connection**:
   - Created a [.env](file:///C:/Users/andre/Desktop/ESPE/SEMESTRE%205/WEB%20AVANZADO/Group%20Repository/AWD30716-SHARKHUB-BACKEND/.env) file using your Supabase credentials and both database URLs:
     - `DATABASE_URL` (pooled connection on port 6543) for application queries.
     - `DIRECT_URL` (direct session connection on port 5432) for migrations/introspection.

3. **Prisma Schema Configuration**:
   - Configured `previewFeatures = ["multiSchema"]` and `schemas = ["public", "auth"]` in [schema.prisma](file:///C:/Users/andre/Desktop/ESPE/SEMESTRE%205/WEB%20AVANZADO/Group%20Repository/AWD30716-SHARKHUB-BACKEND/prisma/schema.prisma) to handle cross-schema foreign keys pointing to Supabase's `auth.users` table.
   - Enabled experimental decimal support (`enable_experimental_decimal = true`) to handle `Decimal`/`Numeric` columns (e.g., prices of products/services).

4. **Introspection & Generation**:
   - Ran `prisma db pull` to introspect your Supabase tables. 32 models were successfully read and generated in your schema file.
   - Ran `prisma generate` to compile the type-safe Prisma Python Client.

5. **MVC + SOLID Folder Architecture**:
   - Created the folder structure inside the [app/](file:///C:/Users/andre/Desktop/ESPE/SEMESTRE%205/WEB%20AVANZADO/Group%20Repository/AWD30716-SHARKHUB-BACKEND/app) directory:
     - `app/controllers/`: Router paths for the API endpoints.
     - `app/services/`: Pure business logic layer.
     - `app/repositories/`: Data access layer (abstracts Prisma queries).
     - `app/models/schemas/`: Pydantic input/output schemas (DTOs).

6. **Boilerplate Implementation**:
   - Created [config.py](file:///C:/Users/andre/Desktop/ESPE/SEMESTRE%205/WEB%20AVANZADO/Group%20Repository/AWD30716-SHARKHUB-BACKEND/app/config.py) to read configuration safely using Pydantic.
   - Created [database.py](file:///C:/Users/andre/Desktop/ESPE/SEMESTRE%205/WEB%20AVANZADO/Group%20Repository/AWD30716-SHARKHUB-BACKEND/app/database.py) to initialize and export the Prisma client.
   - Created [main.py](file:///C:/Users/andre/Desktop/ESPE/SEMESTRE%205/WEB%20AVANZADO/Group%20Repository/AWD30716-SHARKHUB-BACKEND/app/main.py) to define the FastAPI app, hook database connection to lifespan startup/shutdown events, configure CORS, and host a `/api/health` check endpoint.

7. **Verification**:
   - Started the server and performed a request to `http://127.0.0.1:8000/api/health`.
   - The test query (`SELECT 1;`) successfully ran against Supabase, returning:
     ```json
     {
         "status": "healthy",
         "database": "connected"
     }
     ```

---

## How to Run the Server

To launch the backend API locally, navigate to the `AWD30716-SHARKHUB-BACKEND` directory and run:

```powershell
# Start the Uvicorn development server
.venv\Scripts\python -m uvicorn app.main:app --reload
```

- **Interactive API Docs (Swagger UI)**: Open your browser at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs). Here you will see your endpoints automatically documented by FastAPI.
- **Alternative Docs (ReDoc)**: Visit [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc).

---

## Recommendations for Coding

Since you are implementing a clean MVC architecture:
1. **Controllers**: Create sub-routers in `app/controllers` (e.g., `appointment_controller.py`) and import them in `app/main.py` using `app.include_router()`.
2. **Services**: Put all business logic in `app/services`. Controllers should delegate work to services, never query the database directly.
3. **Repositories**: Query Prisma inside classes in `app/repositories` (e.g., `UserRepository`). Services will use these repositories to query data, decoupling database details from logic.
4. **Schemas**: Define Pydantic models in `app/models/schemas` for request validation and response filtering.
