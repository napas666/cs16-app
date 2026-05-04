import os, math, threading, time

class ESP:
    def __init__(self, mem):
        self.mem = mem
        self.on  = False
        self.pen = False
        self.snp = False
        self.w = self.h = 0
        threading.Thread(target=self._run, daemon=True).start()

    @staticmethod
    def _w2s(rel, ang, sw, sh):
        p, y = math.radians(ang[0]), math.radians(ang[1])
        cp, sp, cy, sy = math.cos(p), math.sin(p), math.cos(y), math.sin(y)
        fwd   = (cp*cy, cp*sy, -sp)
        right = (sy,   -cy,    0)
        up    = (sp*cy, sp*sy,  cp)
        dx,dy,dz = rel
        f = dx*fwd[0]+dy*fwd[1]+dz*fwd[2]
        r = dx*right[0]+dy*right[1]+dz*right[2]
        u = dx*up[0]+dy*up[1]+dz*up[2]
        if f < 0.1: return None
        sc = sw / (2*math.tan(math.radians(45)))
        sx, sy_ = int(sw/2+r/f*sc), int(sh/2-u/f*sc)
        if -300<sx<sw+300 and -300<sy_<sh+300: return sx, sy_, f
        return None

    def _run(self):
        try:
            import pygame
            import win32gui, win32con, win32api
        except ImportError:
            return

        pygame.init(); pygame.font.init()
        hw = 0
        for _ in range(30):
            for t in ("Counter-Strike","Half-Life"):
                hw = win32gui.FindWindow(None, t)
                if hw: break
            if hw: break
            time.sleep(1)
        if not hw: return

        rc = win32gui.GetWindowRect(hw)
        self.w, self.h = rc[2]-rc[0], rc[3]-rc[1]
        os.environ['SDL_VIDEO_WINDOW_POS'] = f"{rc[0]},{rc[1]}"
        sc = pygame.display.set_mode((self.w, self.h), pygame.NOFRAME|pygame.SRCALPHA)
        pygame.display.set_caption("ov")
        ow = pygame.display.get_wm_info()['window']
        ex = win32gui.GetWindowLong(ow, win32con.GWL_EXSTYLE)
        win32gui.SetWindowLong(ow, win32con.GWL_EXSTYLE,
            ex|win32con.WS_EX_LAYERED|win32con.WS_EX_TRANSPARENT|win32con.WS_EX_TOPMOST)
        win32gui.SetLayeredWindowAttributes(ow, win32api.RGB(0,0,0), 0, win32con.LWA_COLORKEY)
        win32gui.SetWindowPos(ow, win32con.HWND_TOPMOST, rc[0], rc[1], self.w, self.h, 0)
        fnt = pygame.font.SysFont("Arial", 11, bold=True)
        clk = pygame.time.Clock()

        while True:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT: return
            sc.fill((0,0,0))
            if self.on and self.mem.ok: self._draw(sc, fnt)
            pygame.display.flip(); clk.tick(60)

    def _draw(self, sc, fnt):
        import pygame
        me  = self.mem.local_idx()
        if me < 1: return
        mp  = self.mem.pos(me)
        ang = self.mem.angles()
        for e in self.mem.enemies():
            o = e['pos']
            rel = (o[0]-mp[0], o[1]-mp[1], o[2]-mp[2]+36)
            pr = self._w2s(rel, ang, self.w, self.h)
            if not pr: continue
            sx, sy, dist = pr
            pen = math.dist(mp, o) < 500
            col = (255,80,80,200) if dist<250 else ((60,255,120,200) if (pen and self.pen) else (255,200,50,200))
            bh = max(18, int(1600/max(dist,1))); bw = max(10, bh//2)
            x1,y1 = sx-bw//2, sy-bh
            surf = pygame.Surface((bw,bh), pygame.SRCALPHA)
            surf.fill((*col[:3],30)); pygame.draw.rect(surf, col, (0,0,bw,bh), 2)
            sc.blit(surf,(x1,y1))
            hp = max(0,min(100,e['hp'])); fh = int(bh*hp/100)
            pygame.draw.rect(sc,(40,40,40),(x1-5,y1,3,bh))
            pygame.draw.rect(sc,(int(255*(1-hp/100)),int(255*hp/100),40),(x1-5,y1+bh-fh,3,fh))
            sc.blit(fnt.render(f"{hp}hp",True,(220,220,220)),(x1,sy+2))
            if pen and self.pen and dist>=250:
                sc.blit(fnt.render("PEN",True,(60,255,120)),(x1,y1-13))
            if self.snp:
                pygame.draw.line(sc,(180,60,255),(self.w//2,self.h),(sx,sy),1)
