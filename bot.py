"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   ██╗   ██╗ █████╗ ███╗   ██╗███████╗██╗  ██╗    ██████╗  ██████╗ ████████╗  ║
║   ██║   ██║██╔══██╗████╗  ██║██╔════╝██║  ██║    ██╔══██╗██╔═══██╗╚══██╔══╝  ║
║   ██║   ██║███████║██╔██╗ ██║███████╗███████║    ██████╔╝██║   ██║   ██║     ║
║   ╚██╗ ██╔╝██╔══██║██║╚██╗██║╚════██║██╔══██║    ██╔══██╗██║   ██║   ██║     ║
║    ╚████╔╝ ██║  ██║██║ ╚████║███████║██║  ██║    ██████╔╝╚██████╔╝   ██║     ║
║     ╚═══╝  ╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝    ╚═════╝  ╚═════╝    ╚═╝     ║
║                                                                              ║
║                    PROFESSIONAL TELEGRAM AUTOMATION BOT                       ║
║                           Version 6.0 Ultimate                               ║
║                                                                              ║
║                        Created by @skullmodders                              ║
║                      Join Telegram: @skullmodders                            ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

FEATURES:
- Auto-broadcast to all groups
- Auto-reply to private messages
- Auto-reaction to group mentions
- Auto-reaction to private messages
- Configurable delays and timings
- Statistics and analytics
- Clean professional interface
- Robust error handling
- Database persistence
- Rate limiting protection
"""

import asyncio
import os
import sys
import random
import time
import json
import sqlite3
import hashlib
import logging
import signal
import traceback
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any, Set, Union
from dataclasses import dataclass, field, asdict
from enum import Enum, auto
from contextlib import contextmanager
from functools import wraps
from collections import defaultdict
import threading
import queue

# Third-party imports
try:
    from colorama import init, Fore, Style, Back
    init(autoreset=True)
except ImportError:
    print("Installing colorama...")
    os.system("pip install colorama")
    from colorama import init, Fore, Style, Back
    init(autoreset=True)

try:
    from telethon import TelegramClient, events
    from telethon.errors import (
        SessionPasswordNeededError,
        FloodWaitError,
        ChatWriteForbiddenError,
        UserBannedInChannelError,
        PhoneCodeInvalidError,
        ChannelPrivateError,
        ChatAdminRequiredError,
        UserNotParticipantError,
        MessageIdInvalidError,
        PeerIdInvalidError,
        RPCError,
        AuthKeyUnregisteredError,
        UserDeactivatedError,
        UserDeactivatedBanError,
        PhoneNumberBannedError,
        SlowModeWaitError,
        MessageTooLongError,
    )
    from telethon.tl.functions.messages import SendReactionRequest, GetMessagesRequest
    from telethon.tl.functions.channels import GetParticipantRequest
    from telethon.tl.types import (
        ReactionEmoji,
        User,
        Channel,
        Chat,
        Message,
        InputPeerChannel,
        InputPeerChat,
        InputPeerUser,
        PeerChannel,
        PeerChat,
        PeerUser,
    )
except ImportError:
    print("Installing telethon...")
    os.system("pip install telethon")
    from telethon import TelegramClient, events
    from telethon.errors import *
    from telethon.tl.functions.messages import SendReactionRequest, GetMessagesRequest
    from telethon.tl.types import *


# ══════════════════════════════════════════════════════════════════════════════
#                              CONSTANTS & ENUMS
# ══════════════════════════════════════════════════════════════════════════════

class LogLevel(Enum):
    """Log level enumeration"""
    DEBUG = auto()
    INFO = auto()
    WARNING = auto()
    ERROR = auto()
    CRITICAL = auto()


class BotStatus(Enum):
    """Bot status enumeration"""
    STOPPED = auto()
    STARTING = auto()
    RUNNING = auto()
    PAUSED = auto()
    STOPPING = auto()
    ERROR = auto()


class MessageType(Enum):
    """Message type enumeration"""
    TEXT = auto()
    PHOTO = auto()
    VIDEO = auto()
    DOCUMENT = auto()
    AUDIO = auto()
    VOICE = auto()
    STICKER = auto()
    GIF = auto()
    POLL = auto()
    FORWARD = auto()
    OTHER = auto()


class ActionType(Enum):
    """Action type enumeration"""
    BROADCAST = auto()
    PRIVATE_REPLY = auto()
    GROUP_REACTION = auto()
    PRIVATE_REACTION = auto()
    GROUP_SYNC = auto()
    ERROR = auto()


# Application constants
APP_NAME = "VANSH Telegram Bot"
APP_VERSION = "6.0 Ultimate"
APP_AUTHOR = "@skullmodders"

# File paths
FILES = {
    "credentials": "data/credentials.json",
    "settings": "data/settings.json",
    "groups": "data/groups.json",
    "statistics": "data/statistics.json",
    "blacklist": "data/blacklist.json",
    "whitelist": "data/whitelist.json",
    "templates": "data/templates.json",
    "logs": "logs/bot.log",
    "database": "data/vansh_bot.db",
}

# Default reactions
DEFAULT_REACTIONS = [
    "👍", "❤️", "🔥", "😂", "😍", "😎", "🎉", "⚡", 
    "🫡", "👏", "💯", "🙌", "✨", "🌟", "💪", "🤝",
    "😊", "🥰", "😇", "🤩", "😋", "🤗", "🫶", "💖",
]

# Positive reactions for private messages
PRIVATE_REACTIONS = [
    "❤️", "😍", "🥰", "💕", "💖", "💗", "💓", "💞",
    "✨", "🌟", "⭐", "💫", "🎉", "🎊", "🤩", "😊",
]


# ══════════════════════════════════════════════════════════════════════════════
#                              DATA CLASSES
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class DelayConfig:
    """Delay configuration settings"""
    # Broadcast delays
    broadcast_min: float = 3.0
    broadcast_max: float = 8.0
    
    # Private reply delays
    private_reply_min: float = 2.0
    private_reply_max: float = 5.0
    
    # Group reaction delays
    group_reaction_min: float = 0.5
    group_reaction_max: float = 2.0
    
    # Private reaction delays
    private_reaction_min: float = 0.3
    private_reaction_max: float = 1.5
    
    # Cycle wait time (default 10 minutes)
    cycle_wait_time: int = 600
    
    # Broadcast check interval
    broadcast_check_interval: int = 20
    
    # Group sync interval
    group_sync_interval: int = 300
    
    # Private reply cooldown
    private_reply_cooldown: int = 120
    
    # Rate limit delay
    rate_limit_delay: float = 1.0
    
    # Error retry delay
    error_retry_delay: float = 5.0
    
    # Flood wait buffer
    flood_wait_buffer: int = 5
    
    def get_broadcast_delay(self) -> float:
        """Get random broadcast delay"""
        return random.uniform(self.broadcast_min, self.broadcast_max)
    
    def get_private_reply_delay(self) -> float:
        """Get random private reply delay"""
        return random.uniform(self.private_reply_min, self.private_reply_max)
    
    def get_group_reaction_delay(self) -> float:
        """Get random group reaction delay"""
        return random.uniform(self.group_reaction_min, self.group_reaction_max)
    
    def get_private_reaction_delay(self) -> float:
        """Get random private reaction delay"""
        return random.uniform(self.private_reaction_min, self.private_reaction_max)


@dataclass
class FeatureConfig:
    """Feature toggles configuration"""
    enable_broadcast: bool = True
    enable_private_reply: bool = True
    enable_group_reactions: bool = True
    enable_private_reactions: bool = True
    enable_statistics: bool = True
    enable_logging: bool = True
    enable_auto_sync: bool = True
    enable_rate_limiting: bool = True
    enable_error_recovery: bool = True
    enable_flood_protection: bool = True


@dataclass
class Statistics:
    """Bot statistics"""
    total_broadcasts: int = 0
    successful_broadcasts: int = 0
    failed_broadcasts: int = 0
    
    total_private_replies: int = 0
    successful_private_replies: int = 0
    failed_private_replies: int = 0
    
    total_group_reactions: int = 0
    successful_group_reactions: int = 0
    failed_group_reactions: int = 0
    
    total_private_reactions: int = 0
    successful_private_reactions: int = 0
    failed_private_reactions: int = 0
    
    total_errors: int = 0
    flood_waits: int = 0
    total_flood_wait_time: int = 0
    
    groups_synced: int = 0
    last_sync_time: str = ""
    
    bot_start_time: str = ""
    total_uptime_seconds: int = 0
    
    cycles_completed: int = 0
    last_cycle_time: str = ""
    
    def increment(self, field: str, value: int = 1):
        """Increment a statistics field"""
        if hasattr(self, field):
            setattr(self, field, getattr(self, field) + value)
    
    def get_success_rate(self, action: str) -> float:
        """Get success rate for an action type"""
        total = getattr(self, f"total_{action}", 0)
        successful = getattr(self, f"successful_{action}", 0)
        return (successful / total * 100) if total > 0 else 0.0


@dataclass
class GroupInfo:
    """Group information"""
    id: int
    title: str
    username: Optional[str] = None
    member_count: int = 0
    is_megagroup: bool = False
    is_broadcast: bool = False
    last_message_time: Optional[str] = None
    broadcast_count: int = 0
    last_broadcast_id: Optional[int] = None
    is_active: bool = True
    error_count: int = 0
    last_error: Optional[str] = None


@dataclass
class UserInfo:
    """User information for private messaging"""
    id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    is_bot: bool = False
    last_message_time: Optional[str] = None
    last_reply_time: Optional[str] = None
    reply_count: int = 0
    reaction_count: int = 0
    is_blacklisted: bool = False


# ══════════════════════════════════════════════════════════════════════════════
#                              LOGGING SYSTEM
# ══════════════════════════════════════════════════════════════════════════════

class ColoredLogger:
    """Advanced colored logging system"""
    
    COLORS = {
        LogLevel.DEBUG: Fore.LIGHTBLACK_EX,
        LogLevel.INFO: Fore.CYAN,
        LogLevel.WARNING: Fore.YELLOW,
        LogLevel.ERROR: Fore.RED,
        LogLevel.CRITICAL: Fore.RED + Style.BRIGHT,
    }
    
    ICONS = {
        LogLevel.DEBUG: "🔍",
        LogLevel.INFO: "ℹ️",
        LogLevel.WARNING: "⚠️",
        LogLevel.ERROR: "❌",
        LogLevel.CRITICAL: "🚨",
    }
    
    ACTION_ICONS = {
        ActionType.BROADCAST: "📢",
        ActionType.PRIVATE_REPLY: "💬",
        ActionType.GROUP_REACTION: "⚡",
        ActionType.PRIVATE_REACTION: "💝",
        ActionType.GROUP_SYNC: "🔄",
        ActionType.ERROR: "❌",
    }
    
    def __init__(self, log_file: Optional[str] = None, enable_file_logging: bool = True):
        self.log_file = log_file
        self.enable_file_logging = enable_file_logging
        self.log_queue: queue.Queue = queue.Queue()
        self._lock = threading.Lock()
        
        if enable_file_logging and log_file:
            self._setup_file_logging()
    
    def _setup_file_logging(self):
        """Setup file logging"""
        try:
            log_dir = os.path.dirname(self.log_file)
            if log_dir and not os.path.exists(log_dir):
                os.makedirs(log_dir, exist_ok=True)
            
            logging.basicConfig(
                filename=self.log_file,
                level=logging.DEBUG,
                format='%(asctime)s | %(levelname)s | %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
        except Exception as e:
            print(f"{Fore.YELLOW}Warning: Could not setup file logging: {e}{Style.RESET_ALL}")
    
    def _get_timestamp(self) -> str:
        """Get formatted timestamp"""
        return datetime.now().strftime("%H:%M:%S")
    
    def _format_message(self, level: LogLevel, message: str, action: Optional[ActionType] = None) -> str:
        """Format log message with colors"""
        timestamp = self._get_timestamp()
        color = self.COLORS.get(level, Fore.WHITE)
        icon = self.ICONS.get(level, "•")
        
        if action:
            action_icon = self.ACTION_ICONS.get(action, "")
            return f"{Fore.LIGHTBLACK_EX}[{timestamp}]{Style.RESET_ALL} {action_icon} {color}{message}{Style.RESET_ALL}"
        
        return f"{Fore.LIGHTBLACK_EX}[{timestamp}]{Style.RESET_ALL} {icon} {color}{message}{Style.RESET_ALL}"
    
    def _log_to_file(self, level: LogLevel, message: str):
        """Log to file"""
        if self.enable_file_logging:
            level_name = level.name
            logging.log(getattr(logging, level_name, logging.INFO), message)
    
    def log(self, level: LogLevel, message: str, action: Optional[ActionType] = None, to_file: bool = True):
        """Log a message"""
        with self._lock:
            formatted = self._format_message(level, message, action)
            print(formatted)
            
            if to_file:
                self._log_to_file(level, message)
    
    def debug(self, message: str, action: Optional[ActionType] = None):
        """Log debug message"""
        self.log(LogLevel.DEBUG, message, action)
    
    def info(self, message: str, action: Optional[ActionType] = None):
        """Log info message"""
        self.log(LogLevel.INFO, message, action)
    
    def warning(self, message: str, action: Optional[ActionType] = None):
        """Log warning message"""
        self.log(LogLevel.WARNING, message, action)
    
    def error(self, message: str, action: Optional[ActionType] = None):
        """Log error message"""
        self.log(LogLevel.ERROR, message, action)
    
    def critical(self, message: str, action: Optional[ActionType] = None):
        """Log critical message"""
        self.log(LogLevel.CRITICAL, message, action)
    
    def success(self, message: str, action: Optional[ActionType] = None):
        """Log success message"""
        timestamp = self._get_timestamp()
        formatted = f"{Fore.LIGHTBLACK_EX}[{timestamp}]{Style.RESET_ALL} {Fore.GREEN}✓ {message}{Style.RESET_ALL}"
        print(formatted)
        self._log_to_file(LogLevel.INFO, f"SUCCESS: {message}")
    
    def action(self, action_type: ActionType, message: str, success: bool = True):
        """Log an action"""
        icon = self.ACTION_ICONS.get(action_type, "•")
        color = Fore.GREEN if success else Fore.RED
        timestamp = self._get_timestamp()
        status = "✓" if success else "✗"
        formatted = f"{Fore.LIGHTBLACK_EX}[{timestamp}]{Style.RESET_ALL} {icon} {color}{status} {message}{Style.RESET_ALL}"
        print(formatted)
        self._log_to_file(LogLevel.INFO, f"{action_type.name}: {message}")
    
    def divider(self, char: str = "─", length: int = 70):
        """Print a divider line"""
        print(f"{Fore.CYAN}{char * length}{Style.RESET_ALL}")
    
    def header(self, title: str, char: str = "═"):
        """Print a header"""
        length = 70
        padding = (length - len(title) - 2) // 2
        line = char * padding
        print(f"\n{Fore.CYAN}{line} {Fore.WHITE}{Style.BRIGHT}{title}{Style.RESET_ALL}{Fore.CYAN} {line}{Style.RESET_ALL}\n")
    
    def status_line(self, label: str, value: Any, color: str = Fore.WHITE):
        """Print a status line"""
        print(f"  {Fore.LIGHTBLACK_EX}•{Style.RESET_ALL} {Fore.WHITE}{label}:{Style.RESET_ALL} {color}{value}{Style.RESET_ALL}")


# Global logger instance
logger = ColoredLogger(FILES["logs"])


# ══════════════════════════════════════════════════════════════════════════════
#                              DATABASE MANAGER
# ══════════════════════════════════════════════════════════════════════════════

class DatabaseManager:
    """SQLite database manager for persistent storage"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._ensure_directory()
        self._init_database()
    
    def _ensure_directory(self):
        """Ensure database directory exists"""
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
    
    def _get_connection(self) -> sqlite3.Connection:
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    @contextmanager
    def connection(self):
        """Context manager for database connection"""
        conn = self._get_connection()
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def _init_database(self):
        """Initialize database tables"""
        with self.connection() as conn:
            cursor = conn.cursor()
            
            # Groups table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS groups (
                    id INTEGER PRIMARY KEY,
                    title TEXT NOT NULL,
                    username TEXT,
                    member_count INTEGER DEFAULT 0,
                    is_megagroup INTEGER DEFAULT 0,
                    is_broadcast INTEGER DEFAULT 0,
                    last_message_time TEXT,
                    broadcast_count INTEGER DEFAULT 0,
                    last_broadcast_id INTEGER,
                    is_active INTEGER DEFAULT 1,
                    error_count INTEGER DEFAULT 0,
                    last_error TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Users table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    first_name TEXT,
                    last_name TEXT,
                    username TEXT,
                    is_bot INTEGER DEFAULT 0,
                    last_message_time TEXT,
                    last_reply_time TEXT,
                    reply_count INTEGER DEFAULT 0,
                    reaction_count INTEGER DEFAULT 0,
                    is_blacklisted INTEGER DEFAULT 0,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Broadcast history table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS broadcast_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    group_id INTEGER NOT NULL,
                    message_id INTEGER NOT NULL,
                    broadcast_time TEXT DEFAULT CURRENT_TIMESTAMP,
                    success INTEGER DEFAULT 1,
                    error_message TEXT,
                    FOREIGN KEY (group_id) REFERENCES groups(id)
                )
            """)
            
            # Activity log table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS activity_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    action_type TEXT NOT NULL,
                    target_id INTEGER,
                    target_name TEXT,
                    success INTEGER DEFAULT 1,
                    details TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Statistics table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS statistics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    stat_name TEXT UNIQUE NOT NULL,
                    stat_value INTEGER DEFAULT 0,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Settings table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS settings (
                    key TEXT PRIMARY KEY,
                    value TEXT,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
    
    def save_group(self, group: GroupInfo):
        """Save or update group info"""
        with self.connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO groups 
                (id, title, username, member_count, is_megagroup, is_broadcast,
                 last_message_time, broadcast_count, last_broadcast_id, is_active,
                 error_count, last_error, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            """, (
                group.id, group.title, group.username, group.member_count,
                int(group.is_megagroup), int(group.is_broadcast),
                group.last_message_time, group.broadcast_count, group.last_broadcast_id,
                int(group.is_active), group.error_count, group.last_error
            ))
    
    def get_group(self, group_id: int) -> Optional[GroupInfo]:
        """Get group by ID"""
        with self.connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM groups WHERE id = ?", (group_id,))
            row = cursor.fetchone()
            
            if row:
                return GroupInfo(
                    id=row['id'],
                    title=row['title'],
                    username=row['username'],
                    member_count=row['member_count'],
                    is_megagroup=bool(row['is_megagroup']),
                    is_broadcast=bool(row['is_broadcast']),
                    last_message_time=row['last_message_time'],
                    broadcast_count=row['broadcast_count'],
                    last_broadcast_id=row['last_broadcast_id'],
                    is_active=bool(row['is_active']),
                    error_count=row['error_count'],
                    last_error=row['last_error']
                )
        return None
    
    def get_all_groups(self, active_only: bool = True) -> List[GroupInfo]:
        """Get all groups"""
        groups = []
        with self.connection() as conn:
            cursor = conn.cursor()
            
            if active_only:
                cursor.execute("SELECT * FROM groups WHERE is_active = 1")
            else:
                cursor.execute("SELECT * FROM groups")
            
            for row in cursor.fetchall():
                groups.append(GroupInfo(
                    id=row['id'],
                    title=row['title'],
                    username=row['username'],
                    member_count=row['member_count'],
                    is_megagroup=bool(row['is_megagroup']),
                    is_broadcast=bool(row['is_broadcast']),
                    last_message_time=row['last_message_time'],
                    broadcast_count=row['broadcast_count'],
                    last_broadcast_id=row['last_broadcast_id'],
                    is_active=bool(row['is_active']),
                    error_count=row['error_count'],
                    last_error=row['last_error']
                ))
        return groups
    
    def update_group_broadcast(self, group_id: int, message_id: int, success: bool = True, error: Optional[str] = None):
        """Update group broadcast status"""
        with self.connection() as conn:
            cursor = conn.cursor()
            
            if success:
                cursor.execute("""
                    UPDATE groups SET 
                        broadcast_count = broadcast_count + 1,
                        last_broadcast_id = ?,
                        error_count = 0,
                        last_error = NULL,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                """, (message_id, group_id))
            else:
                cursor.execute("""
                    UPDATE groups SET 
                        error_count = error_count + 1,
                        last_error = ?,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                """, (error, group_id))
            
            # Log broadcast
            cursor.execute("""
                INSERT INTO broadcast_history (group_id, message_id, success, error_message)
                VALUES (?, ?, ?, ?)
            """, (group_id, message_id, int(success), error))
    
    def save_user(self, user: UserInfo):
        """Save or update user info"""
        with self.connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO users 
                (id, first_name, last_name, username, is_bot, last_message_time,
                 last_reply_time, reply_count, reaction_count, is_blacklisted, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            """, (
                user.id, user.first_name, user.last_name, user.username,
                int(user.is_bot), user.last_message_time, user.last_reply_time,
                user.reply_count, user.reaction_count, int(user.is_blacklisted)
            ))
    
    def get_user(self, user_id: int) -> Optional[UserInfo]:
        """Get user by ID"""
        with self.connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            row = cursor.fetchone()
            
            if row:
                return UserInfo(
                    id=row['id'],
                    first_name=row['first_name'],
                    last_name=row['last_name'],
                    username=row['username'],
                    is_bot=bool(row['is_bot']),
                    last_message_time=row['last_message_time'],
                    last_reply_time=row['last_reply_time'],
                    reply_count=row['reply_count'],
                    reaction_count=row['reaction_count'],
                    is_blacklisted=bool(row['is_blacklisted'])
                )
        return None
    
    def update_user_reply(self, user_id: int):
        """Update user reply time and count"""
        with self.connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE users SET 
                    last_reply_time = CURRENT_TIMESTAMP,
                    reply_count = reply_count + 1,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (user_id,))
    
    def update_user_reaction(self, user_id: int):
        """Update user reaction count"""
        with self.connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE users SET 
                    reaction_count = reaction_count + 1,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (user_id,))
    
    def log_activity(self, action_type: ActionType, target_id: Optional[int] = None, 
                     target_name: Optional[str] = None, success: bool = True, 
                     details: Optional[str] = None):
        """Log an activity"""
        with self.connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO activity_log (action_type, target_id, target_name, success, details)
                VALUES (?, ?, ?, ?, ?)
            """, (action_type.name, target_id, target_name, int(success), details))
    
    def update_statistic(self, stat_name: str, value: int = 1, increment: bool = True):
        """Update a statistic"""
        with self.connection() as conn:
            cursor = conn.cursor()
            
            if increment:
                cursor.execute("""
                    INSERT INTO statistics (stat_name, stat_value, updated_at)
                    VALUES (?, ?, CURRENT_TIMESTAMP)
                    ON CONFLICT(stat_name) DO UPDATE SET
                        stat_value = stat_value + ?,
                        updated_at = CURRENT_TIMESTAMP
                """, (stat_name, value, value))
            else:
                cursor.execute("""
                    INSERT OR REPLACE INTO statistics (stat_name, stat_value, updated_at)
                    VALUES (?, ?, CURRENT_TIMESTAMP)
                """, (stat_name, value))
    
    def get_statistic(self, stat_name: str) -> int:
        """Get a statistic value"""
        with self.connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT stat_value FROM statistics WHERE stat_name = ?", (stat_name,))
            row = cursor.fetchone()
            return row['stat_value'] if row else 0
    
    def get_all_statistics(self) -> Dict[str, int]:
        """Get all statistics"""
        stats = {}
        with self.connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT stat_name, stat_value FROM statistics")
            for row in cursor.fetchall():
                stats[row['stat_name']] = row['stat_value']
        return stats
    
    def save_setting(self, key: str, value: Any):
        """Save a setting"""
        with self.connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO settings (key, value, updated_at)
                VALUES (?, ?, CURRENT_TIMESTAMP)
            """, (key, json.dumps(value)))
    
    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get a setting"""
        with self.connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
            row = cursor.fetchone()
            
            if row:
                try:
                    return json.loads(row['value'])
                except:
                    return row['value']
        return default
    
    def clear_old_logs(self, days: int = 7):
        """Clear activity logs older than specified days"""
        with self.connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM activity_log 
                WHERE created_at < datetime('now', ? || ' days')
            """, (-days,))
            
            cursor.execute("""
                DELETE FROM broadcast_history 
                WHERE broadcast_time < datetime('now', ? || ' days')
            """, (-days,))


# ══════════════════════════════════════════════════════════════════════════════
#                              FILE MANAGER
# ══════════════════════════════════════════════════════════════════════════════

class FileManager:
    """File operations manager"""
    
    @staticmethod
    def ensure_directories():
        """Ensure all required directories exist"""
        directories = ["data", "logs", "sessions", "backups"]
        for directory in directories:
            if not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)
    
    @staticmethod
    def read_json(filepath: str, default: Any = None) -> Any:
        """Read JSON file"""
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logger.warning(f"Error reading {filepath}: {e}")
        return default if default is not None else {}
    
    @staticmethod
    def write_json(filepath: str, data: Any, indent: int = 4):
        """Write JSON file"""
        try:
            directory = os.path.dirname(filepath)
            if directory and not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=indent, ensure_ascii=False, default=str)
            return True
        except Exception as e:
            logger.error(f"Error writing {filepath}: {e}")
            return False
    
    @staticmethod
    def read_text(filepath: str) -> Optional[str]:
        """Read text file"""
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    return f.read()
        except Exception as e:
            logger.warning(f"Error reading {filepath}: {e}")
        return None
    
    @staticmethod
    def write_text(filepath: str, content: str) -> bool:
        """Write text file"""
        try:
            directory = os.path.dirname(filepath)
            if directory and not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            logger.error(f"Error writing {filepath}: {e}")
            return False
    
    @staticmethod
    def backup_file(filepath: str) -> bool:
        """Create backup of a file"""
        try:
            if os.path.exists(filepath):
                backup_dir = "backups"
                if not os.path.exists(backup_dir):
                    os.makedirs(backup_dir)
                
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = os.path.basename(filepath)
                backup_path = os.path.join(backup_dir, f"{filename}.{timestamp}.bak")
                
                import shutil
                shutil.copy2(filepath, backup_path)
                return True
        except Exception as e:
            logger.warning(f"Error backing up {filepath}: {e}")
        return False


# ══════════════════════════════════════════════════════════════════════════════
#                              RATE LIMITER
# ══════════════════════════════════════════════════════════════════════════════

class RateLimiter:
    """Rate limiting for API calls"""
    
    def __init__(self, max_calls: int = 30, time_window: int = 60):
        self.max_calls = max_calls
        self.time_window = time_window
        self.calls: List[float] = []
        self._lock = asyncio.Lock()
    
    async def acquire(self):
        """Acquire rate limit slot"""
        async with self._lock:
            now = time.time()
            
            # Remove old calls outside time window
            self.calls = [t for t in self.calls if now - t < self.time_window]
            
            if len(self.calls) >= self.max_calls:
                # Calculate wait time
                oldest_call = self.calls[0]
                wait_time = self.time_window - (now - oldest_call) + 0.5
                
                if wait_time > 0:
                    logger.warning(f"Rate limit reached. Waiting {wait_time:.1f}s")
                    await asyncio.sleep(wait_time)
                    
                    # Refresh after waiting
                    now = time.time()
                    self.calls = [t for t in self.calls if now - t < self.time_window]
            
            self.calls.append(now)
    
    def reset(self):
        """Reset rate limiter"""
        self.calls.clear()


# ══════════════════════════════════════════════════════════════════════════════
#                              ERROR HANDLER
# ══════════════════════════════════════════════════════════════════════════════

class ErrorHandler:
    """Centralized error handling"""
    
    RECOVERABLE_ERRORS = {
        FloodWaitError,
        SlowModeWaitError,
        RPCError,
    }
    
    PERMANENT_ERRORS = {
        ChatWriteForbiddenError,
        UserBannedInChannelError,
        ChannelPrivateError,
        ChatAdminRequiredError,
        UserNotParticipantError,
    }
    
    CRITICAL_ERRORS = {
        AuthKeyUnregisteredError,
        UserDeactivatedError,
        UserDeactivatedBanError,
        PhoneNumberBannedError,
    }
    
    @staticmethod
    def classify_error(error: Exception) -> str:
        """Classify error type"""
        error_type = type(error)
        
        if error_type in ErrorHandler.CRITICAL_ERRORS:
            return "critical"
        elif error_type in ErrorHandler.PERMANENT_ERRORS:
            return "permanent"
        elif error_type in ErrorHandler.RECOVERABLE_ERRORS:
            return "recoverable"
        else:
            return "unknown"
    
    @staticmethod
    def get_friendly_message(error: Exception) -> str:
        """Get user-friendly error message"""
        error_type = type(error)
        
        messages = {
            FloodWaitError: f"Rate limited. Wait {getattr(error, 'seconds', '?')} seconds.",
            SlowModeWaitError: f"Slow mode active. Wait {getattr(error, 'seconds', '?')} seconds.",
            ChatWriteForbiddenError: "Cannot send messages to this chat.",
            UserBannedInChannelError: "Banned from this channel.",
            ChannelPrivateError: "Channel is private or doesn't exist.",
            ChatAdminRequiredError: "Admin privileges required.",
            UserNotParticipantError: "Not a member of this chat.",
            AuthKeyUnregisteredError: "Session expired. Please re-login.",
            UserDeactivatedError: "Account has been deactivated.",
            PhoneNumberBannedError: "Phone number is banned.",
        }
        
        return messages.get(error_type, str(error)[:100])
    
    @staticmethod
    async def handle_flood_wait(error: FloodWaitError, buffer: int = 5) -> int:
        """Handle FloodWaitError"""
        wait_time = error.seconds + buffer
        logger.warning(f"FloodWait: Waiting {wait_time} seconds...")
        await asyncio.sleep(wait_time)
        return wait_time
    
    @staticmethod
    def should_retry(error: Exception, attempt: int, max_attempts: int = 3) -> bool:
        """Determine if operation should be retried"""
        if attempt >= max_attempts:
            return False
        
        error_class = ErrorHandler.classify_error(error)
        return error_class in ("recoverable", "unknown")


def with_error_handling(func):
    """Decorator for error handling"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except FloodWaitError as e:
            await ErrorHandler.handle_flood_wait(e)
            return await func(*args, **kwargs)
        except Exception as e:
            error_class = ErrorHandler.classify_error(e)
            friendly_msg = ErrorHandler.get_friendly_message(e)
            
            if error_class == "critical":
                logger.critical(f"Critical error: {friendly_msg}")
                raise
            elif error_class == "permanent":
                logger.warning(f"Permanent error: {friendly_msg}")
                return None
            else:
                logger.error(f"Error: {friendly_msg}")
                return None
    
    return wrapper


