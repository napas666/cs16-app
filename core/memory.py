import struct
import pymem, pymem.process
from core.offsets import *

class Mem:
    def __init__(self):
        self.pm   = None
        self.hw   = 0
        self.cl   = 0
        self.ok   = False
        self.hw_va = VIEWANGLES   # может быть переопределён SCAN-ом

    def attach(self):
        try:
            self.pm = pymem.Pymem(PROCESS)
            self.hw = pymem.process.module_from_name(self.pm.process_handle, HW_DLL).lpBaseOfDll
            self.cl = pymem.process.module_from_name(self.pm.process_handle, CLIENT_DLL).lpBaseOfDll
            self.ok = True
            return True, "OK"
        except Exception as e:
            self.ok = False
            return False, str(e)

    def alive(self):
        try:
            self._ri(self.hw + self.hw_va)
            return True
        except:
            self.ok = False
            return False

    def _ri(self, a):
        try: return self.pm.read_int(a)
        except: return 0

    def _rv3(self, a):
        try: return struct.unpack('fff', self.pm.read_bytes(a, 12))
        except: return (0.0, 0.0, 0.0)

    def _wv3(self, a, x, y, z):
        try: self.pm.write_bytes(a, struct.pack('fff', x, y, z), 12)
        except: pass

    def _rs(self, a, n):
        try: return self.pm.read_bytes(a, n).split(b'\x00')[0].decode('utf-8','ignore')
        except: return ""

    # ── viewangles ────────────────────────────────────────
    def angles(self):
        return self._rv3(self.hw + self.hw_va)

    def set_angles(self, p, y):
        self._wv3(self.hw + self.hw_va, p, y, 0.0)

    # ── локальный игрок ───────────────────────────────────
    def local_team(self):
        return self._ri(self.cl + LOCAL_TEAM)

    def onground(self):
        return self._ri(self.hw + ONGROUND) == 1

    # ── список игроков ────────────────────────────────────
    def _pi_base(self, i):
        # PlayerInfo[i] в hw.dll
        return self.hw + ENT_LIST + i * ENT_SIZE

    def player_origin(self, i):
        return self._rv3(self._pi_base(i) + PI_ORIGIN)

    def player_name(self, i):
        return self._rs(self._pi_base(i) + PI_NAME, 44)

    def enemies(self):
        my_team = self.local_team()
        out = []
        for i in range(32):
            name = self.player_name(i)
            if not name or name.strip() == "":
                continue
            pos = self.player_origin(i)
            # Фильтр: позиция должна быть реалистичной (не 0,0,0)
            if pos == (0.0, 0.0, 0.0):
                continue
            out.append({'i': i, 'pos': pos, 'name': name})
        return out
