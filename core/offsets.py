PROCESS   = "cs.exe"
HW_DLL    = "hw.dll"
CLIENT_DLL= "client.dll"

# hw.dll
VIEWANGLES = 0x6E3440   # float[3]: pitch, yaw, roll

# client.dll
LOCAL_IDX  = 0x9A8EC4   # int: local player index
ENT_LIST   = 0x1136F8C  # cl_entity_t array

# cl_entity_t layout
ENT_SIZE   = 0x4CC
CURSTATE   = 0x130      # entity_state_t curstate offset
CS_ORIGIN  = CURSTATE + 0x10   # curstate.origin  (vec3)
CS_HEALTH  = CURSTATE + 0xB0   # curstate.health  (int)
CS_TEAM    = CURSTATE + 0xFC   # curstate.iuser1  (int, team)
R_ORIGIN   = 0x44C             # render origin    (vec3)
ONGROUND   = CURSTATE + 0xD4   # curstate.onground(int)
HEAD_Z     = 64.0              # голова выше origin на ~64 ед.
