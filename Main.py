
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import pyautogui
import math
import random
import keyboard
from datetime import datetime
from pygame import mixer
import AppModule

# ---------- SAFETY ----------
pyautogui.FAILSAFE = False

# ---------- WINDOW ----------



newroot = tk.Tk()
root = tk.Toplevel(newroot)
root.overrideredirect(True)
root.attributes("-topmost", True)
root.attributes("-transparentcolor", "white")
root.config(bg="white")
mixer.init()
clickey_sound = mixer.Sound("D:\\Project_\\Audio\\VineBoom.mp3")

newroot.title("Project Draw Tkanwa")
newroot.configure(bg="#1e1e1e")
img = tk.PhotoImage(file='D:/Project_/images/curse.png')
window_width = 350
window_height = 400
newroot.iconphoto(True, img)

screen_width = newroot.winfo_screenwidth()
screen_height = newroot.winfo_screenheight()

x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))

newroot.geometry(f"{window_width}x{window_height}+{x}+{y}")
newroot.resizable(False, False)

bg_img = Image.open("D:\\Project_\\images\\Night.png").resize((350, 400))
bg_photo = ImageTk.PhotoImage(bg_img)

bg_label = tk.Label(newroot, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)


widths = tk.StringVar()
heights = tk.StringVar()


def DrawApps():

    app = AppModule.DrawApp(newroot, int(400), int(400))
    clickey_sound.play()
def InfoWindow():
    win = tk.Toplevel()
    win.title("Info")
    win.geometry(f"350x400+{x-350}+{y}")
    win.config(bg="#1e1e1e")
    win.resizable(False, False)

    label = tk.Label(win, text="Hello this is Project Draw Tkanwa \nThis is the drawing application\nI hope you guys enjoy drawing \nyour imagination with our lovely friends\n\n\n141920" ,justify="center", font=("Times New Roman", 11) , bg="#1e1e1e",fg="#D1DCFF")
    label.pack(fill="both", expand=True,padx=20, pady=20)

openbut = tk.Button(newroot, text="Create",bg="#2391FF",fg="White",font=("Segoe Script", 11, "bold"),width=25 , height=1,relief="flat",activebackground="#17a74a",cursor="hand2", command=DrawApps).pack(pady=40)
Info = tk.Button(newroot, text="Information",bg="#2391FF",fg="White",font=("Segoe Script", 11, "bold"),width=25 , height=1,relief="flat",activebackground="#17a74a",cursor="hand2", command=InfoWindow).pack(pady=40)

Sprite_Size = 80 
path = "D:\\Project_\\images\\"
img_idle = ImageTk.PhotoImage(Image.open(path+"brr.png").resize((Sprite_Size, Sprite_Size)))
img_walk = ImageTk.PhotoImage(Image.open(path+"monster.png").resize((Sprite_Size, Sprite_Size)))
img_follow = ImageTk.PhotoImage(Image.open(path+"smile.png").resize((Sprite_Size, Sprite_Size)))

label = tk.Label(root, image=img_walk, bg="white")
label.pack()

screen_w = root.winfo_screenwidth()
screen_h = root.winfo_screenheight()

sprite_x, sprite_y = 400.0, 400.0
dir_x, dir_y = 1, 0
state = "IDLE"
timer = 0

IDLE_TIME = (40, 120)
WALK_TIME = (60, 200)
FOLLOW_TIME = (80, 200)
DRAG_TIME = (60, 160)
GRAB_DISTANCE = 10
WALK_SPEED = 4
FOLLOW_SPEED = 6
DRAG_SPEED = 12
drag_window = None
WIN_OFFSET_X = 50
WIN_OFFSET_Y = 50

foot_l_img = Image.open("D:\\Project_\\images\\river.png").resize((40, 40))
foot_r_img = Image.open("D:\\Project_\\images\\curse.png").resize((40, 40))

foot_l = ImageTk.PhotoImage(foot_l_img)
foot_r = ImageTk.PhotoImage(foot_r_img)

foot_toggle = False