# ══════════════════════════════════════════════════════════════════════════════
#                              UI COMPONENTS
# ══════════════════════════════════════════════════════════════════════════════

class UI:
    """User interface components"""
    
    @staticmethod
    def clear_screen():
        """Clear terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @staticmethod
    def display_banner():
        """Display the main VANSH ASCII art banner"""
        banner = f"""
{Fore.CYAN}{Style.BRIGHT}
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   {Fore.MAGENTA}██╗   ██╗ █████╗ ███╗   ██╗███████╗██╗  ██╗    ██████╗  ██████╗ ████████╗{Fore.CYAN}  ║
║   {Fore.MAGENTA}██║   ██║██╔══██╗████╗  ██║██╔════╝██║  ██║    ██╔══██╗██╔═══██╗╚══██╔══╝{Fore.CYAN}  ║
║   {Fore.MAGENTA}██║   ██║███████║██╔██╗ ██║███████╗███████║    ██████╔╝██║   ██║   ██║{Fore.CYAN}     ║
║   {Fore.MAGENTA}╚██╗ ██╔╝██╔══██║██║╚██╗██║╚════██║██╔══██║    ██╔══██╗██║   ██║   ██║{Fore.CYAN}     ║
║   {Fore.MAGENTA} ╚████╔╝ ██║  ██║██║ ╚████║███████║██║  ██║    ██████╔╝╚██████╔╝   ██║{Fore.CYAN}     ║
║   {Fore.MAGENTA}  ╚═══╝  ╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝    ╚═════╝  ╚═════╝    ╚═╝{Fore.CYAN}     ║
║                                                                              ║
║{Fore.WHITE}                    ⚡ PROFESSIONAL TELEGRAM AUTOMATION ⚡                    {Fore.CYAN}║
║{Fore.YELLOW}                           Version {APP_VERSION}                          {Fore.CYAN}║
║                                                                              ║
║{Fore.GREEN}                    ┌─────────────────────────────────┐                    {Fore.CYAN}║
║{Fore.GREEN}                    │  📱 Created by: {Fore.WHITE}{APP_AUTHOR:<14}{Fore.GREEN} │                    {Fore.CYAN}║
║{Fore.GREEN}                    │  📢 Channel: {Fore.WHITE}@skullmodders{Fore.GREEN}      │                    {Fore.CYAN}║
║{Fore.GREEN}                    └─────────────────────────────────┘                    {Fore.CYAN}║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}"""
        print(banner)
    
    @staticmethod
    def display_mini_banner():
        """Display a smaller version of the banner"""
        banner = f"""
{Fore.CYAN}╔═══════════════════════════════════════════════════════════════╗
║  {Fore.MAGENTA}██╗   ██╗ █████╗ ███╗   ██╗███████╗██╗  ██╗{Fore.CYAN}  {Fore.YELLOW}v{APP_VERSION}{Fore.CYAN}   ║
║  {Fore.MAGENTA}╚██╗ ██╔╝███████║██╔██╗ ██║███████╗███████║{Fore.CYAN}  {Fore.GREEN}@skullmodders{Fore.CYAN}  ║
║  {Fore.MAGENTA} ╚████╔╝ ██║  ██║██║ ╚████║╚════██║██╔══██║{Fore.CYAN}                 ║
╚═══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""
        print(banner)
    
    @staticmethod
    def display_menu(title: str, options: List[Tuple[str, str]], show_back: bool = True):
        """Display a menu with options"""
        print(f"\n{Fore.YELLOW}╔{'═' * 50}╗")
        print(f"║  {Fore.WHITE}{Style.BRIGHT}{title:<46}{Fore.YELLOW}  ║")
        print(f"╚{'═' * 50}╝{Style.RESET_ALL}\n")
        
        for key, label in options:
            icon = "🔹" if key.isdigit() else "🔸"
            print(f"  {icon} {Fore.CYAN}[{key}]{Style.RESET_ALL} {Fore.WHITE}{label}{Style.RESET_ALL}")
        
        if show_back:
            print(f"\n  🔙 {Fore.CYAN}[0]{Style.RESET_ALL} {Fore.WHITE}Back / Exit{Style.RESET_ALL}")
        
        print(f"\n{Fore.CYAN}{'─' * 52}{Style.RESET_ALL}")
    
    @staticmethod
    def display_status_box(title: str, items: List[Tuple[str, Any]]):
        """Display a status box with items"""
        print(f"\n{Fore.GREEN}┌{'─' * 50}┐")
        print(f"│  {Fore.WHITE}{Style.BRIGHT}{title:<46}{Fore.GREEN}  │")
        print(f"├{'─' * 50}┤{Style.RESET_ALL}")
        
        for label, value in items:
            value_str = str(value)[:30]
            padding = 44 - len(label) - len(value_str)
            print(f"{Fore.GREEN}│{Style.RESET_ALL}  {Fore.LIGHTBLACK_EX}{label}:{Style.RESET_ALL} {Fore.WHITE}{value_str}{' ' * max(0, padding)}{Fore.GREEN}│{Style.RESET_ALL}")
        
        print(f"{Fore.GREEN}└{'─' * 50}┘{Style.RESET_ALL}")
    
    @staticmethod
    def display_statistics_box(stats: Statistics):
        """Display statistics in a formatted box"""
        items = [
            ("📢 Total Broadcasts", f"{stats.successful_broadcasts}/{stats.total_broadcasts}"),
            ("💬 Private Replies", f"{stats.successful_private_replies}/{stats.total_private_replies}"),
            ("⚡ Group Reactions", f"{stats.successful_group_reactions}/{stats.total_group_reactions}"),
            ("💝 Private Reactions", f"{stats.successful_private_reactions}/{stats.total_private_reactions}"),
            ("🔄 Cycles Completed", stats.cycles_completed),
            ("📊 Groups Synced", stats.groups_synced),
            ("❌ Total Errors", stats.total_errors),
            ("⏳ Flood Waits", f"{stats.flood_waits} ({stats.total_flood_wait_time}s)"),
        ]
        
        UI.display_status_box("📊 BOT STATISTICS", items)
    
    @staticmethod
    def display_delay_config(delays: DelayConfig):
        """Display delay configuration"""
        items = [
            ("📢 Broadcast Delay", f"{delays.broadcast_min}-{delays.broadcast_max}s"),
            ("💬 Private Reply Delay", f"{delays.private_reply_min}-{delays.private_reply_max}s"),
            ("⚡ Group Reaction Delay", f"{delays.group_reaction_min}-{delays.group_reaction_max}s"),
            ("💝 Private Reaction Delay", f"{delays.private_reaction_min}-{delays.private_reaction_max}s"),
            ("🔄 Cycle Wait Time", f"{delays.cycle_wait_time}s ({delays.cycle_wait_time // 60}min)"),
            ("⏱️ Broadcast Check", f"{delays.broadcast_check_interval}s"),
            ("🔁 Group Sync", f"{delays.group_sync_interval}s"),
            ("⏳ Reply Cooldown", f"{delays.private_reply_cooldown}s"),
        ]
        
        UI.display_status_box("⏱️ DELAY CONFIGURATION", items)
    
    @staticmethod
    def get_input(prompt: str, color: str = Fore.CYAN) -> str:
        """Get user input with colored prompt"""
        return input(f"\n{color}→ {prompt}: {Style.RESET_ALL}").strip()
    
    @staticmethod
    def get_number_input(prompt: str, min_val: float = 0, max_val: float = float('inf'), 
                        default: Optional[float] = None) -> Optional[float]:
        """Get numeric input with validation"""
        try:
            default_str = f" [{default}]" if default is not None else ""
            raw = input(f"\n{Fore.CYAN}→ {prompt}{default_str}: {Style.RESET_ALL}").strip()
            
            if not raw and default is not None:
                return default
            
            value = float(raw)
            
            if min_val <= value <= max_val:
                return value
            else:
                logger.warning(f"Value must be between {min_val} and {max_val}")
                return None
                
        except ValueError:
            logger.warning("Invalid number input")
            return None
    
    @staticmethod
    def confirm(prompt: str, default: bool = False) -> bool:
        """Get yes/no confirmation"""
        default_str = "Y/n" if default else "y/N"
        response = input(f"\n{Fore.YELLOW}→ {prompt} [{default_str}]: {Style.RESET_ALL}").strip().lower()
        
        if not response:
            return default
        
        return response in ('y', 'yes', 'да', '1', 'true')
    
    @staticmethod
    def press_enter_to_continue():
        """Wait for user to press Enter"""
        input(f"\n{Fore.LIGHTBLACK_EX}Press Enter to continue...{Style.RESET_ALL}")
    
    @staticmethod
    def show_progress(current: int, total: int, prefix: str = "", suffix: str = "", width: int = 40):
        """Display a progress bar"""
        if total == 0:
            return
        
        percent = current / total
        filled = int(width * percent)
        bar = "█" * filled + "░" * (width - filled)
        
        print(f"\r{Fore.CYAN}{prefix} │{Fore.GREEN}{bar}{Fore.CYAN}│ {Fore.WHITE}{current}/{total} {Fore.LIGHTBLACK_EX}({percent:.1%}) {suffix}{Style.RESET_ALL}", end="")
        
        if current >= total:
            print()


