from telethon import TelegramClient as AsyncTelethonTelegramClient
from telethon.sync import TelegramClient as SyncTelethonTelegramClient
from pyrogram import Client as PyrogramTelegramClient
from telethon.sessions import MemorySession, SQLiteSession
from pyrogram.storage import MemoryStorage, FileStorage, Storage
from telethon.crypto import AuthKey
from telethon.version import __version__ as telethon_version
from pathlib import Path
from stream_sqlite import stream_sqlite
from typing import Union
import io
import nest_asyncio
import asyncio
import base64
import struct
import platform
import sqlite3
import os
import json


class TelegramSession:

    def to_pyrogram_sqlite(self, session_name: str = "pyrogram", workdir: str = None) -> str:
        """Convert current session to a Pyrogram SQLite session file.
        
        This is a dedicated method for creating Pyrogram SQLite session files,
        ensuring proper format and compatibility.
        
        Args:
            session_name (str): Name for the session file (without .session extension)
            workdir (str): Working directory to save the session file (default: current directory)
            
        Returns:
            str: Path to the created session file
        """
        if workdir is None:
            workdir = os.getcwd()
        
        session_path = os.path.join(workdir, f"{session_name}.session")
        
        # Create storage instance
        storage = FileStorage(session_name, Path(workdir))
        storage.conn = sqlite3.connect(session_path)
        
        async def async_wrapper():
            # Get user data from Telethon
            user_id = 999999999
            th_client = self.make_telethon()
            if th_client:
                async with th_client:
                    user = await th_client.get_me()
                    user_id = user.id
            
            # Create necessary tables
            storage.create()
            
            # Store session data
            await storage.dc_id(self._dc_id)
            await storage.api_id(self.api_id)
            await storage.test_mode(False)
            await storage.auth_key(self._auth_key)
            await storage.user_id(user_id)
            await storage.date(0)
            await storage.is_bot(False)
            await storage.save()
            
            # Ensure proper cleanup
            storage.conn.commit()
            storage.conn.close()
            return session_path
            
        if self.USE_NEST_ASYNCIO:
            nest_asyncio.apply(self._loop)
            
        task = self._loop.create_task(async_wrapper())
        return self._loop.run_until_complete(task)

    def to_tdata(self, folder_name: str = "tdata") -> bool:
        """Convert current session to Telegram Desktop tdata folder format.
        
        This creates a complete tdata folder that can be used with Telegram Desktop,
        including all necessary files and proper encryption.
        
        Args:
            folder_name (str): Name of the output folder to store tdata
            
        Returns:
            bool: True if conversion was successful
        """
        from opentele.td import TDesktop
        from opentele.api import APIData
        
        # Ensure folder exists
        tdata_path = Path(folder_name)
        tdata_path.mkdir(parents=True, exist_ok=True)
        
        # Create API configuration
        api = APIData(
            api_id=self.api_id,
            api_hash=self.api_hash,
            device_model=self.DEFAULT_DEFICE_MODEL,
            system_version=self.DEFAULT_SYSTEM_VERSION,
            app_version=self.DEFAULT_APP_VERSION
        )
        
        async def async_wrapper():
            try:
                # Create and connect temporary client
                temp_client = self.make_telethon()
                await temp_client.connect()
                
                # Initialize TDesktop instance
                tdesk = TDesktop()
                
                # Convert session to tdata format
                await tdesk.FromTelethon(temp_client, folder_name, api)
                
                # Cleanup
                await temp_client.disconnect()
                return True
                
            except Exception as e:
                if tdata_path.exists():
                    import shutil
                    shutil.rmtree(tdata_path)
                raise Exception(f"Failed to create tdata: {str(e)}")
        
        if self.USE_NEST_ASYNCIO:
            nest_asyncio.apply(self._loop)
            
        task = self._loop.create_task(async_wrapper())
        return self._loop.run_until_complete(task)
