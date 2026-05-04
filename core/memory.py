import struct
import pymem, pymem.process
from core.offsets import *

class Mem:
    def __init__(self):
        self.pm   = None
        self.hw   = 0
        self.cl   = 0
        self.ok   = False

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
            self._ri(self.hw + VIEWANGLES)
            return True
        except:
            self.ok = False
            return False

    def _ri(self, a):
        try: return self.pm.read_int(a)
        except: return 0

    def _rf(self, a):
        try: return self.pm.read_float(a)
        except: return 0.0

    def _rv3(self, a):
        try: return struct.unpack('fff', self.pm.read_bytes(a, 12))
        except: return (0.0, 0.0, 0.0)

    def _wv3(self, a, x, y, z):
        try: self.pm.write_bytes(a, struct.pack('fff', x, y, z), 12)
        except: pass

    def angles(self):
        return self._rv3(self.hw + VIEWANGLES)

    def set_angles(self, p, y):
        self._wv3(self.hw + VIEWANGLES, p, y, 0.0)

    def local_idx(self):
        return self._ri(self.cl + LOCAL_IDX)

    def _ent(self, i):
        return self.cl + ENT_LIST + i * ENT_SIZE

    def pos(self, i):
        return self._rv3(self._ent(i) + R_ORIGIN)

    def aim_pos(self, i):
        return self._rv3(self._ent(i) + CS_ORIGIN)

    def hp(self, i):
        return self._ri(self._ent(i) + CS_HEALTH)

    def team(self, i):
        return self._ri(self._ent(i) + CS_TEAM)

    def onground(self, i):
        return self._ri(self._ent(i) + ONGROUND) != 0

    def enemies(self):
        me = self.local_idx()
        my_team = self.team(me)
        out = []
        for i in range(1, 33):
            if i == me: continue
            h = self.hp(i)
            if not (1 <= h <= 100): continue
            t = self.team(i)
            if t == my_team or t not in (1, 2): continue
            out.append({'i': i, 'pos': self.pos(i), 'aim': self.aim_pos(i), 'hp': h})
        return out