# ══════════════════════════════════════════════════════════════════════════════
#                              CONFIGURATION MANAGER
# ══════════════════════════════════════════════════════════════════════════════

class ConfigManager:
    """Manage bot configuration"""
    
    def __init__(self, db: DatabaseManager):
        self.db = db
        self.delays = DelayConfig()
        self.features = FeatureConfig()
        self.credentials: Optional[Dict[str, str]] = None
        self._load_config()
    
    def _load_config(self):
        """Load configuration from database"""
        # Load delays
        delays_data = self.db.get_setting("delays")
        if delays_data:
            for key, value in delays_data.items():
                if hasattr(self.delays, key):
                    setattr(self.delays, key, value)
        
        # Load features
        features_data = self.db.get_setting("features")
        if features_data:
            for key, value in features_data.items():
                if hasattr(self.features, key):
                    setattr(self.features, key, value)
        
        # Load credentials
        self.credentials = self.db.get_setting("credentials")
    
    def save_config(self):
        """Save configuration to database"""
        self.db.save_setting("delays", asdict(self.delays))
        self.db.save_setting("features", asdict(self.features))
        
        if self.credentials:
            self.db.save_setting("credentials", self.credentials)
    
    def save_credentials(self, api_id: str, api_hash: str, phone: str):
        """Save Telegram credentials"""
        self.credentials = {
            "api_id": api_id,
            "api_hash": api_hash,
            "phone": phone
        }
        self.db.save_setting("credentials", self.credentials)
        logger.success("Credentials saved")
    
    def get_credentials(self) -> Optional[Tuple[str, str, str]]:
        """Get saved credentials"""
        if self.credentials:
            return (
                self.credentials.get("api_id"),
                self.credentials.get("api_hash"),
                self.credentials.get("phone")
            )
        return None
    
    def update_delay(self, delay_name: str, value: float) -> bool:
        """Update a delay setting"""
        if hasattr(self.delays, delay_name):
            setattr(self.delays, delay_name, value)
            self.save_config()
            return True
        return False
    
    def toggle_feature(self, feature_name: str) -> bool:
        """Toggle a feature on/off"""
        if hasattr(self.features, feature_name):
            current = getattr(self.features, feature_name)
            setattr(self.features, feature_name, not current)
            self.save_config()
            return True
        return False
    
    def export_config(self, filepath: str) -> bool:
        """Export configuration to file"""
        config = {
            "delays": asdict(self.delays),
            "features": asdict(self.features),
            "exported_at": datetime.now().isoformat()
        }
        return FileManager.write_json(filepath, config)
    
    def import_config(self, filepath: str) -> bool:
        """Import configuration from file"""
        config = FileManager.read_json(filepath)
        
        if config:
            if "delays" in config:
                for key, value in config["delays"].items():
                    if hasattr(self.delays, key):
                        setattr(self.delays, key, value)
            
            if "features" in config:
                for key, value in config["features"].items():
                    if hasattr(self.features, key):
                        setattr(self.features, key, value)
            
            self.save_config()
            return True
        
        return False


