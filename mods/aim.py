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
        ca = self.mem.angles()
        enemies = self.mem.enemies()
        if not enemies:
            return

        best, best_d = None, self.fov

        # Позиция локального игрока — берём из первого found enemy как origin базу
        # Для внешнего чита с этой структурой нет прямого доступа к своей позиции,
        # поэтому aim считается по углу к абсолютным координатам цели
        for e in enemies:
            o = e['pos']
            target = (o[0], o[1], o[2] + (HEAD_Z if self.head else 0))

            # Угол к цели (абсолютный yaw через atan2)
            ta = self._calc((0, 0, 0), target)

            # Дельта между текущим взглядом и направлением к цели
            dp = abs(self._norm(ca[0] - ta[0]))
            dy = abs(self._norm(ca[1] - ta[1]))
            d  = math.hypot(dp, dy)

            if d < best_d:
                best_d, best = d, ta

        if best:
            dp = self._norm(best[0] - ca[0]) / self.smooth
            dy = self._norm(best[1] - ca[1]) / self.smooth
            self.mem.set_angles(ca[0] + dp, ca[1] + dy)
