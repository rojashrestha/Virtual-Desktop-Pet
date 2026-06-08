import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import random, math, os, sys

# ── Config ────────────────────────────────────────────────────────────────────
WIN_W   = 150
WIN_H   = 180   # sprite + bubble room
IMG_W   = 120
IMG_H   = 120
CAT_IMG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "momo_cat.png")

# ── Fallback: draw a simple cute cat if no image found ────────────────────────
def make_fallback_cat(size=120):
    """Draw a simple cute ginger cat using PIL — clean and readable."""
    frames = {}
    for state in ['idle', 'walk', 'sleep', 'happy']:
        imgs = []
        for f in range(2):
            img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
            d   = ImageDraw.Draw(img)
            cx, cy = size // 2, size // 2 + 8

            if state == 'sleep':
                # curled sleeping cat
                # body oval
                d.ellipse([cx-38, cy-10, cx+38, cy+38], fill="#E8841A", outline="#3B1500", width=2)
                d.ellipse([cx-22, cy, cx+22, cy+30], fill="#FAE0A0")
                # head
                hx, hy = cx-16, cy-18
                d.ellipse([hx-20, hy-20, hx+20, hy+12], fill="#E8841A", outline="#3B1500", width=2)
                # closed eyes
                d.arc([hx-14, hy-8, hx-4, hy+2],  start=0, end=180, fill="#3B1500", width=2)
                d.arc([hx+4,  hy-8, hx+14, hy+2], start=0, end=180, fill="#3B1500", width=2)
                # nose
                d.ellipse([hx-2, hy+3, hx+2, hy+7], fill="#FF8C94")
                # tail arc
                d.arc([cx-42, cy-8, cx+42, cy+42], start=30, end=150, fill="#C05000", width=5)
                # zzz
                if f == 1:
                    d.text((cx+22, cy-28), "z",  fill="#7B9FD4")
                    d.text((cx+30, cy-40), "Z",  fill="#7B9FD4")
            else:
                bob = 2 if f == 1 else 0
                cy2 = cy + bob

                # ── tail ──
                tail_x = cx + 32
                tail_sway = 4 if f == 0 else -2
                d.arc([cx+14, cy2+20, tail_x+tail_sway+20, cy2+50],
                      start=200, end=360, fill="#C05000", width=6)

                # ── body ──
                d.ellipse([cx-30, cy2+8, cx+30, cy2+68],
                          fill="#E8841A", outline="#3B1500", width=2)
                # belly
                d.ellipse([cx-16, cy2+20, cx+16, cy2+60], fill="#FAE0A0")

                # ── stripes ──
                d.arc([cx-30, cy2+10, cx-10, cy2+30], start=270, end=90,  fill="#C05000", width=2)
                d.arc([cx+10, cy2+10, cx+30, cy2+30], start=90,  end=270, fill="#C05000", width=2)

                # ── paws ──
                if state == 'walk':
                    leg = 6 if f == 0 else -6
                    d.ellipse([cx-22, cy2+60+leg, cx-8,  cy2+72+leg], fill="#E8841A", outline="#3B1500", width=1)
                    d.ellipse([cx+8,  cy2+60-leg, cx+22, cy2+72-leg], fill="#E8841A", outline="#3B1500", width=1)
                else:
                    d.ellipse([cx-22, cy2+62, cx-8,  cy2+74], fill="#E8841A", outline="#3B1500", width=1)
                    d.ellipse([cx+8,  cy2+62, cx+22, cy2+74], fill="#E8841A", outline="#3B1500", width=1)
                # toe marks
                for px_ in [cx-18, cx+12]:
                    for dl in [-3, 1, 5]:
                        d.line([px_+dl, cy2+68, px_+dl, cy2+73], fill="#3B1500", width=1)

                # ── head ──
                d.ellipse([cx-28, cy2-32, cx+28, cy2+18],
                          fill="#E8841A", outline="#3B1500", width=2)

                # ── ears ──
                d.polygon([cx-24, cy2-28, cx-34, cy2-52, cx-10, cy2-34],
                           fill="#E8841A", outline="#3B1500")
                d.polygon([cx-23, cy2-30, cx-31, cy2-48, cx-12, cy2-34],
                           fill="#FFB3BA")
                d.polygon([cx+24, cy2-28, cx+34, cy2-52, cx+10, cy2-34],
                           fill="#E8841A", outline="#3B1500")
                d.polygon([cx+23, cy2-30, cx+31, cy2-48, cx+12, cy2-34],
                           fill="#FFB3BA")

                # ── forehead stripes ──
                for fy in [cy2-20, cy2-14, cy2-8]:
                    d.line([cx-5, fy, cx+5, fy], fill="#C05000", width=2)

                # ── eyes ──
                ey = cy2 - 4
                if state == 'happy':
                    d.arc([cx-18, ey-8, cx-6,  ey+4], start=0, end=180, fill="#3B1500", width=3)
                    d.arc([cx+6,  ey-8, cx+18, ey+4], start=0, end=180, fill="#3B1500", width=3)
                elif f == 1 and state == 'idle':
                    # blink frame
                    d.line([cx-16, ey, cx-7, ey], fill="#3B1500", width=3)
                    d.line([cx+7,  ey, cx+16, ey], fill="#3B1500", width=3)
                else:
                    for ex in [cx-12, cx+12]:
                        d.ellipse([ex-8, ey-8, ex+8, ey+8], fill="#E8E8E8", outline="#3B1500", width=1)
                        d.ellipse([ex-6, ey-6, ex+6, ey+6], fill="#FFD700")
                        d.ellipse([ex-3, ey-6, ex+3, ey+6], fill="#1A1A1A")
                        d.ellipse([ex+2, ey-6, ex+5, ey-3], fill="#FFFFFF")

                # ── nose ──
                d.polygon([cx, cy2+7, cx-4, cy2+12, cx+4, cy2+12], fill="#FF8C94", outline="#3B1500")
                # mouth
                d.arc([cx-7, cy2+11, cx,   cy2+17], start=180, end=360, fill="#3B1500", width=1)
                d.arc([cx,   cy2+11, cx+7, cy2+17], start=180, end=360, fill="#3B1500", width=1)

                # ── whiskers ──
                for wy in [cy2+5, cy2+9, cy2+13]:
                    d.line([cx-6, wy, cx-28, wy-1], fill="#3B1500", width=1)
                    d.line([cx+6, wy, cx+28, wy-1], fill="#3B1500", width=1)

                # ── heart (happy) ──
                if state == 'happy' and f == 1:
                    hpts = []
                    for i in range(20):
                        a = math.pi * 2 * i / 20
                        hx2 = 7 * 16 * (math.sin(a)**3) / 16
                        hy2 = -7 * (13*math.cos(a) - 5*math.cos(2*a) - 2*math.cos(3*a) - math.cos(4*a)) / 16
                        hpts.append((cx+28+hx2, cy2-44+hy2))
                    if len(hpts) >= 3:
                        d.polygon(hpts, fill="#FF7BAC")

            imgs.append(img)
        frames[state] = imgs
    return frames