# ══════════════════════════════════════════════════════════════════════════════
#                              STATISTICS MANAGER
# ══════════════════════════════════════════════════════════════════════════════

class StatisticsManager:
    """Manage bot statistics"""
    
    def __init__(self, db: DatabaseManager):
        self.db = db
        self.stats = Statistics()
        self._load_stats()
        self._start_time = datetime.now()
    
    def _load_stats(self):
        """Load statistics from database"""
        db_stats = self.db.get_all_statistics()
        
        for key, value in db_stats.items():
            if hasattr(self.stats, key):
                setattr(self.stats, key, value)
    
    def save_stats(self):
        """Save statistics to database"""
        for field_name, value in asdict(self.stats).items():
            if isinstance(value, (int, float)):
                self.db.update_statistic(field_name, value, increment=False)
    
    def increment(self, stat_name: str, value: int = 1):
        """Increment a statistic"""
        if hasattr(self.stats, stat_name):
            current = getattr(self.stats, stat_name)
            setattr(self.stats, stat_name, current + value)
            self.db.update_statistic(stat_name, value, increment=True)
    
    def record_broadcast(self, success: bool):
        """Record a broadcast attempt"""
        self.increment("total_broadcasts")
        if success:
            self.increment("successful_broadcasts")
        else:
            self.increment("failed_broadcasts")
    
    def record_private_reply(self, success: bool):
        """Record a private reply attempt"""
        self.increment("total_private_replies")
        if success:
            self.increment("successful_private_replies")
        else:
            self.increment("failed_private_replies")
    
    def record_group_reaction(self, success: bool):
        """Record a group reaction attempt"""
        self.increment("total_group_reactions")
        if success:
            self.increment("successful_group_reactions")
        else:
            self.increment("failed_group_reactions")
    
    def record_private_reaction(self, success: bool):
        """Record a private reaction attempt"""
        self.increment("total_private_reactions")
        if success:
            self.increment("successful_private_reactions")
        else:
            self.increment("failed_private_reactions")
    
    def record_error(self):
        """Record an error"""
        self.increment("total_errors")
    
    def record_flood_wait(self, seconds: int):
        """Record a flood wait"""
        self.increment("flood_waits")
        self.increment("total_flood_wait_time", seconds)
    
    def record_cycle_complete(self):
        """Record a broadcast cycle completion"""
        self.increment("cycles_completed")
        self.stats.last_cycle_time = datetime.now().isoformat()
    
    def record_group_sync(self, count: int):
        """Record a group sync"""
        self.stats.groups_synced = count
        self.stats.last_sync_time = datetime.now().isoformat()
    
    def get_uptime(self) -> str:
        """Get formatted uptime"""
        delta = datetime.now() - self._start_time
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours}h {minutes}m {seconds}s"
    
    def get_summary(self) -> Dict[str, Any]:
        """Get statistics summary"""
        return {
            "uptime": self.get_uptime(),
            "broadcasts": f"{self.stats.successful_broadcasts}/{self.stats.total_broadcasts}",
            "private_replies": f"{self.stats.successful_private_replies}/{self.stats.total_private_replies}",
            "group_reactions": f"{self.stats.successful_group_reactions}/{self.stats.total_group_reactions}",
            "private_reactions": f"{self.stats.successful_private_reactions}/{self.stats.total_private_reactions}",
            "errors": self.stats.total_errors,
            "cycles": self.stats.cycles_completed,
            "groups": self.stats.groups_synced,
        }
    
    def reset_stats(self):
        """Reset all statistics"""
        self.stats = Statistics()
        self.stats.bot_start_time = datetime.now().isoformat()
        self.save_stats()


