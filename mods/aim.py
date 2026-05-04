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
        ca = self.mem.angles()
        best, best_d = None, self.fov
        # Ищем ближайшего врага по углу (без фильтра команды — все игроки)
        for e in self.mem.enemies():
            o = e['pos']
            # Используем позицию камеры как src (грубо — центр карты не знаем,
            # но viewangles дают направление, а enemy pos — цель)
            target = (o[0], o[1], o[2] + (HEAD_Z if self.head else 0))
            # Для aim нам нужна относительная позиция
            # Берём viewangles и считаем угол к цели от origin
            ta = self._ang((0,0,0), target)
            # Сравниваем угол между текущим взглядом и направлением к цели
            d = math.hypot(self._norm(ca[0]-ta[0]), self._norm(ca[1]-ta[1]))
            if d < best_d:
                best_d, best = d, ta

        if best:
            dp = self._norm(best[0]-ca[0]) / self.smooth
            dy = self._norm(best[1]-ca[1]) / self.smooth
            self.mem.set_angles(ca[0]+dp, ca[1]+dy)