def mouse_down(event):
    global mouse_dragging, drag_offset_x, drag_offset_y

    if state == "DRAG":
        return

    mouse_dragging = True
    drag_offset_x = event.x
    drag_offset_y = event.y


def mouse_move(event):
    global mouse_dragging, sprite_x, sprite_y

    if not mouse_dragging or state == "DRAG":
        return

    sprite_x = event.x_root - drag_offset_x
    sprite_y = event.y_root - drag_offset_y


def mouse_up(event):
    global mouse_dragging
    mouse_dragging = False

label.bind("<Button-1>", mouse_down)
label.bind("<B1-Motion>", mouse_move)
label.bind("<ButtonRelease-1>", mouse_up)

def random_dir():
    angle = random.uniform(0, math.tau)
    return math.cos(angle), math.sin(angle)

def switch_state():
    global state, timer, dir_x, dir_y, drag_window

    state = random.choice(["IDLE", "WALK", "FOLLOW","Drop","FOLLOWFORDRAG"])#
    if drag_window:
        drag_window.destroy()
        drag_window = None

    if state == "IDLE":
        print("Idle")
        label.config(image=img_idle)
        timer = random.randint(*IDLE_TIME)

    elif state == "WALK":
        print("WALK")
        label.config(image=img_walk)
        timer = random.randint(*WALK_TIME)
        dir_x, dir_y = random_dir()

    elif state == "Drop":
        print("Drop")
        label.config(image=img_walk)
        timer = random.randint(*WALK_TIME)
        dir_x, dir_y = random_dir()

    elif state == "FOLLOW":
        print("FOLLOW")
        label.config(image=img_follow)
        timer = random.randint(*FOLLOW_TIME)
    elif state == "FOLLOWFORDRAG":
        print("FOLLOWFORDRAG")
        label.config(image=img_follow)
        timer = random.randint(*FOLLOW_TIME)
    elif state == "DRAG":
        print("DRAG")
        label.config(image=img_follow)
        timer = random.randint(*FOLLOW_TIME)
    


