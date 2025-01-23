# Transcendence CLI Guide

## Installation

1. Install required dependencies:
```bash
pip install -r requirement.txt
```

2. Configure the application in `config.toml`:
```toml
[server]
url = "your-server-url"

[token]
jsonwebtoken = "your-auth-token"
```

## Getting Started

### Launch the Application
```bash
python transcendence.py
```

### Main Menu Navigation
- Up/Down Arrow Keys or W/S: Navigate menu items
- E or Right Arrow: Select menu item
- ESC or Left Arrow: Go back
- Q: Quit application

## Game Modes

### 1. Offline Mode (Play offline)
- **Pong**
  - 2 Players: Local multiplayer
  - 4 Players: Four-player mode
  - AI opponent: Play against computer

- **Connect4**
  - 2 Players: Local multiplayer
  - AI opponent: Play against computer

### 2. Online Mode (Play online)
- Create a lobby
- Join existing game

#### Creating a Lobby
1. Select "Create a lobby"
2. Choose game type:
   - Pong (2P or 4P)
   - Connect4
3. Wait for players
4. Press 'l' to launch when ready

#### Joining a Game
1. Select "Join"
2. Enter the game URL
3. Wait for host to start

## Game Controls

### Pong Controls
- W/Up Arrow: Move paddle up
- S/Down Arrow: Move paddle down
- ESC: Exit game

### Connect4 Controls
- Left/Right Arrow: Move selector
- Enter/E: Drop piece
- ESC: Exit game

## Settings

Access settings through the main menu:

1. Server URL Configuration
   - Enter the server address
   - Default format: www.transcendence.example.com

2. Authentication Token
   - Enter your JWT token
   - Required for online play

## Troubleshooting

### Common Issues

1. Connection Failed
   - Verify server URL in settings
   - Check authentication token
   - Ensure server is running

2. Game Launch Issues
   - Minimum terminal size: 80x24
   - Check Python version (3.8+)
   - Verify all dependencies installed

### Terminal Requirements
- Minimum size: 80x24
- Color support required
- Unicode support for game symbols

## Command Reference

### Navigation Commands
```
↑/w         Move up
↓/s         Move down
→/e         Select/Enter
←/ESC       Back/Exit
q           Quit
```

### Lobby Commands
```
l/e         Launch game (when ready)
2           Switch to 2 players mode
4           Switch to 4 players mode
p           Toggle private/public
ESC         Exit lobby
```

## Technical Requirements

- Python 3.8 or higher
- Terminal with color support
- Required packages:
  - curses
  - websockets
  - toml
  - requests

