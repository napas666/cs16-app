import threading, time

class Hop:
    def __init__(self, mem):
        self.mem  = mem
        self.on   = False
        self._air = False
        threading.Thread(target=self._run, daemon=True).start()

    def _run(self):
        while True:
            if self.on and self.mem.ok:
                try: self._tick()
                except: pass
            time.sleep(0.005)

    def _tick(self):
        try:
            import win32api, win32con
        except: return
        gnd = self.mem.onground()
        if self._air and gnd:
            win32api.keybd_event(win32con.VK_SPACE, 0, 0, 0)
            time.sleep(0.013)
            win32api.keybd_event(win32con.VK_SPACE, 0, win32con.KEYEVENTF_KEYUP, 0)
        self._air = not gnd