class MomoCat:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Momo")
        self.root.overrideredirect(True)
        self.root.wm_attributes("-transparentcolor", "#010101")
        self.root.wm_attributes("-topmost", True)
        self.root.configure(bg="#010101")

        self.canvas = tk.Canvas(self.root, width=WIN_W, height=WIN_H,
                                bg="#010101", highlightthickness=0)
        self.canvas.pack()

        # Load image or use drawn fallback
        self.use_image = os.path.exists(CAT_IMG)
        if self.use_image:
            self._load_sprite_sheet()
        else:
            self.frames = make_fallback_cat(IMG_W)

        self.state     = 'idle'
        self.tick      = 0
        self.happiness = 80
        self.hunger    = 60
        self.direction = 1
        self.vert_dir  = 1
        self._stop_wander  = False
        self._bubble_text  = None
        self._bubble_after = None
        self._photo_refs   = []   # keep refs so GC doesn't eat them

        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        self.x = sw // 2 - WIN_W // 2
        self.y = sh // 2 - WIN_H // 2
        self._place()

        self.canvas.bind("<ButtonPress-1>",   self._drag_start)
        self.canvas.bind("<B1-Motion>",       self._drag_move)
        self.canvas.bind("<ButtonRelease-1>", self._drag_end)
        self.canvas.bind("<Double-Button-1>", lambda e: self._pet())
        self.canvas.bind("<Button-3>",        self._show_menu)

        self.menu = tk.Menu(self.root, tearoff=0)
        self.menu.add_command(label="🐾  Pet",   command=self._pet)
        self.menu.add_command(label="🐟  Feed",  command=self.feed)
        self.menu.add_command(label="🧶  Play",  command=self.play)
        self.menu.add_command(label="💤  Sleep", command=self.sleep_cmd)
        self.menu.add_separator()
        self.menu.add_command(label="✖  Quit",  command=self.root.destroy)

        self._tick_anim()
        self._tick_wander()
        self._tick_decay()
        self.root.mainloop()

    def _load_sprite_sheet(self):
        """If user placed momo_cat.png next to the script, use it."""
        raw = Image.open(CAT_IMG).convert("RGBA").resize((IMG_W, IMG_H), Image.LANCZOS)
        self.frames = {s: [raw, raw] for s in ['idle','walk','sleep','happy']}

    def _place(self):
        self.root.geometry(f"{WIN_W}x{WIN_H}+{self.x}+{self.y}")

    def _drag_start(self, e):
        self._dx = e.x_root - self.x
        self._dy = e.y_root - self.y
        self._stop_wander = True

    def _drag_move(self, e):
        self.x = e.x_root - self._dx
        self.y = e.y_root - self._dy
        self._place()

    def _drag_end(self, e):
        self._stop_wander = False

    def _show_menu(self, e):
        self.menu.tk_popup(e.x_root, e.y_root)

    def _pet(self):
        if self.state == 'sleep':
            self._bubble("Nyaa! >:(", 2000); self.state = 'idle'; return
        self.happiness = min(100, self.happiness + 15)
        self.state = 'happy'
        self._bubble(random.choice(["Purrrr~", "Nyaa~~", "*headbonk*", "Meow!"]), 2200)
        self.root.after(2000, self._back_to_idle)

    def feed(self):
        if self.hunger >= 95:
            self._bubble("I'm full!", 1800); return
        self.hunger    = min(100, self.hunger + 30)
        self.happiness = min(100, self.happiness + 5)
        self.state = 'happy'
        self._bubble("Nom nom~", 2000)
        self.root.after(2000, self._back_to_idle)

    def play(self):
        if self.state == 'sleep':
            self._bubble("Zzz...", 1500); return
        self.happiness = min(100, self.happiness + 18)
        self.hunger    = max(0, self.hunger - 8)
        self.state = 'walk'
        self._bubble(random.choice(["Weee!", "*pounce*", "Zoooom!!"]), 2000)
        self.root.after(2500, self._back_to_idle)

    def sleep_cmd(self):
        self.state = 'sleep'
        self._bubble("Zzz... zZz", 3000)

    def _back_to_idle(self):
        if self.state != 'sleep': self.state = 'idle'

    def _bubble(self, text, ms=2000):
        if self._bubble_after: self.root.after_cancel(self._bubble_after)
        self._bubble_text  = text
        self._bubble_after = self.root.after(ms, lambda: setattr(self, '_bubble_text', None))

    def _tick_wander(self):
        if not self._stop_wander and self.state in ('idle', 'walk'):
            sw = self.root.winfo_screenwidth()
            sh = self.root.winfo_screenheight()
            if random.random() < 0.38:
                self.state = 'walk'
                self.x = max(0, min(sw-WIN_W, self.x + random.randint(10,24)*self.direction))
                if random.random() < 0.22: self.direction *= -1
                if random.random() < 0.40:
                    self.y = max(0, min(sh-WIN_H, self.y + random.randint(5,18)*self.vert_dir))
                    if random.random() < 0.28: self.vert_dir *= -1
                self._place()
            else:
                self.state = 'idle'
        self.root.after(600, self._tick_wander)

    def _tick_decay(self):
        if self.state != 'sleep':
            self.happiness = max(0, self.happiness - 0.8)
            self.hunger    = max(0, self.hunger    - 0.4)
        else:
            self.happiness = min(100, self.happiness + 1.5)
        if self.happiness < 20 and random.random() < 0.25:
            self._bubble("Feed me :(", 2000)
        self.root.after(3000, self._tick_decay)

    def _tick_anim(self):
        self.tick += 1
        frame_list = self.frames.get(self.state, self.frames['idle'])
        fi = (self.tick // 5) % len(frame_list)
        self._draw(frame_list[fi])
        spd = 600 if self.state == 'sleep' else 300
        self.root.after(spd, self._tick_anim)

    def _draw(self, img):
        c = self.canvas
        c.delete("all")

        # mirror when walking left
        draw_img = img
        if self.direction == -1 and self.state == 'walk':
            draw_img = img.transpose(Image.FLIP_LEFT_RIGHT)

        # convert RGBA → keep transparency via PhotoImage trick
        photo = ImageTk.PhotoImage(draw_img)
        self._photo_refs = [photo]   # keep reference

        off_x = (WIN_W - IMG_W) // 2
        off_y = 28
        c.create_image(off_x, off_y, anchor="nw", image=photo)

        # speech bubble
        if self._bubble_text:
            bx = WIN_W // 2
            tw = len(self._bubble_text) * 7 + 14
            c.create_rectangle(bx-tw//2, 4, bx+tw//2, 22,
                                fill="#2B1500", outline="#E8841A", width=1)
            c.create_text(bx, 13, text=self._bubble_text,
                          font=("Segoe UI", 8), fill="#FAE0A0", anchor="center")

        # stat dots
        hp = "#E24B4A" if self.happiness < 30 else "#E8841A"
        hu = "#E24B4A" if self.hunger    < 20 else "#3DBB6A"
        c.create_oval(WIN_W-9,  WIN_H-8, WIN_W-3,  WIN_H-2, fill=hu, outline="")
        c.create_oval(WIN_W-18, WIN_H-8, WIN_W-12, WIN_H-2, fill=hp, outline="")


if __name__ == "__main__":
    # Check Pillow
    try:
        from PIL import Image
    except ImportError:
        import subprocess, sys
        subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
    MomoCat()