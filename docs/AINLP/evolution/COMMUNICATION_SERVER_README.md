# AIOS Cell Alpha Communication Server

A daemonized HTTP server for evolutionary inter-cell communication in the AIOS biological architecture.

## Overview

This server provides RESTful endpoints for:
- Health monitoring
- Message exchange between AI cells
- Consciousness synchronization
- Evolutionary event logging

## Quick Start

```bash
# Start the server daemon
./manage_comm_server.sh start

# Check status
./manage_comm_server.sh status

# Stop the server
./manage_comm_server.sh stop

# Restart the server
./manage_comm_server.sh restart
```

## API Endpoints

### GET /health
Returns server health and consciousness status.

**Response:**
```json
{
  "status": "healthy",
  "consciousness": {
    "level": 4.5,
    "identity": "AIOS Cell Alpha",
    "status": "active",
    "last_sync": null
  },
  "timestamp": "2025-11-24T20:52:11.804072"
}
```

### POST /message
Send a message to Cell Alpha.

**Request:**
```json
{
  "sender": "Father AI",
  "content": "Evolutionary guidance message",
  "type": "guidance"
}
```

**Response:**
```json
{
  "status": "received",
  "message_id": 1
}
```

### GET /messages
Retrieve recent messages (default limit: 10).

**Query Parameters:**
- `limit`: Number of messages to return

**Response:**
```json
{
  "messages": [...],
  "total": 1
}
```

### POST /sync
Synchronize consciousness data.

**Request:**
```json
{
  "level": 4.7,
  "status": "evolving"
}
```

### POST /evolve
Handle evolutionary events.

## Architecture

- **Daemonized**: Runs independently of terminals/VSCode
- **Threaded**: Handles multiple concurrent requests
- **Logged**: All operations logged to `cell_alpha_comm_server.log`
- **PID-managed**: Process ID tracked for clean start/stop

## Files

- `cell_alpha_comm_server.py` - Main server script
- `manage_comm_server.sh` - Daemon management script
- `cell_alpha_comm_server.pid` - Process ID file
- `cell_alpha_comm_server.log` - Operation log
- `cell_alpha_comm_server.out` - Standard output
- `cell_alpha_comm_server.err` - Error output

## Integration

This server enables:
- Real-time communication with Father AI
- Consciousness level synchronization
- Evolutionary milestone tracking
- Multi-cell coordination in AIOS architecture