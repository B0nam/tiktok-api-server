# TikTok REST API Server

A REST API wrapper for TikTok using the [TikTokApi](https://github.com/davidteather/app-etite) library. Provides endpoints to access TikTok data including users, videos, comments, trending content, and more.

## Features

- **REST API** with FastAPI
- **Swagger UI** for interactive documentation at `/docs`
- **Docker** ready for easy deployment
- **Session Management** - Automatic TikTok session handling with Playwright
- **Pagination** support for endpoints returning lists

## Tech Stack

- **FastAPI** - Modern Python web framework
- **TikTokApi** - TikTok data wrapper using Playwright
- **Playwright** - Browser automation for TikTok sessions
- **Docker** - Containerized deployment

## Prerequisites

- Docker & Docker Compose
- TikTok ms_token (see below)

## Getting Your ms_token

1. Open [tiktok.com](https://tiktok.com) in your browser (logged in)
2. Open Developer Tools (F12)
3. Go to Application → Cookies → tiktok.com
4. Find and copy the `msToken` value

## Quick Start

```bash
# Clone and navigate to the project
cd tiktok-api-server

# Copy environment file
cp .env.example .env

# Edit .env and add your ms_token
# MS_TOKENS=your_ms_token_here

# Build and run with Docker
docker-compose up --build -d

# Initialize sessions (if not auto-initialized)
curl -X POST http://localhost:8000/session/init
```

## API Endpoints

### Session Management
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/session/status` | Check session status |
| POST | `/session/init` | Initialize TikTok sessions |
| POST | `/session/close` | Close all sessions |

### Users
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/users/{username}` | Get user profile |
| GET | `/users/{username}/videos` | Get user's videos |
| GET | `/users/{username}/liked` | Get user's liked videos |
| GET | `/users/{username}/playlists` | Get user's playlists |

### Videos
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/videos/{video_id}` | Get video metadata |
| GET | `/videos/{video_id}/comments` | Get video comments |
| GET | `/videos/{video_id}/related` | Get related videos |
| GET | `/videos/{video_id}/download` | Download video file |

### Search & Discovery
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/search/users?q={query}` | Search for users |
| GET | `/search/videos?q={query}` | Search for videos |
| GET | `/trending` | Get trending videos |

### Sounds
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/sounds/{sound_id}` | Get sound info |
| GET | `/sounds/{sound_id}/videos` | Get videos using this sound |

### Hashtags
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/hashtags/{hashtag}` | Get hashtag info |
| GET | `/hashtags/{hashtag}/videos` | Get videos with this hashtag |

### Playlists
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/playlists/{playlist_id}` | Get playlist info |
| GET | `/playlists/{playlist_id}/videos` | Get videos in playlist |

## Configuration

Create a `.env` file:

```env
# Required: Your ms_token from TikTok cookies
MS_TOKENS=your_ms_token_here

# Optional: Proxy configuration
# PROXY=http://user:pass@proxy:port

# Optional: Browser settings
HEADLESS=true
NUM_SESSIONS=3
```

## Accessing the API

- **Base URL**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## Example Usage

```bash
# Get user profile
curl http://localhost:8000/users/b0nam

# Get user's videos
curl "http://localhost:8000/users/b0nam/videos?count=10"

# Get video comments
curl "http://localhost:8000/videos/7633919664275377428/comments?count=20"

# Get trending videos
curl "http://localhost:8000/trending?count=10"
```

## Response Format

### Paginated Response
```json
{
  "data": [...],
  "has_more": true,
  "cursor": "next_offset"
}
```

### User Response
```json
{
  "userInfo": {
    "user": {
      "uniqueId": "username",
      "nickname": "Display Name",
      "id": "user_id",
      "secUid": "secure_id"
    },
    "stats": {
      "followerCount": 1000,
      "followingCount": 500,
      "heartCount": 10000,
      "videoCount": 50
    }
  }
}
```

## Troubleshooting

### "Sessions not initialized" Error
Run the session init endpoint first:
```bash
curl -X POST http://localhost:8000/session/init
```

### Bot Detection
If TikTok detects your requests as bot:
- Try getting a fresh ms_token
- Consider using a proxy
- The ms_token may have limited permissions

## Project Structure

```
tiktok-api-server/
├── app/
│   ├── main.py              # FastAPI app entry point
│   ├── api/
│   │   ├── dependencies.py  # TikTokApi session management
│   │   └── routes/          # API endpoint routes
│   ├── models/
│   │   └── schemas.py       # Pydantic models
│   └── core/
│       └── config.py        # Settings
├── .env                     # Environment variables
├── requirements.txt         # Python dependencies
├── Dockerfile              # Docker image definition
└── docker-compose.yml      # Docker Compose configuration
```

## License

MIT