# ══════════════════════════════════════════════════════════════════════════════
#                              TELEGRAM BOT CORE
# ══════════════════════════════════════════════════════════════════════════════

class VanshBot:
    """Main Telegram bot class"""
    
    def __init__(self):
        # Initialize managers
        FileManager.ensure_directories()
        
        self.db = DatabaseManager(FILES["database"])
        self.config = ConfigManager(self.db)
        self.statistics = StatisticsManager(self.db)
        self.rate_limiter = RateLimiter()
        
        # Bot state
        self.status = BotStatus.STOPPED
        self.client: Optional[TelegramClient] = None
        self.me: Optional[User] = None
        self.me_id: Optional[int] = None
        self.me_username: Optional[str] = None
        
        # Runtime state
        self.groups: List[GroupInfo] = []
        self.sent_to_group: Dict[int, int] = {}
        self.last_private_reply: Dict[int, float] = {}
        self.last_private_reaction: Dict[int, float] = {}
        
        # Tasks
        self._tasks: List[asyncio.Task] = []
        self._stop_event = asyncio.Event()
    
    # ══════════════════════════════════════════════════════════════════════════
    #                              AUTHENTICATION
    # ══════════════════════════════════════════════════════════════════════════
    
    async def setup_credentials(self) -> bool:
        """Setup or load API credentials"""
        credentials = self.config.get_credentials()
        
        if credentials:
            api_id, api_hash, phone = credentials
            if api_id and api_hash and phone:
                logger.info(f"Found saved credentials for: {phone}")
                
                if UI.confirm("Use saved credentials?", default=True):
                    return await self._create_client(api_id, api_hash, phone)
        
        # Get new credentials
        logger.header("TELEGRAM API SETUP")
        print(f"{Fore.LIGHTBLACK_EX}Get your API credentials from: https://my.telegram.org{Style.RESET_ALL}")
        print()
        
        api_id = UI.get_input("Enter API ID")
        api_hash = UI.get_input("Enter API Hash")
        phone = UI.get_input("Enter Phone Number (with country code)")
        
        if not all([api_id, api_hash, phone]):
            logger.error("All fields are required")
            return False
        
        # Save credentials
        self.config.save_credentials(api_id, api_hash, phone)
        
        return await self._create_client(api_id, api_hash, phone)
    
    async def _create_client(self, api_id: str, api_hash: str, phone: str) -> bool:
        """Create and authorize Telegram client"""
        try:
            api_id_int = int(api_id)
        except ValueError:
            logger.error("Invalid API ID - must be a number")
            return False
        
        # Create session file
        session_name = f"sessions/session_{phone.replace('+', '').replace(' ', '')}"
        
        self.client = TelegramClient(session_name, api_id_int, api_hash)
        
        try:
            await self.client.connect()
            
            if not await self.client.is_user_authorized():
                logger.info("Sending verification code...")
                await self.client.send_code_request(phone)
                
                code = UI.get_input("Enter verification code")
                
                try:
                    await self.client.sign_in(phone=phone, code=code)
                except SessionPasswordNeededError:
                    password = UI.get_input("Enter 2FA password")
                    await self.client.sign_in(password=password)
                except PhoneCodeInvalidError:
                    logger.error("Invalid verification code")
                    return False
            
            # Get user info
            self.me = await self.client.get_me()
            self.me_id = self.me.id
            self.me_username = self.me.username
            
            name = self.me.first_name or self.me.username or str(self.me.id)
            logger.success(f"Logged in as: {name}")
            
            return True
            
        except AuthKeyUnregisteredError:
            logger.error("Session expired. Please re-authenticate.")
            # Remove old session
            session_file = f"{session_name}.session"
            if os.path.exists(session_file):
                os.remove(session_file)
            return False
            
        except UserDeactivatedError:
            logger.critical("Account has been deactivated by Telegram")
            return False
            
        except PhoneNumberBannedError:
            logger.critical("This phone number is banned by Telegram")
            return False
            
        except Exception as e:
            logger.error(f"Authentication failed: {e}")
            return False
    
    # ══════════════════════════════════════════════════════════════════════════
    #                              GROUP MANAGEMENT
    # ══════════════════════════════════════════════════════════════════════════
    
    async def sync_groups(self) -> int:
        """Sync all joined groups"""
        if not self.client:
            return 0
        
        try:
            dialogs = await self.client.get_dialogs()
            groups = []
            
            for dialog in dialogs:
                if dialog.is_group:
                    group_info = GroupInfo(
                        id=dialog.entity.id,
                        title=getattr(dialog.entity, 'title', 'Unknown'),
                        username=getattr(dialog.entity, 'username', None),
                        is_megagroup=getattr(dialog.entity, 'megagroup', False),
                        is_active=True
                    )
                    groups.append(group_info)
                    self.db.save_group(group_info)
                
                elif dialog.is_channel and hasattr(dialog.entity, 'megagroup') and dialog.entity.megagroup:
                    group_info = GroupInfo(
                        id=dialog.entity.id,
                        title=getattr(dialog.entity, 'title', 'Unknown'),
                        username=getattr(dialog.entity, 'username', None),
                        is_megagroup=True,
                        is_active=True
                    )
                    groups.append(group_info)
                    self.db.save_group(group_info)
            
            self.groups = groups
            self.statistics.record_group_sync(len(groups))
            
            # Clean up old sent markers
            current_ids = {g.id for g in groups}
            for gid in list(self.sent_to_group.keys()):
                if gid not in current_ids:
                    del self.sent_to_group[gid]
            
            logger.success(f"Synced {len(groups)} groups")
            return len(groups)
            
        except FloodWaitError as e:
            wait_time = await ErrorHandler.handle_flood_wait(e)
            self.statistics.record_flood_wait(wait_time)
            return await self.sync_groups()
            
        except Exception as e:
            logger.error(f"Group sync error: {e}")
            self.statistics.record_error()
            return 0
    
    async def get_group_list(self) -> List[GroupInfo]:
        """Get list of all groups"""
        if not self.groups:
            await self.sync_groups()
        return self.groups
    
    # ══════════════════════════════════════════════════════════════════════════
    #                              SAVED MESSAGES
    # ══════════════════════════════════════════════════════════════════════════
    
    async def get_latest_saved_message(self) -> Optional[Message]:
        """Get the latest message from Saved Messages"""
        if not self.client:
            return None
        
        try:
            messages = await self.client.get_messages("me", limit=1)
            if messages and len(messages) > 0:
                return messages[0]
        except Exception as e:
            logger.error(f"Error getting saved message: {e}")
        
        return None
    
    # ══════════════════════════════════════════════════════════════════════════
    #                              BROADCASTING
    # ══════════════════════════════════════════════════════════════════════════
    
    async def broadcast_to_group(self, group: GroupInfo, message: Message) -> bool:
        """Broadcast message to a specific group"""
        if not self.client:
            return False
        
        try:
            # Rate limiting
            await self.rate_limiter.acquire()
            
            # Random delay
            delay = self.config.delays.get_broadcast_delay()
            await asyncio.sleep(delay)
            
            # Forward the message
            await self.client.forward_messages(group.id, message.id, from_peer="me")
            
            # Update tracking
            self.sent_to_group[group.id] = message.id
            self.db.update_group_broadcast(group.id, message.id, success=True)
            self.statistics.record_broadcast(success=True)
            
            logger.action(ActionType.BROADCAST, f"{group.title[:40]}", success=True)
            return True
            
        except FloodWaitError as e:
            wait_time = await ErrorHandler.handle_flood_wait(e, self.config.delays.flood_wait_buffer)
            self.statistics.record_flood_wait(wait_time)
            return await self.broadcast_to_group(group, message)
            
        except SlowModeWaitError as e:
            logger.warning(f"Slow mode in {group.title[:30]}: Wait {e.seconds}s")
            return False
            
        except (ChatWriteForbiddenError, UserBannedInChannelError, ChannelPrivateError) as e:
            error_msg = ErrorHandler.get_friendly_message(e)
            logger.warning(f"{group.title[:30]}: {error_msg}")
            self.db.update_group_broadcast(group.id, message.id, success=False, error=error_msg)
            self.statistics.record_broadcast(success=False)
            return False
            
        except Exception as e:
            error_msg = str(e)[:50]
            logger.error(f"Broadcast failed: {group.title[:30]} - {error_msg}")
            self.db.update_group_broadcast(group.id, message.id, success=False, error=error_msg)
            self.statistics.record_broadcast(success=False)
            self.statistics.record_error()
            return False
    
    async def broadcast_to_all_groups(self) -> Tuple[int, int]:
        """Broadcast latest saved message to all groups"""
        if not self.config.features.enable_broadcast:
            return 0, 0
        
        message = await self.get_latest_saved_message()
        if not message:
            logger.warning("No message in Saved Messages")
            return 0, 0
        
        groups = await self.get_group_list()
        if not groups:
            logger.warning("No groups to broadcast to")
            return 0, 0
        
        successful = 0
        failed = 0
        
        logger.header("BROADCASTING")
        
        for i, group in enumerate(groups):
            if self.status != BotStatus.RUNNING:
                break
            
            # Check if already sent
            last_sent = self.sent_to_group.get(group.id)
            if last_sent == message.id:
                continue
            
            if await self.broadcast_to_group(group, message):
                successful += 1
            else:
                failed += 1
            
            # Show progress
            total = len(groups)
            UI.show_progress(i + 1, total, "Progress", f"✓{successful} ✗{failed}")
        
        print()  # New line after progress
        logger.success(f"Broadcast complete: {successful} successful, {failed} failed")
        
        return successful, failed
    
    # ══════════════════════════════════════════════════════════════════════════
    #                              PRIVATE MESSAGES
    # ══════════════════════════════════════════════════════════════════════════
    
    async def handle_private_message(self, event) -> bool:
        """Handle incoming private message with auto-reply and reaction"""
        if not self.client:
            return False
        
        try:
            sender = await event.get_sender()
            
            # Skip bots
            if getattr(sender, "bot", False):
                return False
            
            user_id = event.sender_id
            if not user_id or user_id == self.me_id:
                return False
            
            # Save user info
            user_info = UserInfo(
                id=user_id,
                first_name=getattr(sender, 'first_name', None),
                last_name=getattr(sender, 'last_name', None),
                username=getattr(sender, 'username', None),
                is_bot=getattr(sender, 'bot', False),
                last_message_time=datetime.now().isoformat()
            )
            self.db.save_user(user_info)
            
            # Check if user is blacklisted
            saved_user = self.db.get_user(user_id)
            if saved_user and saved_user.is_blacklisted:
                return False
            
            success = False
            
            # Handle auto-reaction to private message
            if self.config.features.enable_private_reactions:
                reaction_success = await self._send_private_reaction(event, user_id)
                if reaction_success:
                    success = True
            
            # Handle auto-reply
            if self.config.features.enable_private_reply:
                reply_success = await self._send_private_reply(event, user_id, sender)
                if reply_success:
                    success = True
            
            return success
            
        except Exception as e:
            logger.error(f"Private message handler error: {e}")
            self.statistics.record_error()
            return False
    
    async def _send_private_reaction(self, event, user_id: int) -> bool:
        """Send reaction to private message"""
        try:
            # Check cooldown (shorter than reply cooldown)
            now = time.time()
            last_time = self.last_private_reaction.get(user_id, 0)
            cooldown = 30  # 30 second cooldown for reactions
            
            if now - last_time < cooldown:
                return False
            
            # Random delay
            delay = self.config.delays.get_private_reaction_delay()
            await asyncio.sleep(delay)
            
            # Select random positive reaction
            emoji = random.choice(PRIVATE_REACTIONS)
            peer = await event.get_input_chat()
            
            await self.client(
                SendReactionRequest(
                    peer=peer,
                    msg_id=event.message.id,
                    reaction=[ReactionEmoji(emoticon=emoji)]
                )
            )
            
            self.last_private_reaction[user_id] = now
            self.db.update_user_reaction(user_id)
            self.statistics.record_private_reaction(success=True)
            
            name = getattr(await event.get_sender(), 'first_name', 'User')
            logger.action(ActionType.PRIVATE_REACTION, f"{emoji} to {name[:20]}", success=True)
            
            return True
            
        except FloodWaitError as e:
            wait_time = await ErrorHandler.handle_flood_wait(e)
            self.statistics.record_flood_wait(wait_time)
            return False
            
        except Exception as e:
            self.statistics.record_private_reaction(success=False)
            return False
    
    async def _send_private_reply(self, event, user_id: int, sender) -> bool:
        """Send auto-reply to private message"""
        try:
            # Check cooldown
            now = time.time()
            last_time = self.last_private_reply.get(user_id, 0)
            
            if now - last_time < self.config.delays.private_reply_cooldown:
                return False
            
            # Get saved message
            saved_msg = await self.get_latest_saved_message()
            if not saved_msg:
                return False
            
            # Random delay
            delay = self.config.delays.get_private_reply_delay()
            await asyncio.sleep(delay)
            
            # Rate limiting
            await self.rate_limiter.acquire()
            
            # Forward saved message as reply
            await self.client.forward_messages(event.chat_id, saved_msg.id, from_peer="me")
            
            self.last_private_reply[user_id] = now
            self.db.update_user_reply(user_id)
            self.statistics.record_private_reply(success=True)
            
            name = getattr(sender, 'first_name', 'Unknown')
            logger.action(ActionType.PRIVATE_REPLY, f"Replied to {name[:20]}", success=True)
            
            return True
            
        except FloodWaitError as e:
            wait_time = await ErrorHandler.handle_flood_wait(e)
            self.statistics.record_flood_wait(wait_time)
            return False
            
        except Exception as e:
            logger.error(f"Private reply error: {e}")
            self.statistics.record_private_reply(success=False)
            self.statistics.record_error()
            return False
    
    # ══════════════════════════════════════════════════════════════════════════
    #                              GROUP REACTIONS
    # ══════════════════════════════════════════════════════════════════════════
    
    async def handle_group_mention(self, event) -> bool:
        """Handle group mention or reply with reaction"""
        if not self.config.features.enable_group_reactions:
            return False
        
        if not self.client:
            return False
        
        try:
            # Random delay
            delay = self.config.delays.get_group_reaction_delay()
            await asyncio.sleep(delay)
            
            # Select random reaction
            emoji = random.choice(DEFAULT_REACTIONS)
            peer = await event.get_input_chat()
            
            await self.client(
                SendReactionRequest(
                    peer=peer,
                    msg_id=event.message.id,
                    reaction=[ReactionEmoji(emoticon=emoji)]
                )
            )
            
            self.statistics.record_group_reaction(success=True)
            
            chat = await event.get_chat()
            chat_title = getattr(chat, 'title', 'Unknown')[:30]
            
            logger.action(ActionType.GROUP_REACTION, f"{emoji} in {chat_title}", success=True)
            
            return True
            
        except FloodWaitError as e:
            wait_time = await ErrorHandler.handle_flood_wait(e)
            self.statistics.record_flood_wait(wait_time)
            return False
            
        except Exception:
            self.statistics.record_group_reaction(success=False)
            return False
    
    # ══════════════════════════════════════════════════════════════════════════
    #                              BACKGROUND TASKS
    # ══════════════════════════════════════════════════════════════════════════
    
    async def _broadcast_loop(self):
        """Background task for continuous broadcasting"""
        while self.status == BotStatus.RUNNING:
            try:
                if not self._stop_event.is_set():
                    await self.broadcast_to_all_groups()
                    self.statistics.record_cycle_complete()
                    
                    # Wait for cycle time
                    cycle_wait = self.config.delays.cycle_wait_time
                    logger.info(f"Cycle complete. Next cycle in {cycle_wait // 60} minutes")
                    
                    # Wait with check for stop event
                    for _ in range(cycle_wait):
                        if self._stop_event.is_set():
                            break
                        await asyncio.sleep(1)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Broadcast loop error: {e}")
                self.statistics.record_error()
                await asyncio.sleep(self.config.delays.error_retry_delay)
    
    async def _group_sync_loop(self):
        """Background task for periodic group syncing"""
        while self.status == BotStatus.RUNNING:
            try:
                # Wait first, then sync
                for _ in range(self.config.delays.group_sync_interval):
                    if self._stop_event.is_set():
                        break
                    await asyncio.sleep(1)
                
                if not self._stop_event.is_set():
                    await self.sync_groups()
                    
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Group sync loop error: {e}")
                self.statistics.record_error()
                await asyncio.sleep(self.config.delays.error_retry_delay)
    
    async def _status_update_loop(self):
        """Background task for periodic status updates"""
        while self.status == BotStatus.RUNNING:
            try:
                # Update every 5 minutes
                for _ in range(300):
                    if self._stop_event.is_set():
                        break
                    await asyncio.sleep(1)
                
                if not self._stop_event.is_set():
                    summary = self.statistics.get_summary()
                    logger.info(f"Status: Up {summary['uptime']} | Broadcasts: {summary['broadcasts']} | Cycles: {summary['cycles']}")
                    
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Status update error: {e}")
    
    # ══════════════════════════════════════════════════════════════════════════
    #                              BOT CONTROL
    # ══════════════════════════════════════════════════════════════════════════
    
    async def start(self):
        """Start the bot"""
        if self.status == BotStatus.RUNNING:
            logger.warning("Bot is already running")
            return
        
        if not self.client:
            logger.error("Client not initialized")
            return
        
        UI.clear_screen()
        UI.display_mini_banner()
        
        logger.header("STARTING BOT")
        
        self.status = BotStatus.STARTING
        self._stop_event.clear()
        
        # Update statistics
        self.statistics.stats.bot_start_time = datetime.now().isoformat()
        
        # Initial group sync
        await self.sync_groups()
        
        # Display configuration
        logger.divider()
        logger.status_line("Broadcast Delay", f"{self.config.delays.broadcast_min}-{self.config.delays.broadcast_max}s")
        logger.status_line("Cycle Wait Time", f"{self.config.delays.cycle_wait_time}s ({self.config.delays.cycle_wait_time // 60} min)")
        logger.status_line("Reply Cooldown", f"{self.config.delays.private_reply_cooldown}s")
        logger.status_line("Groups", len(self.groups))
        logger.divider()
        
        # Register event handlers
        @self.client.on(events.NewMessage(incoming=True))
        async def on_new_message(event):
            if not self.status == BotStatus.RUNNING:
                return
            
            if event.sender_id == self.me_id:
                return
            
            # Handle private messages
            if event.is_private:
                await self.handle_private_message(event)
                return
            
            # Handle group messages (mentions/replies)
            if event.is_group:
                should_react = bool(getattr(event.message, "mentioned", False))
                
                if not should_react and event.message.is_reply:
                    try:
                        reply_msg = await event.get_reply_message()
                        if reply_msg and reply_msg.sender_id == self.me_id:
                            should_react = True
                    except:
                        pass
                
                if should_react:
                    await self.handle_group_mention(event)
        
        # Start background tasks
        self._tasks = [
            asyncio.create_task(self._broadcast_loop()),
            asyncio.create_task(self._group_sync_loop()),
            asyncio.create_task(self._status_update_loop()),
        ]
        
        self.status = BotStatus.RUNNING
        
        print()
        logger.success("BOT IS RUNNING")
        print(f"\n{Fore.YELLOW}Press Ctrl+C to stop{Style.RESET_ALL}\n")
        logger.divider()
        
        try:
            await self.client.run_until_disconnected()
        except KeyboardInterrupt:
            pass
        finally:
            await self.stop()
    
    async def stop(self):
        """Stop the bot"""
        if self.status == BotStatus.STOPPED:
            return
        
        logger.info("Stopping bot...")
        self.status = BotStatus.STOPPING
        self._stop_event.set()
        
        # Cancel all tasks
        for task in self._tasks:
            if not task.done():
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass
        
        self._tasks.clear()
        
        # Save statistics
        self.statistics.save_stats()
        
        self.status = BotStatus.STOPPED
        logger.success("Bot stopped")
    
    async def disconnect(self):
        """Disconnect from Telegram"""
        if self.client:
            await self.client.disconnect()
            logger.info("Disconnected from Telegram")