def drop_footprint():
    global foot_toggle

    img = foot_l if foot_toggle else foot_r
    foot_toggle = not foot_toggle

    fx = int(sprite_x + Sprite_Size // 2)
    fy = int(sprite_y + Sprite_Size - 12)

    fp = tk.Toplevel(root)
    fp.overrideredirect(True)
    fp.attributes("-topmost", True)
    fp.attributes("-transparentcolor", "black")
    fp.config(bg="black")

    fp.geometry(f"40x40+{fx}+{fy}")

    lbl = tk.Label(fp, image=img, bg="black", bd=0)
    lbl.image = img   # 🔴 CRITICAL: keep reference
    lbl.pack()
    fp.lower(root)

    # auto-remove
    fp.after(6000, fp.destroy)

def lerp(a, b, t):
    return a + (b - a) * t


switch_state()

def start_drags():
    global state, timer, dir_x, dir_y
    state = "DRAG"
    timer = random.randint(60, 160)
    dir_x, dir_y = random_dir()
def create_drag_window():
    global drag_window

    if drag_window is not None:
        return

    drag_window = tk.Toplevel(root)
    drag_window.overrideredirect(True)
    drag_window.attributes("-topmost", True)
    drag_window.geometry("220x120+400+300")
    drag_window.config(bg="#222")

    lbl = tk.Label(
        drag_window,
        text="HELP 😭\nLET ME GO",
        fg="white",
        bg="#222",
        font=("Arial", 14, "bold"),
        justify="center"
    )
    lbl.pack(expand=True, fill="both")

def apply_bounds():
    global sprite_x, sprite_y, dir_x, dir_y

    if sprite_x < 0:
        sprite_x = 0
        dir_x *= -1
    elif sprite_x + Sprite_Size > screen_w:
        sprite_x = screen_w - Sprite_Size
        dir_x *= -1

    if sprite_y < 0:
        sprite_y = 0
        dir_y *= -1
    elif sprite_y + Sprite_Size > screen_h:
        sprite_y = screen_h - Sprite_Size
        dir_y *= -1
def start_drag():
    global state, timer, dir_x, dir_y
    state = "Win_Drag"
    timer = random.randint(120, 300)
    dir_x, dir_y = random_dir()
    create_drag_window()



# ---------- UPDATE LOOP ----------
def update():
    global sprite_x, sprite_y, timer

    
    if state in ("Drop"):
        if random.random() < 0.3:  # annoyance level 😈
            drop_footprint()
        

    if keyboard.is_pressed("esc"):
        root.destroy()
        return

    if state == "IDLE":
        pass  # do nothing 😴

    elif state == "WALK":
        sprite_x += dir_x * WALK_SPEED
        sprite_y += dir_y * WALK_SPEED
    elif state == "Drop":
        sprite_x += dir_x * WALK_SPEED
        sprite_y += dir_y * WALK_SPEED

    elif state == "FOLLOW":
        mx, my = pyautogui.position()
        dx, dy = mx - sprite_x, my - sprite_y
        dist = math.hypot(dx, dy)

        if dist > GRAB_DISTANCE:
            dx /= dist
            dy /= dist
            sprite_x += dx * FOLLOW_SPEED
            sprite_y += dy * FOLLOW_SPEED
        else:
            start_drag()
    elif state == "FOLLOWFORDRAG":
        mx, my = pyautogui.position()
        dx, dy = mx - sprite_x, my - sprite_y
        dist = math.hypot(dx, dy)

        if dist > GRAB_DISTANCE:
            dx /= dist
            dy /= dist
            sprite_x += dx * FOLLOW_SPEED
            sprite_y += dy * FOLLOW_SPEED
        else:
            start_drags()
       


    elif state == "DRAG":
        drop_footprint()
        sprite_x += dir_x * DRAG_SPEED
        sprite_y += dir_y * DRAG_SPEED
        pyautogui.moveTo(sprite_x + 40, sprite_y + 40, duration=0)

        
    elif state == "Win_Drag":
        global drag_window

        if drag_window is None:
            return

        drop_footprint()

        # sprite movement
        sprite_x += dir_x * DRAG_SPEED
        sprite_y += dir_y * DRAG_SPEED

        # target position (sprite is dragging the window)
        target_x = sprite_x + WIN_OFFSET_X
        target_y = sprite_y + WIN_OFFSET_Y

        # current window position
        wx = drag_window.winfo_x()
        wy = drag_window.winfo_y()

        # smooth annoying drag 😈
        wx = lerp(wx, target_x, 0.15)
        wy = lerp(wy, target_y, 0.15)

        drag_window.geometry(f"+{int(wx)}+{int(wy)}")




    apply_bounds()
    root.geometry(f"+{int(sprite_x)}+{int(sprite_y)}")

    timer -= 1
    if timer <= 0:
        switch_state()

    root.after(16, update)

# def main():
#     
    

update()
root.mainloop()




    
    
   
    







# app = DrawApp(root)


# import tkinter as tk
# from tkinter import colorchooser
# import ttkbootstrap as ttk # The modern UI addon
# from PIL import Image, ImageDraw # The image backend

# class PaintApp(ttk.Window):
#     def init(self):
#         super().init(themename="superhero") # Modern Dark Theme
#         self.title("Python Paint")
#         self.geometry("800x600")

#         # 1. Setup Image Backend (PIL)
#         self.image = Image.new("RGB", (800, 600), "white")
#         self.draw = ImageDraw.Draw(self.image)

#         # 2. Setup UI (Ribbon)
#         self.controls = ttk.Frame(self)
#         self.controls.pack(side="top", fill="x")

#         ttk.Button(self.controls, text="Brush Color", command=self.choose_color).pack(side="left", padx=5, pady=5)
#         ttk.Button(self.controls, text="Save", command=self.save_image).pack(side="left", padx=5)

#         # 3. Setup Canvas (The Drawing Area)
#         self.canvas = tk.Canvas(self, bg="white", cursor="cross")
#         self.canvas.pack(fill="both", expand=True)

#         # 4. Bind Mouse Events
#         self.canvas.bind("<B1-Motion>", self.paint)
#         self.brush_color = "black"

#     def paint(self, event):
#         # Draw on screen (Tkinter)
#         x1, y1 = (event.x - 2), (event.y - 2)
#         x2, y2 = (event.x + 2), (event.y + 2)
#         self.canvas.create_oval(x1, y1, x2, y2, fill=self.brush_color, outline=self.brush_color)
#         self.draw.ellipse([x1, y1, x2, y2], fill=self.brush_color)

#     def choose_color(self):
#         color = colorchooser.askcolor()[1]
#         if color: self.brush_color = color

#     def save_image(self):
#         self.image.save("drawing.png")
#         print("Saved as drawing.png")

# if __name__ == "__main__":
#     app = PaintApp()
#     app.mainloop()

# import tkinter as tk
# from PIL import Image, ImageTk
# import pyautogui
# import random
# import math
# import keyboard

# pyautogui.FAILSAFE = False

# # ================= WINDOW =================
# root = tk.Tk()
# root.overrideredirect(True)
# root.attributes("-topmost", True)
# root.attributes("-transparentcolor", "white")
# root.config(bg="white")

# screen_w = root.winfo_screenwidth()
# screen_h = root.winfo_screenheight()

# # ================= sprite =================
# Sprite_Size = 80
# path = "D:/Project_/images/"

# img_idle = ImageTk.PhotoImage(Image.open(path+"brr.png").resize((Sprite_Size, Sprite_Size)))
# img_walk = ImageTk.PhotoImage(Image.open(path+"monster.png").resize((Sprite_Size, Sprite_Size)))
# img_follow = ImageTk.PhotoImage(Image.open(path+"smile.png").resize((Sprite_Size, Sprite_Size)))

# label = tk.Label(root, image=img_walk, bg="white")
# label.pack()

# # ================= STATE =================
# sprite_x, sprite_y = 400.0, 400.0
# dir_x, dir_y = 1, 0
# state = "WALK"
# timer = 120

# WALK_SPEED = 4
# FOLLOW_SPEED = 6
# DRAG_SPEED = 10
# GRAB_DISTANCE = 15

# drag_window = None
# WIN_OFFSET_X = 60
# WIN_OFFSET_Y = 40

# # ================= HELPERS =================
# def random_dir():
#     a = random.uniform(0, math.tau)
#     return math.cos(a), math.sin(a)

# def lerp(a, b, t):
#     return a + (b - a) * t

# def apply_bounds():
#     global sprite_x, sprite_y, dir_x, dir_y
#     if sprite_x < 0 or sprite_x + Sprite_Size > screen_w:
#         dir_x *= -1
#     if sprite_y < 0 or sprite_y + Sprite_Size > screen_h:
#         dir_y *= -1

# # ================= DRAG WINDOW =================
# def create_drag_window():
#     global drag_window
#     if drag_window:
#         return

#     drag_window = tk.Toplevel(root)
#     drag_window.overrideredirect(True)
#     drag_window.attributes("-topmost", True)
#     drag_window.geometry("220x120+500+300")
#     drag_window.config(bg="#222")

#     lbl = tk.Label(
#         drag_window,
#         text="HELP 😭\nLET ME GO",
#         fg="white",
#         bg="#222",
#         font=("Arial", 14, "bold"),
#         justify="center"
#     )
#     lbl.pack(expand=True, fill="both")

# def destroy_drag_window():
#     global drag_window
#     if drag_window:
#         drag_window.destroy()
#         drag_window = None

# # ================= STATE SWITCH =================
# def switch_state():
#     global state, timer, dir_x, dir_y

#     destroy_drag_window()
#     state = random.choice(["WALK", "FOLLOW"])

#     if state == "WALK":
#         label.config(image=img_walk)
#         timer = random.randint(80, 160)
#         dir_x, dir_y = random_dir()

#     elif state == "FOLLOW":
#         label.config(image=img_follow)
#         timer = random.randint(100, 200)

# def start_win_drag():
#     global state, timer, dir_x, dir_y
#     state = "WIN_DRAG"
#     timer = random.randint(150, 300)
#     dir_x, dir_y = random_dir()
#     create_drag_window()

# # ================= UPDATE LOOP =================
# def update():
#     global sprite_x, sprite_y, timer

#     if keyboard.is_pressed("esc"):
#         root.destroy()
#         return

#     if state == "WALK":
#         sprite_x += dir_x * WALK_SPEED
#         sprite_y += dir_y * WALK_SPEED

#     elif state == "FOLLOW":
#         mx, my = pyautogui.position()
#         dx, dy = mx - sprite_x, my - sprite_y
#         dist = math.hypot(dx, dy)

#         if dist > GRAB_DISTANCE:
#             sprite_x += dx / dist * FOLLOW_SPEED
#             sprite_y += dy / dist * FOLLOW_SPEED
#         else:
#             start_win_drag()

#     elif state == "WIN_DRAG":
#         sprite_x += dir_x * DRAG_SPEED
#         sprite_y += dir_y * DRAG_SPEED

#         if drag_window:
#             target_x = sprite_x + WIN_OFFSET_X
#             target_y = sprite_y + WIN_OFFSET_Y

#             wx = drag_window.winfo_x()
#             wy = drag_window.winfo_y()

#             wx = lerp(wx, target_x, 0.15)
#             wy = lerp(wy, target_y, 0.15)

#             drag_window.geometry(f"+{int(wx)}+{int(wy)}")

#     apply_bounds()
#     root.geometry(f"+{int(sprite_x)}+{int(sprite_y)}")

#     timer -= 1
#     if timer <= 0:
#         switch_state()

#     root.after(16, update)

# # ================= START =================
# switch_state()
# update()
# # root.mainloop()
# import tkinter as tk
# from PIL import Image, ImageTk
# import pyautogui
# import math, random, keyboard

# pyautogui.FAILSAFE = False

# # ================= MAIN WINDOW =================
# newroot = tk.Tk()
# newroot.withdraw()  # hide launcher (optional)

# root = tk.Toplevel(newroot)
# root.overrideredirect(True)
# root.attributes("-topmost", True)
# root.attributes("-transparentcolor", "white")
# root.config(bg="white")

# screen_w = root.winfo_screenwidth()
# screen_h = root.winfo_screenheight()

# # ================= sprite IMAGE =================
# Sprite_Size = 80
# path = "D:/Project_/images/"

# img_idle = ImageTk.PhotoImage(Image.open(path+"brr.png").resize((Sprite_Size, Sprite_Size)))
# img_walk = ImageTk.PhotoImage(Image.open(path+"monster.png").resize((Sprite_Size, Sprite_Size)))
# img_follow = ImageTk.PhotoImage(Image.open(path+"smile.png").resize((Sprite_Size, Sprite_Size)))

# label = tk.Label(root, image=img_walk, bg="white")
# label.pack()

# # ================= FOOTPRINT =================
# foot_l = ImageTk.PhotoImage(Image.open(path+"river.png").resize((40, 40)))
# foot_r = ImageTk.PhotoImage(Image.open(path+"curse.png").resize((40, 40)))
# foot_toggle = False

# # ================= STATE =================
# sprite_x, sprite_y = 400.0, 400.0
# dir_x, dir_y = 1, 0
# state = "WALK"
# timer = 120

# WALK_SPEED = 4
# FOLLOW_SPEED = 6
# DRAG_SPEED = 10
# GRAB_DISTANCE = 12

# drag_window = None
# WIN_OFFSET_X = 60
# WIN_OFFSET_Y = 40

# # ================= HELPERS =================
# def random_dir():
#     a = random.uniform(0, math.tau)
#     return math.cos(a), math.sin(a)

# def lerp(a, b, t):
#     return a + (b - a) * t

# def apply_bounds():
#     global sprite_x, sprite_y, dir_x, dir_y
#     if sprite_x < 0 or sprite_x + Sprite_Size > screen_w:
#         dir_x *= -1
#     if sprite_y < 0 or sprite_y + Sprite_Size > screen_h:
#         dir_y *= -1

# def drop_footprint():
#     global foot_toggle
#     img = foot_l if foot_toggle else foot_r
#     foot_toggle = not foot_toggle

#     fp = tk.Toplevel(root)
#     fp.overrideredirect(True)
#     fp.attributes("-topmost", True)
#     fp.attributes("-transparentcolor", "black")
#     fp.config(bg="black")

#     fp.geometry(f"40x40+{int(sprite_x)+40}+{int(sprite_y)+60}")
#     lbl = tk.Label(fp, image=img, bg="black")
#     lbl.image = img
#     lbl.pack()
#     fp.after(5000, fp.destroy)

# # ================= DRAG WINDOW =================
# def create_drag_window():
#     global drag_window
#     if drag_window:
#         return

#     drag_window = tk.Toplevel(root)
#     drag_window.overrideredirect(True)
#     drag_window.attributes("-topmost", True)
#     drag_window.geometry("220x120+500+300")
#     drag_window.config(bg="#222")

#     tk.Label(
#         drag_window,
#         text="HELP 😭\nLET ME GO",
#         fg="white",
#         bg="#222",
#         font=("Arial", 14, "bold"),
#         justify="center"
#     ).pack(expand=True, fill="both")

# def destroy_drag_window():
#     global drag_window
#     if drag_window:
#         drag_window.destroy()
#         drag_window = None

# # ================= STATE CONTROL =================
# def switch_state():
#     global state, timer, dir_x, dir_y
#     destroy_drag_window()

#     state = random.choice(["WALK", "IDLE", "FOLLOW"])
#     dir_x, dir_y = random_dir()

#     if state == "IDLE":
#         label.config(image=img_idle)
#         timer = random.randint(60, 140)

#     elif state == "WALK":
#         label.config(image=img_walk)
#         timer = random.randint(80, 200)

#     elif state == "FOLLOW":
#         label.config(image=img_follow)
#         timer = random.randint(100, 220)

# def start_win_drag():
#     global state, timer, dir_x, dir_y
#     state = "WIN_DRAG"
#     timer = random.randint(150, 300)
#     dir_x, dir_y = random_dir()
#     create_drag_window()

# # ================= UPDATE LOOP =================
# def update():
#     global sprite_x, sprite_y, timer

#     if keyboard.is_pressed("esc"):
#         root.destroy()
#         return

#     if state == "IDLE":
#         pass

#     elif state == "WALK":
#         sprite_x += dir_x * WALK_SPEED
#         sprite_y += dir_y * WALK_SPEED

#     elif state == "FOLLOW":
#         mx, my = pyautogui.position()
#         dx, dy = mx - sprite_x, my - sprite_y
#         dist = math.hypot(dx, dy)

#         if dist > GRAB_DISTANCE:
#             sprite_x += dx / dist * FOLLOW_SPEED
#             sprite_y += dy / dist * FOLLOW_SPEED
#         else:
#             start_win_drag()

#     elif state == "WIN_DRAG":
#         drop_footprint()
#         sprite_x += dir_x * DRAG_SPEED
#         sprite_y += dir_y * DRAG_SPEED

#         if drag_window:
#             wx = drag_window.winfo_x()
#             wy = drag_window.winfo_y()

#             tx = sprite_x + WIN_OFFSET_X
#             ty = sprite_y + WIN_OFFSET_Y

#             drag_window.geometry(
#                 f"+{int(lerp(wx, tx, 0.15))}+{int(lerp(wy, ty, 0.15))}"
#             )

#     apply_bounds()
#     root.geometry(f"+{int(sprite_x)}+{int(sprite_y)}")

#     timer -= 1
#     if timer <= 0:
#         switch_state()

#     root.after(16, update)

# # ================= START =================
# switch_state()
# update()
# root.mainloop()
