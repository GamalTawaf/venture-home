# Venture Dashboard

A comprehensive dashboard for managing and visualizing venture data, built with Django REST Framework on the backend and SvelteKit on the frontend.

## Features

- **Venture Management**: Create, read, update, and delete venture records
- **Interactive Charts**: Visualize venture metrics with D3.js
- **AI-Powered Chat**: Ask questions about your ventures using Gemini AI
- **Filtering & Search**: Advanced filtering by stage, status, pod, and search functionality
- **Metrics Dashboard**: Real-time metrics including total ventures, active ventures, burn rate, and runway
- **Authentication**: JWT-based authentication system
- **Responsive Design**: Mobile-friendly interface with Tailwind CSS

## Tech Stack

### Backend
- **Django** - Web framework
- **Django REST Framework** - API development
- **PostgreSQL** - Database
- **JWT Authentication** - Secure token-based auth
- **Docker** - Containerization

### Frontend
- **SvelteKit** - Full-stack framework
- **Svelte** - Reactive UI framework
- **D3.js** - Data visualization
- **Tailwind CSS** - Utility-first CSS framework
- **Vite** - Build tool and dev server

## Prerequisites

- Docker and Docker Compose
- Git

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd venture
   ```

2. **Environment Configuration**

   Create a `.env` file in the `backend/` directory:
   ```env
   DEBUG=True
   SECRET_KEY=your-secret-key-here
   POSTGRES_DB=venture-db
   POSTGRES_USER=venture-user
   POSTGRES_PASSWORD=venture-pass
   POSTGRES_HOST=db
   POSTGRES_PORT=5432
   GOOGLE_API_KEY=your-google-api-key-here
   ```

   **Getting a Google API Key:**
   1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
   2. Create a new API key
   3. Add it to your `.env` file as `GOOGLE_API_KEY`

3. **Build and Start Services**
   ```bash
   docker-compose up --build
   ```

   This will:
   - Build the backend and frontend images
   - Start PostgreSQL database
   - Run Django migrations
   - Start the development servers

4. **Inital Setup**
   * this already adds an admin user to play with 
   * It also loads about 30 ventures as a start, you can generate more
    ```
    username: venture-admin
    password: gamalIsTheBest!   
    ```

5. **Access the Application**
   - Frontend: http://localhost:5173

## API Endpoints

### Authentication
- `POST /auth/login/` - Login and get JWT tokens
- `POST /auth/refresh/` - Refresh access token
- `POST /auth/register/` - Register new user

### Ventures
- `GET /ventures/` - List ventures (with filtering/pagination)
- `POST /ventures/` - Create new venture
- `GET /ventures/{id}/` - Get specific venture
- `PUT /ventures/{id}/` - Update venture
- `DELETE /ventures/{id}/` - Delete venture
- `GET /ventures/metrics/` - Get dashboard metrics
- `POST /ventures/chat/` - AI-powered chat about ventures
- `POST /ventures/generate_random/` - Generate sample data

### Filtering Parameters
- `search` - Search in name, pod, stage, status
- `pod` - Filter by pod
- `stage` - Filter by stage
- `status` - Filter by status
- `ordering` - Sort by field (e.g., `-last_update`)

## AI Chat Feature

The application includes an AI-powered chat feature that allows users to ask natural language questions about their venture data.

### How it works
1. User asks a question (e.g., "Which ventures have the highest burn rate?")
2. System queries the database for all venture data
3. Data is sent to Google's Gemini AI via LangChain
4. AI analyzes the data and provides insights
5. Response is displayed in the chat interface

### Example Questions
- "Which ventures have the highest burn rate?"
- "How many ventures are in each stage?"
- "What are the most common venture statuses?"
- "Which pod has the most ventures?"
- "Show me ventures with runway less than 6 months"
- "What is the average burn rate across all ventures?"

### Technical Implementation
- **LangChain**: Orchestrates the AI workflow
- **Google Gemini 1.5 Flash**: Provides the AI analysis
- **Real-time Data**: Always uses current database state
- **Secure**: API key stored server-side, never exposed to frontend


## Project Structure

```
venture/
├── backend/
│   ├── dashboard/
│   │   ├── models.py          # Venture model
│   │   ├── serializers.py     # DRF serializers
│   │   ├── apis.py           # API views
│   │   ├── auth_apis.py      # Authentication views
│   │   └── urls.py           # URL routing
│   ├── venture/
│   │   ├── settings.py       # Django settings
│   │   └── urls.py           # Main URL config
│   ├── requirements.txt      # Python dependencies
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── routes/
│   │   │   ├── +page.svelte     # Dashboard page
│   │   │   ├── Chart.svelte     # Chart component
│   │   │   ├── login/           # Login page
│   │   │   └── venture-list/    # Venture list page
│   │   ├── lib/
│   │   │   └── auth.js          # Authentication store
│   │   └── app.html
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

## Authentication Flow

1. User visits the application
2. If not authenticated, redirected to `/login`
3. User enters credentials and logs in
4. JWT token stored in localStorage
5. All API requests include `Authorization: Bearer <token>` header
6. Token automatically refreshed when needed
7. Logout clears token and redirects to login