# ══════════════════════════════════════════════════════════════════════════════
#                              MENU HANDLERS
# ══════════════════════════════════════════════════════════════════════════════

class MenuHandler:
    """Handle menu interactions"""
    
    def __init__(self, bot: VanshBot):
        self.bot = bot
    
    async def main_menu(self):
        """Display and handle main menu"""
        while True:
            UI.clear_screen()
            UI.display_banner()
            
            # Show current status
            status_items = [
                ("Status", "Ready" if self.bot.client else "Not Connected"),
                ("Groups", len(self.bot.groups)),
                ("Uptime", self.bot.statistics.get_uptime() if self.bot.statistics.stats.bot_start_time else "N/A"),
            ]
            UI.display_status_box("📊 CURRENT STATUS", status_items)
            
            options = [
                ("1", "🚀 Start Bot"),
                ("2", "⏱️  Configure Delays"),
                ("3", "🔧 Toggle Features"),
                ("4", "📊 View Statistics"),
                ("5", "🔄 Sync Groups"),
                ("6", "📋 View Groups"),
                ("7", "💾 Export/Import Config"),
                ("8", "🗑️  Reset Statistics"),
            ]
            
            UI.display_menu("MAIN MENU", options)
            
            choice = UI.get_input("Select option")
            
            if choice == '0':
                if UI.confirm("Exit the bot?"):
                    if self.bot.client:
                        await self.bot.disconnect()
                    logger.success("Goodbye!")
                    break
            
            elif choice == '1':
                try:
                    await self.bot.start()
                except KeyboardInterrupt:
                    pass
                UI.press_enter_to_continue()
            
            elif choice == '2':
                await self.delay_config_menu()
            
            elif choice == '3':
                await self.feature_toggle_menu()
            
            elif choice == '4':
                await self.view_statistics()
            
            elif choice == '5':
                logger.info("Syncing groups...")
                count = await self.bot.sync_groups()
                logger.success(f"Synced {count} groups")
                UI.press_enter_to_continue()
            
            elif choice == '6':
                await self.view_groups()
            
            elif choice == '7':
                await self.export_import_menu()
            
            elif choice == '8':
                if UI.confirm("Reset all statistics?"):
                    self.bot.statistics.reset_stats()
                    logger.success("Statistics reset")
                UI.press_enter_to_continue()
    
    async def delay_config_menu(self):
        """Configure delay settings"""
        while True:
            UI.clear_screen()
            UI.display_mini_banner()
            
            UI.display_delay_config(self.bot.config.delays)
            
            options = [
                ("1", "📢 Broadcast Delay (min-max)"),
                ("2", "💬 Private Reply Delay (min-max)"),
                ("3", "⚡ Group Reaction Delay (min-max)"),
                ("4", "💝 Private Reaction Delay (min-max)"),
                ("5", "🔄 Cycle Wait Time"),
                ("6", "⏱️  Broadcast Check Interval"),
                ("7", "🔁 Group Sync Interval"),
                ("8", "⏳ Private Reply Cooldown"),
            ]
            
            UI.display_menu("DELAY CONFIGURATION", options)
            
            choice = UI.get_input("Select option")
            
            if choice == '0':
                break
            
            elif choice == '1':
                min_val = UI.get_number_input("Min broadcast delay (seconds)", 0.5, 60, self.bot.config.delays.broadcast_min)
                max_val = UI.get_number_input("Max broadcast delay (seconds)", 0.5, 120, self.bot.config.delays.broadcast_max)
                
                if min_val and max_val and min_val <= max_val:
                    self.bot.config.delays.broadcast_min = min_val
                    self.bot.config.delays.broadcast_max = max_val
                    self.bot.config.save_config()
                    logger.success(f"Set to {min_val}-{max_val}s")
                else:
                    logger.error("Invalid values")
                UI.press_enter_to_continue()
            
            elif choice == '2':
                min_val = UI.get_number_input("Min private reply delay (seconds)", 0.5, 60, self.bot.config.delays.private_reply_min)
                max_val = UI.get_number_input("Max private reply delay (seconds)", 0.5, 120, self.bot.config.delays.private_reply_max)
                
                if min_val and max_val and min_val <= max_val:
                    self.bot.config.delays.private_reply_min = min_val
                    self.bot.config.delays.private_reply_max = max_val
                    self.bot.config.save_config()
                    logger.success(f"Set to {min_val}-{max_val}s")
                else:
                    logger.error("Invalid values")
                UI.press_enter_to_continue()
            
            elif choice == '3':
                min_val = UI.get_number_input("Min group reaction delay (seconds)", 0.1, 30, self.bot.config.delays.group_reaction_min)
                max_val = UI.get_number_input("Max group reaction delay (seconds)", 0.1, 60, self.bot.config.delays.group_reaction_max)
                
                if min_val and max_val and min_val <= max_val:
                    self.bot.config.delays.group_reaction_min = min_val
                    self.bot.config.delays.group_reaction_max = max_val
                    self.bot.config.save_config()
                    logger.success(f"Set to {min_val}-{max_val}s")
                else:
                    logger.error("Invalid values")
                UI.press_enter_to_continue()
            
            elif choice == '4':
                min_val = UI.get_number_input("Min private reaction delay (seconds)", 0.1, 30, self.bot.config.delays.private_reaction_min)
                max_val = UI.get_number_input("Max private reaction delay (seconds)", 0.1, 60, self.bot.config.delays.private_reaction_max)
                
                if min_val and max_val and min_val <= max_val:
                    self.bot.config.delays.private_reaction_min = min_val
                    self.bot.config.delays.private_reaction_max = max_val
                    self.bot.config.save_config()
                    logger.success(f"Set to {min_val}-{max_val}s")
                else:
                    logger.error("Invalid values")
                UI.press_enter_to_continue()
            
            elif choice == '5':
                val = UI.get_number_input("Cycle wait time (seconds)", 60, 3600, self.bot.config.delays.cycle_wait_time)
                if val:
                    self.bot.config.delays.cycle_wait_time = int(val)
                    self.bot.config.save_config()
                    logger.success(f"Set to {int(val)}s ({int(val) // 60} minutes)")
                UI.press_enter_to_continue()
            
            elif choice == '6':
                val = UI.get_number_input("Broadcast check interval (seconds)", 5, 300, self.bot.config.delays.broadcast_check_interval)
                if val:
                    self.bot.config.delays.broadcast_check_interval = int(val)
                    self.bot.config.save_config()
                    logger.success(f"Set to {int(val)}s")
                UI.press_enter_to_continue()
            
            elif choice == '7':
                val = UI.get_number_input("Group sync interval (seconds)", 60, 3600, self.bot.config.delays.group_sync_interval)
                if val:
                    self.bot.config.delays.group_sync_interval = int(val)
                    self.bot.config.save_config()
                    logger.success(f"Set to {int(val)}s")
                UI.press_enter_to_continue()
            
            elif choice == '8':
                val = UI.get_number_input("Private reply cooldown (seconds)", 10, 3600, self.bot.config.delays.private_reply_cooldown)
                if val:
                    self.bot.config.delays.private_reply_cooldown = int(val)
                    self.bot.config.save_config()
                    logger.success(f"Set to {int(val)}s")
                UI.press_enter_to_continue()
    
    async def feature_toggle_menu(self):
        """Toggle feature settings"""
        while True:
            UI.clear_screen()
            UI.display_mini_banner()
            
            features = self.bot.config.features
            
            items = [
                ("Broadcasting", "✅ ON" if features.enable_broadcast else "❌ OFF"),
                ("Private Reply", "✅ ON" if features.enable_private_reply else "❌ OFF"),
                ("Group Reactions", "✅ ON" if features.enable_group_reactions else "❌ OFF"),
                ("Private Reactions", "✅ ON" if features.enable_private_reactions else "❌ OFF"),
                ("Statistics", "✅ ON" if features.enable_statistics else "❌ OFF"),
                ("Logging", "✅ ON" if features.enable_logging else "❌ OFF"),
                ("Auto Sync", "✅ ON" if features.enable_auto_sync else "❌ OFF"),
                ("Rate Limiting", "✅ ON" if features.enable_rate_limiting else "❌ OFF"),
            ]
            
            UI.display_status_box("🔧 FEATURE STATUS", items)
            
            options = [
                ("1", "📢 Toggle Broadcasting"),
                ("2", "💬 Toggle Private Reply"),
                ("3", "⚡ Toggle Group Reactions"),
                ("4", "💝 Toggle Private Reactions"),
                ("5", "📊 Toggle Statistics"),
                ("6", "📝 Toggle Logging"),
                ("7", "🔄 Toggle Auto Sync"),
                ("8", "⏱️  Toggle Rate Limiting"),
            ]
            
            UI.display_menu("TOGGLE FEATURES", options)
            
            choice = UI.get_input("Select option")
            
            if choice == '0':
                break
            
            feature_map = {
                '1': 'enable_broadcast',
                '2': 'enable_private_reply',
                '3': 'enable_group_reactions',
                '4': 'enable_private_reactions',
                '5': 'enable_statistics',
                '6': 'enable_logging',
                '7': 'enable_auto_sync',
                '8': 'enable_rate_limiting',
            }
            
            if choice in feature_map:
                feature = feature_map[choice]
                self.bot.config.toggle_feature(feature)
                new_state = getattr(self.bot.config.features, feature)
                logger.success(f"{feature} is now {'ON' if new_state else 'OFF'}")
                await asyncio.sleep(0.5)
    
    async def view_statistics(self):
        """View bot statistics"""
        UI.clear_screen()
        UI.display_mini_banner()
        
        UI.display_statistics_box(self.bot.statistics.stats)
        
        # Additional info
        summary = self.bot.statistics.get_summary()
        
        print(f"\n{Fore.CYAN}Additional Information:{Style.RESET_ALL}")
        print(f"  • Uptime: {Fore.WHITE}{summary['uptime']}{Style.RESET_ALL}")
        print(f"  • Last Sync: {Fore.WHITE}{self.bot.statistics.stats.last_sync_time or 'Never'}{Style.RESET_ALL}")
        print(f"  • Last Cycle: {Fore.WHITE}{self.bot.statistics.stats.last_cycle_time or 'Never'}{Style.RESET_ALL}")
        
        UI.press_enter_to_continue()
    
    async def view_groups(self):
        """View all groups"""
        UI.clear_screen()
        UI.display_mini_banner()
        
        groups = await self.bot.get_group_list()
        
        if not groups:
            logger.warning("No groups found. Try syncing first.")
            UI.press_enter_to_continue()
            return
        
        print(f"\n{Fore.YELLOW}╔{'═' * 60}╗")
        print(f"║  {Fore.WHITE}{Style.BRIGHT}{'GROUPS LIST':<56}{Fore.YELLOW}  ║")
        print(f"╚{'═' * 60}╝{Style.RESET_ALL}\n")
        
        for i, group in enumerate(groups, 1):
            username = f"@{group.username}" if group.username else "No username"
            status = "✅" if group.is_active else "❌"
            print(f"  {status} {Fore.CYAN}[{i:3}]{Style.RESET_ALL} {Fore.WHITE}{group.title[:35]:<35}{Style.RESET_ALL} {Fore.LIGHTBLACK_EX}{username}{Style.RESET_ALL}")
        
        print(f"\n{Fore.CYAN}Total: {len(groups)} groups{Style.RESET_ALL}")
        
        UI.press_enter_to_continue()
    
    async def export_import_menu(self):
        """Export/Import configuration"""
        while True:
            UI.clear_screen()
            UI.display_mini_banner()
            
            options = [
                ("1", "📤 Export Configuration"),
                ("2", "📥 Import Configuration"),
                ("3", "💾 Backup Database"),
            ]
            
            UI.display_menu("EXPORT / IMPORT", options)
            
            choice = UI.get_input("Select option")
            
            if choice == '0':
                break
            
            elif choice == '1':
                filepath = UI.get_input("Export filepath", Fore.WHITE) or "config_export.json"
                if self.bot.config.export_config(filepath):
                    logger.success(f"Configuration exported to {filepath}")
                else:
                    logger.error("Export failed")
                UI.press_enter_to_continue()
            
            elif choice == '2':
                filepath = UI.get_input("Import filepath", Fore.WHITE) or "config_export.json"
                if os.path.exists(filepath):
                    if self.bot.config.import_config(filepath):
                        logger.success("Configuration imported successfully")
                    else:
                        logger.error("Import failed")
                else:
                    logger.error("File not found")
                UI.press_enter_to_continue()
            
            elif choice == '3':
                if FileManager.backup_file(FILES["database"]):
                    logger.success("Database backed up to backups/ folder")
                else:
                    logger.error("Backup failed")
                UI.press_enter_to_continue()


