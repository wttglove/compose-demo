# 🚀 Docker Compose Multi-Container Demo

Full-stack application demonstrating Docker Compose with multiple services.

## 📋 Architecture
```
┌─────────────┐      ┌─────────────┐      ┌──────────────┐
│   Frontend  │─────▶│     API     │─────▶│  PostgreSQL  │
│   (Nginx)   │      │   (Flask)   │      │   Database   │
│   Port 8080 │      │   Port 5000 │      │              │
└─────────────┘      └─────────────┘      └──────────────┘
```

## 🛠️ Tech Stack

- **Frontend**: Nginx serving static HTML/JS
- **Backend**: Python Flask REST API
- **Database**: PostgreSQL 15
- **Orchestration**: Docker Compose

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose installed

### Run the application
```bash
# Start all services
docker-compose up --build

# Or run in detached mode
docker-compose up -d --build
```

### Access the application
- **Frontend**: http://localhost:8080
- **API**: http://localhost:5000/api/status
- **Health Check**: http://localhost:5000/api/health

## 📊 Features

- ✅ Multi-container orchestration
- ✅ Database persistence with volumes
- ✅ Health checks for database
- ✅ Environment variable configuration
- ✅ API endpoint for visit tracking
- ✅ Real-time visit statistics

## 🔧 Useful Commands
```bash
# View logs
docker-compose logs

# View specific service logs
docker-compose logs api
docker-compose logs -f db  # Follow logs

# Stop services
docker-compose down

# Stop and remove volumes (data will be lost!)
docker-compose down -v

# Rebuild images
docker-compose build

# Check running services
docker-compose ps
```

## 📁 Project Structure
```
compose-demo/
├── docker-compose.yml       # Main orchestration file
├── frontend/
│   ├── Dockerfile
│   └── index.html          # Static frontend
├── api/
│   ├── Dockerfile
│   ├── app.py              # Flask API
│   └── requirements.txt    # Python dependencies
└── README.md
```

## 🗄️ Database Schema
```sql
CREATE TABLE visits (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    endpoint VARCHAR(100)
);
```

## 🌐 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/status` | GET | Get API status and increment visit counter |
| `/api/visits` | GET | Get last 10 visits from database |
| `/api/health` | GET | Health check endpoint |

## 🔐 Environment Variables

The API uses the following environment variables (configured in `docker-compose.yml`):

- `DB_HOST`: Database hostname (default: `db`)
- `DB_NAME`: Database name (default: `devops_db`)
- `DB_USER`: Database user (default: `devops_user`)
- `DB_PASSWORD`: Database password (default: `devops_pass`)

## 📝 Learning Outcomes

This project demonstrates:

1. **Docker Compose** - Multi-container orchestration
2. **Service Dependencies** - Using `depends_on` with health checks
3. **Networking** - Container-to-container communication
4. **Volumes** - Data persistence across container restarts
5. **Environment Variables** - Configuration management
6. **Health Checks** - Ensuring service readiness

## 🎯 Next Steps

- [ ] Add Redis caching layer
- [ ] Implement JWT authentication
- [ ] Add monitoring with Prometheus/Grafana
- [ ] Create CI/CD pipeline
- [ ] Deploy to cloud (AWS/GCP/Azure)

## 📚 Resources

- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

---

**Built with ❤️ as part of DevOps learning journey**