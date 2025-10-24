# Docker Expert Demo - Todo Application

A comprehensive Flask-based Todo application demonstrating Docker best practices, multi-stage builds, and container orchestration with Redis as the backend storage.

## 🏗️ Project Architecture

This demo showcases a modern web application built with:
- **Backend**: Flask (Python 3.12)
- **Database**: Redis for data persistence
- **Frontend**: HTML templates with Tailwind CSS
- **Containerization**: Docker with multi-stage builds
- **Orchestration**: Docker Compose

## 📁 Project Structure

```
docker-expert-demo/
├── app/
│   ├── main.py              # Flask application with web and API routes
│   ├── models.py            # Todo data model
│   ├── storage.py           # Redis storage abstraction
│   ├── static/
│   │   └── style.css        # Custom CSS styles
│   └── templates/
│       ├── base.html        # Base template with Tailwind CSS
│       └── index.html       # Main todo interface
├── Dockerfile.chunky        # Single-stage Docker build (larger image)
├── Dockerfile.multistage    # Multi-stage Docker build (optimized)
├── docker-compose.yml       # Container orchestration
├── requirements.txt         # Python dependencies
├── .dockerignore           # Docker ignore patterns
└── commands.txt            # Development commands reference
```

## 🚀 Features

### Web Interface
- **Modern UI**: Clean, responsive design with Tailwind CSS
- **Real-time Updates**: Add, toggle, and delete todos instantly
- **Host Information**: Displays container hostname for load balancing demos
- **Flash Messages**: User feedback for all operations

### API Endpoints
- `GET /` - Main todo interface
- `GET /health` - Health check with Redis connectivity
- `POST /add` - Add new todo
- `POST /toggle/<id>` - Toggle todo completion
- `POST /delete/<id>` - Delete specific todo
- `POST /clear-completed` - Remove all completed todos

### JSON API
- `GET /api/todos` - List all todos (JSON)
- `POST /api/todos` - Create new todo (JSON)
- `POST /api/todos/<id>/toggle` - Toggle todo (JSON)
- `DELETE /api/todos/<id>` - Delete todo (JSON)
- `POST /api/todos/clear-completed` - Clear completed (JSON)

## 🐳 Docker Configurations

### Single-Stage Build (Dockerfile.chunky)
```dockerfile
FROM python:3.12
WORKDIR /app
COPY . /app
RUN pip install --upgrade pip && pip install -r requirements.txt
EXPOSE 5005
CMD ["python", "-m", "app.main"]
```

**Characteristics:**
- Simple, straightforward build
- Larger final image size
- Includes build tools and dependencies
- Runs as root user

### Multi-Stage Build (Dockerfile.multistage)
```dockerfile
# Stage 1: Builder
FROM python:3.12-slim AS builder
# Build wheels for dependencies

# Stage 2: Runner  
FROM python:3.12-slim
# Copy wheels and install
# Create non-root user
# Add health check
```

**Optimizations:**
- **Smaller Image**: ~50% reduction in size
- **Security**: Non-root user execution
- **Health Checks**: Built-in container health monitoring
- **Layer Optimization**: Efficient caching and minimal layers

## 🛠️ Development Setup

### Local Development
```bash
# Start Redis
brew services start redis  # macOS
# or
sudo systemctl start redis  # Linux

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export REDIS_HOST=localhost
export REDIS_PORT=6379
export FLASK_ENV=development
export FLASK_APP=app/main.py
export PORT=5004

# Run application
python -m app.main
```

### Docker Development

#### Single-Stage Build
```bash
# Build chunky image
docker build -f Dockerfile.chunky -t sr-demo-chunky:latest .

# Check image size
docker images | grep sr-demo-chunky
```

#### Multi-Stage Build
```bash
# Build optimized image
docker build -f Dockerfile.multistage -t sr-demo-lean:latest .

# Compare image sizes
docker images | egrep 'sr-demo-(lean|chunky)'
```

#### Docker Compose
```bash
# Start full stack
docker compose up --build

# Test endpoints
curl http://localhost:5005/
curl http://localhost:5005/health
curl http://localhost:5005/api/todos

# Cleanup
docker compose down -v
```

## 🔧 Configuration

### Environment Variables
- `REDIS_HOST`: Redis server hostname (default: localhost)
- `REDIS_PORT`: Redis server port (default: 6379)
- `REDIS_DB`: Redis database number (default: 0)
- `FLASK_SECRET`: Flask secret key for sessions
- `PORT`: Application port (default: 5005)

### Redis Configuration
The application uses Redis for data persistence with:
- **Key Structure**: `TODO:<id>` for individual todos
- **Ordering**: `TODOS_ORDER` list for todo sequence
- **Persistence**: AOF (Append Only File) enabled
- **Data Format**: JSON serialization

## 📊 Performance Comparison

| Build Type | Image Size | Security | Health Checks | Build Time |
|------------|------------|----------|---------------|------------|
| Single-Stage | ~400MB | Root user | None | Fast |
| Multi-Stage | ~200MB | Non-root | Included | Moderate |

## 🧪 Testing

### Health Check
```bash
curl http://localhost:5005/health
# Expected: {"status": "ok", "redis": true}
```

### API Testing
```bash
# Add todo
curl -X POST http://localhost:5005/api/todos \
  -H "Content-Type: application/json" \
  -d '{"title": "Learn Docker"}'

# List todos
curl http://localhost:5005/api/todos

# Toggle todo
curl -X POST http://localhost:5005/api/todos/<id>/toggle
```

## 🎯 Take Home Challenge

### Step 1: Push Your Image
Deploy the Todo app to ECR, ACR, or Docker Hub

**Requirements:**
- Build the optimized multi-stage image
- Tag with your registry prefix
- Push to your chosen container registry
- Document the push process

**Example Commands:**
```bash
# Tag for your registry
docker tag sr-demo-lean:latest your-registry/todo-app:latest

# Push to registry
docker push your-registry/todo-app:latest
```

### Step 2: Document Steps
Take screenshots of your deployment process or record it if you wish

**Documentation Should Include:**
- Screenshots of the build process
- Registry push confirmation
- Image size comparison
- Any custom configurations made

### Step 3: Get 1-on-1 Session
Send your documentation to **hello@shreyas-shack.tech**

**Submission Requirements:**
- Link to your pushed image
- Screenshots or video of the process
- Brief description of any challenges faced
- Your preferred time for the 1-on-1 session

## 🔍 Key Learning Objectives

This demo teaches:
1. **Docker Best Practices**: Multi-stage builds, security, optimization
2. **Container Orchestration**: Docker Compose for multi-service apps
3. **Application Architecture**: Microservices with Redis backend
4. **Development Workflow**: Local development with Docker
5. **Production Readiness**: Health checks, non-root users, minimal images

## 📝 Additional Notes

- The application includes both web UI and REST API
- Redis persistence ensures data survives container restarts
- Health checks enable proper container orchestration
- Multi-stage builds demonstrate production optimization techniques
- The demo is designed to showcase Docker expertise in interviews

---

**Created by**: Shreyas Ladhe  
**Contact**: hello@shreyas-shack.tech  
**Purpose**: Docker Expert Talk - SR University
