# CS 1.6 build 8684 (Aug 3 2020) — cs.exe
# Source: unknowncheats.me/forum/505331

PROCESS    = "cs.exe"
HW_DLL     = "hw.dll"     # Engine
CLIENT_DLL = "client.dll" # Client

# ── hw.dll (Engine) ───────────────────────────────────────
VIEWANGLES = 0x1230274    # float[3] pitch, yaw, roll
ONGROUND   = 0x122E2D4    # int: 1=земля, 0=воздух
INMENU     = 0x6C3AB0     # int: 1=в меню

# ── Список игроков (hw.dll) ───────────────────────────────
# EntityList = hw.dll + 0x12043C8
# Структура PlayerInfo (размер 0x250):
#   0x000 number      int
#   0x004 cmd[256]    char
#   0x104 name[44]    char
#   0x130 model[80]   char
#   0x180 anim_frame  float
#   0x184 smth        float
#   0x188 origin      float[3]   ← позиция игрока
#   0x194 pad[188]    ...
ENT_LIST   = 0x12043C8    # база массива PlayerInfo в hw.dll
ENT_SIZE   = 0x250        # размер одной записи PlayerInfo
PI_NAME    = 0x104        # имя игрока (char[44])
PI_ORIGIN  = 0x188        # позиция (vec3)

# ── client.dll ────────────────────────────────────────────
LOCAL_TEAM = 0x100DE4     # int: команда локального игрока (1=T, 2=CT)
INMENU_CL  = 0x135484     # int: в меню

# ── Константы ─────────────────────────────────────────────
TEAM_T     = 1
TEAM_CT    = 2
HEAD_Z     = 64.0         # смещение головы над origin
