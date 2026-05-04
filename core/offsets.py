# CS 1.6 build 8684 (Aug 3 2020) — cs.exe
# Verified offsets from unknowncheats.me

PROCESS    = "cs.exe"
HW_DLL     = "hw.dll"
CLIENT_DLL = "client.dll"

# ── hw.dll ────────────────────────────────────────────────
VIEWANGLES = 0x1230274    # float[3]: pitch, yaw, roll
ONGROUND   = 0x122E2D4    # int: 1=земля 0=воздух
RECOIL     = 0x122E324    # vec3: recoil punch angles

# Entity list (Players)
ENT_LIST   = 0x12043C8    # база массива PlayerInfo (индекс 0 = мир, 1..32 = игроки)
ENT_SIZE   = 0x250        # sizeof(PlayerInfo)

# Смещения внутри PlayerInfo:
PI_NUMBER  = 0x000        # int: номер
PI_NAME    = 0x104        # char[44]: имя
PI_MODEL   = 0x130        # char[80]: модель
PI_ORIGIN  = 0x188        # float[3]: позиция XYZ

# ── client.dll ────────────────────────────────────────────
LOCAL_TEAM   = 0x100DF4   # int: команда локального игрока
FORCE_JUMP   = 0x131434   # bhop

# ── Игровые константы ─────────────────────────────────────
TEAM_T  = 1
TEAM_CT = 2
HEAD_Z  = 64.0            # голова выше origin на ~64 ед.
