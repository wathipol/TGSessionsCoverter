<img src="https://cdn4.iconfinder.com/data/icons/social-media-and-logos-12/32/Logo_telegram_Airplane_Air_plane_paper_airplane-33-256.png" align="right" width="131" />

# TGSessionsConverter
![PyPI](https://img.shields.io/pypi/v/TGSessionsConverter)
![PyPI - License](https://img.shields.io/pypi/l/TGSessionsConverter)


This module is small util for easy converting Telegram sessions  to various formats (Telethon, Pyrogram, Tdata)
<hr/>


## Installation
```
$ pip install TGSessionsConverter
```

## Quickstart

1. in the first step: Converting your format to a TelegramSession instance

```python
from tg_converter import TelegramSession
import io

API_ID = 123
API_HASH = "Your API HASH"

# From SQLite telethon\pyrogram session file
session = TelegramSession.from_sqlite_session_file("my_session_file.session", API_ID, API_HASH)

# From SQLite telethon\pyrogram session file bytes stream (io.BytesIO)
with open("my_example_file.session", "rb") as file:
    session_stream = io.BytesIO(file.read())
session = TelegramSession.from_telethon_sqlite_stream(session_stream, API_ID, API_HASH)
```

2. Converting TelegramSession instance to the format whats you need

```python
from tg_converter import TelegramSession

session = TelegramSession(...) # See first step to learn how to create from various formats

# To telethon client
client = session.make_telethon(sync=True) # Use MemorySession as default, see docs
client.connect()
client.send_message("me", "Hello, World!")
client.disconnect()

# To telethon session file (SQLite)
session.make_telethon_session_file("telethon.session")

# To Pyrogram SQLite session file
pyrogram_path = session.to_pyrogram_sqlite("pyrogram_session")

# To Telegram Desktop tdata folder
success = session.to_tdata("tdata_folder")
```

## Docs

### How it works
> An authorization session consists of an authorization key and some additional data required to connect. The module simply extracts this data and creates an instance of TelegramSession based on it, the methods of which are convenient to use to convert to the format you need.

### TelegramSession

...

### Converting to the format whats you need

The TelegramSession class provides several methods to convert your session to different formats:

**to_pyrogram_sqlite(session_name: str = "pyrogram", workdir: str = None) -> str**
- Creates a Pyrogram SQLite session file from the current session
- Parameters:
  - session_name: Name for the session file (without .session extension)
  - workdir: Working directory to save the session file (default: current directory)
- Returns: Path to the created session file

**to_tdata(folder_name: str = "tdata") -> bool**
- Converts the current session to Telegram Desktop tdata folder format
- Parameters:
  - folder_name: Name of the output folder to store tdata
- Returns: True if conversion was successful

...

## TODO

- [x] From telethon\pyrogram SQLite session file
- [x] From telethon\pyrogram SQLite session stream
- [x] From tdata
- [x] To telethon client object (Sync\Async)
- [x] To telethon SQLite session file
- [x] To pyrogram client object
- [x] To pyrogram SQLite session file
- [x] To tdata
- [x] From telethon client object
- [ ] From pyrogram client object
- [ ] CLI usage
- [ ] Write normal docs
