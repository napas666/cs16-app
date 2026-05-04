import customtkinter as ctk
from tkinter import colorchooser

from core.memory import Mem
from mods.aim    import Aim
from mods.esp    import ESP
from mods.hop    import Hop
from mods.sight  import Sight, STYLES

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

AC  = "#c850ff"
BG  = "#0d0d0d"
C1  = "#161616"
C2  = "#1a1a1a"


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("CS 1.6 Trainer")
        self.geometry("360x720")
        self.resizable(False, False)
        self.configure(fg_color=BG)

        self.mem   = Mem()
        self.aim   = Aim(self.mem)
        self.esp   = ESP(self.mem)
        self.hop   = Hop(self.mem)
        self.sight = Sight()

        self._ui()
        self._tick()

    # ── шапка ─────────────────────────────────────────────
    def _ui(self):
        hdr = ctk.CTkFrame(self, fg_color=C1, corner_radius=0, height=52)
        hdr.pack(fill="x")
        ctk.CTkLabel(hdr, text="CS 1.6 TRAINER",
                     font=("Arial",15,"bold"), text_color=AC).pack(side="left", padx=14, pady=12)
        self._dot = ctk.CTkLabel(hdr, text="●", font=("Arial",18), text_color="#f44")
        self._dot.pack(side="right", padx=12)
        self._slbl = ctk.CTkLabel(hdr, text="NOT ATTACHED", font=("Arial",10), text_color="#555")
        self._slbl.pack(side="right")

        ctk.CTkButton(self, text="ATTACH TO CS 1.6", command=self._attach,
                      fg_color="#1e1040", hover_color="#2e1860",
                      border_color=AC, border_width=1,
                      font=("Arial",12,"bold"), height=36,
                      corner_radius=8).pack(fill="x", padx=14, pady=(12,2))

        # дебаг-строка
        self._dbg = ctk.CTkLabel(self, text="pitch=--  yaw=--  idx=--",
                                  font=("Courier",10), text_color="#333")
        self._dbg.pack(pady=(0,2))

        tabs = ctk.CTkTabview(self, fg_color=C1,
                              segmented_button_fg_color=C2,
                              segmented_button_selected_color="#2a1040",
                              segmented_button_selected_hover_color="#3a1860",
                              text_color="#bbb")
        tabs.pack(fill="both", expand=True, padx=14, pady=4)
        for n in ("AIM","ESP","PEN","BHOP","SIGHT"):
            tabs.add(n)
        self._aim_tab(tabs.tab("AIM"))
        self._esp_tab(tabs.tab("ESP"))
        self._pen_tab(tabs.tab("PEN"))
        self._hop_tab(tabs.tab("BHOP"))
        self._sight_tab(tabs.tab("SIGHT"))

    # ── AIM ───────────────────────────────────────────────
    def _aim_tab(self, t):
        self._sw_aim  = self._sw(t, "AIMBOT",  lambda: setattr(self.aim,'on', self._sw_aim.get()))
        self._sl(t,"FOV",   2,60,30,lambda v: setattr(self.aim,'fov',  float(v)),"deg")
        self._sl(t,"SMOOTH",1,20, 3,lambda v: setattr(self.aim,'smooth',float(v)),"x")
        row = ctk.CTkFrame(t, fg_color="transparent"); row.pack(fill="x",padx=6,pady=4)
        ctk.CTkLabel(row,text="TARGET",font=("Arial",11),text_color="#aaa",width=70).pack(side="left")
        self._tgt = ctk.CTkSegmentedButton(row, values=["HEAD","BODY"],
            command=lambda v: setattr(self.aim,'head', v=="HEAD"),
            selected_color="#2a1040", unselected_color=C2, font=("Arial",11,"bold"))
        self._tgt.set("HEAD"); self._tgt.pack(side="right")

    # ── ESP ───────────────────────────────────────────────
    def _esp_tab(self, t):
        self._sw_esp = self._sw(t,"ESP / WALLHACK", lambda: setattr(self.esp,'on', self._sw_esp.get()))
        self._sw_snp = self._sw(t,"SNAPLINES",      lambda: setattr(self.esp,'snp',self._sw_snp.get()))
        leg = ctk.CTkFrame(t, fg_color=C2, corner_radius=8); leg.pack(fill="x",padx=6,pady=8)
        for col,lbl in [("#f55","Direct view"),("#fc8","Behind wall"),("#4f7","PenBox")]:
            r=ctk.CTkFrame(leg,fg_color="transparent"); r.pack(fill="x",padx=10,pady=1)
            ctk.CTkLabel(r,text="●",font=("Arial",13),text_color=col).pack(side="left")
            ctk.CTkLabel(r,text=lbl,font=("Arial",11),text_color="#aaa").pack(side="left",padx=6)

    # ── PEN ───────────────────────────────────────────────
    def _pen_tab(self, t):
        self._sw_pen = self._sw(t,"PENBOX", lambda: setattr(self.esp,'pen',self._sw_pen.get()))
        f=ctk.CTkFrame(t,fg_color=C2,corner_radius=8); f.pack(fill="x",padx=6,pady=8)
        for ln in ["Green box = enemy behind","a penetrable surface.",
                   "","CS 1.6: metal/wood < 500 units.","Concrete = no penetration."]:
            ctk.CTkLabel(f,text=ln,font=("Arial",10),text_color="#555").pack(anchor="w",padx=12,pady=1)

    # ── BHOP ──────────────────────────────────────────────
    def _hop_tab(self, t):
        self._sw_hop = self._sw(t,"BUNNY HOP", lambda: setattr(self.hop,'on',self._sw_hop.get()))
        f=ctk.CTkFrame(t,fg_color=C2,corner_radius=8); f.pack(fill="x",padx=6,pady=8)
        for ln in ["Hold SPACE — auto bhop.","","Detects landing frame","and jumps at right moment."]:
            ctk.CTkLabel(f,text=ln,font=("Arial",10),text_color="#555").pack(anchor="w",padx=12,pady=1)

    # ── SIGHT ─────────────────────────────────────────────
    def _sight_tab(self, t):
        self._sw_sgt = self._sw(t,"CUSTOM CROSSHAIR", lambda: setattr(self.sight,'on',self._sw_sgt.get()))
        row=ctk.CTkFrame(t,fg_color="transparent"); row.pack(fill="x",padx=6,pady=(6,2))
        ctk.CTkLabel(row,text="STYLE",font=("Arial",11),text_color="#aaa",width=60).pack(side="left")
        om=ctk.CTkOptionMenu(row,values=STYLES,fg_color=C2,button_color="#2a1040",
                             button_hover_color="#3a1860",font=("Arial",11),
                             command=lambda v: setattr(self.sight,'style',STYLES.index(v)))
        om.pack(side="right")
        self._sl(t,"SIZE", 2,30,10,lambda v: setattr(self.sight,'size', int(v)),"px")
        self._sl(t,"WIDTH",1, 6, 2,lambda v: setattr(self.sight,'thick',int(v)),"px")
        self._sl(t,"GAP",  0,20, 4,lambda v: setattr(self.sight,'gap',  int(v)),"px")
        self._sw_dot = self._sw(t,"CENTER DOT", lambda: setattr(self.sight,'dot',    self._sw_dot.get()))
        self._sw_dot.select()
        self._sw_out = self._sw(t,"OUTLINE",    lambda: setattr(self.sight,'outline',self._sw_out.get()))
        self._sw_out.select()
        rc=ctk.CTkFrame(t,fg_color="transparent"); rc.pack(fill="x",padx=6,pady=(6,2))
        ctk.CTkLabel(rc,text="COLOR",font=("Arial",11),text_color="#aaa",width=60).pack(side="left")
        self._cprev=ctk.CTkLabel(rc,text="  ",fg_color="#00ff50",corner_radius=4,width=28,height=18)
        self._cprev.pack(side="right",padx=(0,4))
        ctk.CTkButton(rc,text="Pick",command=self._pick,fg_color=C2,hover_color="#2a1040",
                      font=("Arial",11),height=26,width=60,corner_radius=6).pack(side="right",padx=4)

    # ── helpers ───────────────────────────────────────────
    def _sw(self, parent, label, cmd):
        row=ctk.CTkFrame(parent,fg_color="transparent"); row.pack(fill="x",padx=6,pady=(8,2))
        ctk.CTkLabel(row,text=label,font=("Arial",12,"bold"),text_color="#ddd").pack(side="left")
        sw=ctk.CTkSwitch(row,text="",command=cmd,onvalue=True,offvalue=False,
                         button_color=AC,progress_color="#3d1a6e",width=44)
        sw.pack(side="right"); return sw

    def _sl(self, parent, label, mn, mx, default, cmd, unit=""):
        row=ctk.CTkFrame(parent,fg_color="transparent"); row.pack(fill="x",padx=6,pady=(2,0))
        ctk.CTkLabel(row,text=label,font=("Arial",10),text_color="#777",width=60).pack(side="left")
        vl=ctk.CTkLabel(row,text=f"{default}{unit}",font=("Arial",10,"bold"),text_color=AC,width=38)
        vl.pack(side="right")
        def cb(v): vl.configure(text=f"{int(v)}{unit}"); cmd(v)
        sl=ctk.CTkSlider(row,from_=mn,to=mx,number_of_steps=mx-mn,
                         command=cb,button_color=AC,progress_color=AC)
        sl.set(default); sl.pack(side="left",fill="x",expand=True,padx=8)

    def _attach(self):
        ok, msg = self.mem.attach()
        if ok:
            self._dot.configure(text_color="#4f8")
            self._slbl.configure(text="ATTACHED")
        else:
            self._dot.configure(text_color="#f44")
            self._slbl.configure(text=f"ERROR: {msg[:28]}")

    def _pick(self):
        col=colorchooser.askcolor(title="Color",color='#%02x%02x%02x'%self.sight.color)
        if col and col[0]:
            self.sight.color=tuple(int(c) for c in col[0])
            self._cprev.configure(fg_color='#%02x%02x%02x'%self.sight.color)

    def _tick(self):
        if self.mem.ok:
            try:
                p,y,_=self.mem.angles()
                idx=self.mem.local_idx()
                self._dbg.configure(text=f"pitch={p:.1f}  yaw={y:.1f}  idx={idx}",
                                    text_color="#555")
            except:
                pass
        self.after(150, self._tick)


if __name__ == "__main__":
    App().mainloop()
