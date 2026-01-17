# aura/setup_handlers.py

from aura.command_engine import SimpleKeywordHandler, CommandCategory, EnhancedCommandEngine
from aura.system_handlers import SystemHandler
from aura.smart_search import SmartSearch
from aura.screen_reader import read_screen
from aura.voice import set_voice

sys = SystemHandler()
smart = SmartSearch(sys_handler=sys)


def initialize_engine():
    engine = EnhancedCommandEngine()

    # ---------------------------------------------------------
    # SPECIFIC APP SHORTCUTS
    # ---------------------------------------------------------
    engine.register_handler(
        "open_chrome",
        SimpleKeywordHandler(
            name="open_chrome",
            keywords=["open chrome", "launch chrome", "start chrome"],
            response_func=lambda t: sys.open_app("chrome"),
            category=CommandCategory.SYSTEM
        )
    )

    engine.register_handler(
        "play_music",
        SimpleKeywordHandler(
            name="play_music",
            keywords=["play music", "start music", "open spotify", "music on"],
            response_func=lambda t: sys.open_app("spotify"),
            category=CommandCategory.ENTERTAINMENT
        )
    )

    # ---------------------------------------------------------
    # GENERIC OPEN / CLOSE APPS
    # ---------------------------------------------------------
    engine.register_handler(
        "open_app",
        SimpleKeywordHandler(
            name="open_app",
            keywords=["open", "launch", "start"],
            response_func=lambda t: sys.open_app(t.replace("open", "").replace("launch", "").replace("start", "").strip()),
            category=CommandCategory.SYSTEM
        )
    )

    engine.register_handler(
        "close_app",
        SimpleKeywordHandler(
            name="close_app",
            keywords=["close", "exit", "quit"],
            response_func=lambda t: sys.close_app(t.replace("close", "").replace("exit", "").replace("quit", "").strip()),
            category=CommandCategory.SYSTEM
        )
    )

    # ---------------------------------------------------------
    # YOUTUBE (explicit)
    # ---------------------------------------------------------
    engine.register_handler(
        "youtube_search",
        SimpleKeywordHandler(
            name="youtube_search",
            keywords=["youtube", "video", "watch", "play song"],
            response_func=lambda t: sys.open_youtube(
                t.replace("youtube", "")
                 .replace("video", "")
                 .replace("watch", "")
                 .replace("play", "")
                 .replace("song", "")
                 .strip()
            ),
            category=CommandCategory.INFORMATION
        )
    )

    # ---------------------------------------------------------
    # GOOGLE / AI SMART SEARCH
    # ---------------------------------------------------------
    engine.register_handler(
        "google_search",
        SimpleKeywordHandler(
            name="google_search",
            keywords=[
                "search", "google", "about", "who is", "what is", "define",
                "meaning of", "tell me about", "information on", "explain"
            ],
            response_func=lambda t: smart.handle(t),
            category=CommandCategory.INFORMATION
        )
    )

    # ---------------------------------------------------------
    # WIFI / BLUETOOTH / AIRPLANE / HOTSPOT
    # ---------------------------------------------------------
    engine.register_handler(
        "wifi_on",
        SimpleKeywordHandler(
            name="wifi_on",
            keywords=["wifi on", "turn on wifi", "enable wifi"],
            response_func=lambda t: sys.wifi_on(),
            category=CommandCategory.SYSTEM
        )
    )
    engine.register_handler(
        "wifi_off",
        SimpleKeywordHandler(
            name="wifi_off",
            keywords=["wifi off", "turn off wifi", "disable wifi"],
            response_func=lambda t: sys.wifi_off(),
            category=CommandCategory.SYSTEM
        )
    )

    engine.register_handler(
        "bluetooth_on",
        SimpleKeywordHandler(
            name="bluetooth_on",
            keywords=["bluetooth on", "enable bluetooth", "turn on bluetooth"],
            response_func=lambda t: sys.bluetooth_on(),
            category=CommandCategory.SYSTEM
        )
    )
    engine.register_handler(
        "bluetooth_off",
        SimpleKeywordHandler(
            name="bluetooth_off",
            keywords=["bluetooth off", "disable bluetooth", "turn off bluetooth"],
            response_func=lambda t: sys.bluetooth_off(),
            category=CommandCategory.SYSTEM
        )
    )

    engine.register_handler(
        "airplane_on",
        SimpleKeywordHandler(
            name="airplane_on",
            keywords=["airplane mode on", "enable airplane mode"],
            response_func=lambda t: sys.airplane_on(),
            category=CommandCategory.SYSTEM
        )
    )
    engine.register_handler(
        "airplane_off",
        SimpleKeywordHandler(
            name="airplane_off",
            keywords=["airplane mode off", "disable airplane mode"],
            response_func=lambda t: sys.airplane_off(),
            category=CommandCategory.SYSTEM
        )
    )

    engine.register_handler(
        "hotspot_on",
        SimpleKeywordHandler(
            name="hotspot_on",
            keywords=["hotspot on", "enable hotspot"],
            response_func=lambda t: sys.hotspot_on(),
            category=CommandCategory.SYSTEM
        )
    )
    engine.register_handler(
        "hotspot_off",
        SimpleKeywordHandler(
            name="hotspot_off",
            keywords=["hotspot off", "disable hotspot"],
            response_func=lambda t: sys.hotspot_off(),
            category=CommandCategory.SYSTEM
        )
    )

    # ---------------------------------------------------------
    # BRIGHTNESS / VOLUME
    # ---------------------------------------------------------
    engine.register_handler(
        "brightness_up",
        SimpleKeywordHandler(
            name="brightness_up",
            keywords=["increase brightness", "brightness up"],
            response_func=lambda t: sys.brightness_up(),
            category=CommandCategory.SYSTEM
        )
    )
    engine.register_handler(
        "brightness_down",
        SimpleKeywordHandler(
            name="brightness_down",
            keywords=["decrease brightness", "brightness down"],
            response_func=lambda t: sys.brightness_down(),
            category=CommandCategory.SYSTEM
        )
    )
    engine.register_handler(
        "brightness_set",
        SimpleKeywordHandler(
            name="brightness_set",
            keywords=["set brightness to"],
            response_func=lambda t: sys.brightness_set(
                int(t.replace("set brightness to", "").replace("%", "").strip())
            ),
            category=CommandCategory.SYSTEM
        )
    )

    engine.register_handler(
        "volume_set",
        SimpleKeywordHandler(
            name="volume_set",
            keywords=["set volume to"],
            response_func=lambda t: sys.volume_set(
                int(t.replace("set volume to", "").replace("%", "").strip())
            ),
            category=CommandCategory.SYSTEM
        )
    )

    # ---------------------------------------------------------
    # DARK / LIGHT MODE
    # ---------------------------------------------------------
    engine.register_handler(
        "dark_mode",
        SimpleKeywordHandler(
            name="dark_mode",
            keywords=["dark mode", "switch to dark mode"],
            response_func=lambda t: sys.dark_mode(),
            category=CommandCategory.SYSTEM
        )
    )
    engine.register_handler(
        "light_mode",
        SimpleKeywordHandler(
            name="light_mode",
            keywords=["light mode", "switch to light mode"],
            response_func=lambda t: sys.light_mode(),
            category=CommandCategory.SYSTEM
        )
    )

    # ---------------------------------------------------------
    # MICROPHONE / BATTERY
    # ---------------------------------------------------------
    engine.register_handler(
        "mic_mute",
        SimpleKeywordHandler(
            name="mic_mute",
            keywords=["mute microphone", "microphone mute"],
            response_func=lambda t: sys.mic_mute(),
            category=CommandCategory.SYSTEM
        )
    )
    engine.register_handler(
        "mic_unmute",
        SimpleKeywordHandler(
            name="mic_unmute",
            keywords=["unmute microphone", "microphone on"],
            response_func=lambda t: sys.mic_unmute(),
            category=CommandCategory.SYSTEM
        )
    )

    engine.register_handler(
        "battery_on",
        SimpleKeywordHandler(
            name="battery_on",
            keywords=["battery saver on", "enable battery saver"],
            response_func=lambda t: sys.battery_saver_on(),
            category=CommandCategory.SYSTEM
        )
    )
    engine.register_handler(
        "battery_off",
        SimpleKeywordHandler(
            name="battery_off",
            keywords=["battery saver off", "disable battery saver"],
            response_func=lambda t: sys.battery_saver_off(),
            category=CommandCategory.SYSTEM
        )
    )

    # ---------------------------------------------------------
    # SCREEN READER
    # ---------------------------------------------------------
    engine.register_handler(
        "read_screen",
        SimpleKeywordHandler(
            name="read_screen",
            keywords=["read screen", "read this", "read the screen"],
            response_func=lambda t: read_screen(),
            category=CommandCategory.PRODUCTIVITY
        )
    )

    # ---------------------------------------------------------
    # CHANGE VOICE
    # ---------------------------------------------------------
    engine.register_handler(
        "change_voice",
        SimpleKeywordHandler(
            name="change_voice",
            keywords=["voice number", "set voice"],
            response_func=lambda t: set_voice(
                int(''.join(ch for ch in t if ch.isdigit()) or 0)
            ),
            category=CommandCategory.OTHER
        )
    )

    # ---------------------------------------------------------
    # POWER CONTROL
    # ---------------------------------------------------------
    engine.register_handler(
        "shutdown",
        SimpleKeywordHandler(
            name="shutdown",
            keywords=["shutdown", "power off"],
            response_func=lambda t: sys.shutdown(),
            category=CommandCategory.SYSTEM
        )
    )
    engine.register_handler(
        "restart",
        SimpleKeywordHandler(
            name="restart",
            keywords=["restart", "reboot"],
            response_func=lambda t: sys.restart(),
            category=CommandCategory.SYSTEM
        )
    )
    engine.register_handler(
        "sleep",
        SimpleKeywordHandler(
            name="sleep",
            keywords=["sleep", "sleep mode"],
            response_func=lambda t: sys.sleep_mode(),
            category=CommandCategory.SYSTEM
        )
    )
    engine.register_handler(
        "lock",
        SimpleKeywordHandler(
            name="lock",
            keywords=["lock", "lock system"],
            response_func=lambda t: sys.lock_system(),
            category=CommandCategory.SYSTEM
        )
    )

    # ---------------------------------------------------------
    # CHROME TAB CONTROL
    # ---------------------------------------------------------
    engine.register_handler(
        "chrome_new_tab",
        SimpleKeywordHandler(
            name="chrome_new_tab",
            keywords=["new tab", "open new tab"],
            response_func=lambda t: sys.chrome_new_tab(),
            category=CommandCategory.PRODUCTIVITY
        )
    )
    engine.register_handler(
        "chrome_close_tab",
        SimpleKeywordHandler(
            name="chrome_close_tab",
            keywords=["close tab", "close this tab"],
            response_func=lambda t: sys.chrome_close_tab(),
            category=CommandCategory.PRODUCTIVITY
        )
    )

    # ---------------------------------------------------------
    # SMART FALLBACK SEARCH (catch-all AI)
    # ---------------------------------------------------------
    engine.register_handler(
        "smart_search",
        SimpleKeywordHandler(
            name="smart_search",
            keywords=[""],   # empty string → always matches (fallback)
            response_func=lambda t: smart.handle(t),
            category=CommandCategory.INFORMATION
        )
    )

    return engine
