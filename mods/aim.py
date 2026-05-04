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
    def _norm(a):
        while a >  180: a -= 360
        while a < -180: a += 360
        return a

    @staticmethod
    def _calc(src, dst):
        dx = dst[0] - src[0]
        dy = dst[1] - src[1]
        dz = dst[2] - src[2]
        pitch = -math.degrees(math.atan2(dz, math.hypot(dx, dy)))
        yaw   =  math.degrees(math.atan2(dy, dx))
        return pitch, yaw

    def _run(self):
        while True:
            if self.on and self.mem.ok:
                try: self._tick()
                except: pass
            time.sleep(0.008)

    def _tick(self):
        ca      = self.mem.angles()          # текущий прицел (pitch, yaw, roll)
        my_pos  = self.mem.local_origin()    # позиция локального игрока
        enemies = self.mem.enemies()
        if not enemies:
            return

        best, best_d = None, self.fov

        for e in enemies:
            o = e['pos']
            # Цель: позиция врага + смещение головы
            target = (o[0], o[1], o[2] + (HEAD_Z if self.head else 0))
            # Угол от нашей позиции к цели
            ta = self._calc(my_pos, target)
            # Дистанция в угловом пространстве от текущего взгляда
            d = math.hypot(self._norm(ca[0] - ta[0]),
                           self._norm(ca[1] - ta[1]))
            if d < best_d:
                best_d, best = d, ta

        if best:
            dp = self._norm(best[0] - ca[0]) / self.smooth
            dy = self._norm(best[1] - ca[1]) / self.smooth
            self.mem.set_angles(ca[0] + dp, ca[1] + dy)
