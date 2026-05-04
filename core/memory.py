import struct
import pymem, pymem.process
from core.offsets import *

class Mem:
    def __init__(self):
        self.pm = None
        self.hw = 0
        self.cl = 0
        self.ok = False

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
            self._rv3(self.hw + VIEWANGLES)
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

    def _rs(self, a, n=44):
        try: return self.pm.read_bytes(a, n).split(b'\x00')[0].decode('utf-8', 'ignore').strip()
        except: return ""

    # ── viewangles ────────────────────────────────────────
    def angles(self):
        return self._rv3(self.hw + VIEWANGLES)

    def set_angles(self, p, y):
        self._wv3(self.hw + VIEWANGLES, p, y, 0.0)

    # ── игрок ─────────────────────────────────────────────
    def local_team(self):
        return self._ri(self.cl + LOCAL_TEAM)

    def onground(self):
        return self._ri(self.hw + ONGROUND) == 1

    def _pi(self, i):
        return self.hw + ENT_LIST + i * ENT_SIZE

    def pi_name(self, i):
        return self._rs(self._pi(i) + PI_NAME)

    def pi_origin(self, i):
        return self._rv3(self._pi(i) + PI_ORIGIN)

    def local_origin(self):
        # Локальный игрок = индекс 1 в entity list
        return self.pi_origin(1)

    def local_name(self):
        return self.pi_name(1)

    # ── список врагов ─────────────────────────────────────
    def enemies(self):
        my_name = self.local_name()
        out = []
        for i in range(1, 33):
            name = self.pi_name(i)
            if not name:
                continue
            if name == my_name:          # пропускаем себя
                continue
            pos = self.pi_origin(i)
            if pos == (0.0, 0.0, 0.0):
                continue
            out.append({'i': i, 'pos': pos, 'name': name})
        return out