# ══════════════════════════════════════════════════════════════════════════════
#                              APPLICATION ENTRY
# ══════════════════════════════════════════════════════════════════════════════

class Application:
    """Main application class"""
    
    def __init__(self):
        self.bot: Optional[VanshBot] = None
        self.menu_handler: Optional[MenuHandler] = None
    
    async def initialize(self) -> bool:
        """Initialize the application"""
        UI.clear_screen()
        UI.display_banner()
        
        # Create bot instance
        self.bot = VanshBot()
        
        # Setup credentials and authenticate
        if not await self.bot.setup_credentials():
            logger.error("Failed to setup credentials")
            return False
        
        # Create menu handler
        self.menu_handler = MenuHandler(self.bot)
        
        return True
    
    async def run(self):
        """Run the application"""
        try:
            if await self.initialize():
                await self.menu_handler.main_menu()
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Interrupted by user{Style.RESET_ALL}")
        except Exception as e:
            logger.critical(f"Application error: {e}")
            traceback.print_exc()
        finally:
            await self.cleanup()
    
    async def cleanup(self):
        """Cleanup resources"""
        if self.bot:
            await self.bot.stop()
            await self.bot.disconnect()


async def main():
    """Main entry point"""
    app = Application()
    await app.run()


# ══════════════════════════════════════════════════════════════════════════════
#                              SIGNAL HANDLERS
# ══════════════════════════════════════════════════════════════════════════════

def setup_signal_handlers():
    """Setup signal handlers for graceful shutdown"""
    def signal_handler(signum, frame):
        print(f"\n{Fore.YELLOW}Received signal {signum}. Shutting down...{Style.RESET_ALL}")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)


# ══════════════════════════════════════════════════════════════════════════════
#                              ENTRY POINT
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    # Setup signal handlers
    setup_signal_handlers()
    
    # Check Python version
    if sys.version_info < (3, 8):
        print(f"{Fore.RED}Python 3.8 or higher is required{Style.RESET_ALL}")
        sys.exit(1)
    
    # Run the application
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Program interrupted{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Critical error: {e}{Style.RESET_ALL}")
        traceback.print_exc()
        sys.exit(1)
