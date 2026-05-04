import math, threading, time
from core.offsets import HEAD_Z

class Aim:
    def __init__(self, mem):
        self.mem    = mem
        self.on     = False
        self.fov    = 30.0
        self.smooth = 3.0
        self.head   = True
        threading.Thread(target=self._run, daemon=True).start()

    @staticmethod
    def _ang(src, dst):
        dx, dy, dz = dst[0]-src[0], dst[1]-src[1], dst[2]-src[2]
        return (-math.degrees(math.atan2(dz, math.hypot(dx, dy))),
                 math.degrees(math.atan2(dy, dx)))

    @staticmethod
    def _norm(a):
        while a >  180: a -= 360
        while a < -180: a += 360
        return a

    def _run(self):
        while True:
            if self.on and self.mem.ok:
                try: self._tick()
                except: pass
            time.sleep(0.008)

    def _tick(self):
        me = self.mem.local_idx()
        if me < 1: return
        my = self.mem.aim_pos(me)
        ca = self.mem.angles()
        best, best_d = None, self.fov
        for e in self.mem.enemies():
            o = e['aim']
            t = (o[0], o[1], o[2] + (HEAD_Z if self.head else 0))
            ta = self._ang(my, t)
            d  = math.hypot(self._norm(ca[0]-ta[0]), self._norm(ca[1]-ta[1]))
            if d < best_d:
                best_d, best = d, ta
        if best:
            dp = self._norm(best[0]-ca[0]) / self.smooth
            dy = self._norm(best[1]-ca[1]) / self.smooth
            self.mem.set_angles(ca[0]+dp, ca[1]+dy)
