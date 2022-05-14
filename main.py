from tkinter import *
from tkinter import ttk

tk = Tk()
tk.title("Tap Titan 2 raid titan part targeter")
tk.minsize(height=500, width=500)
tk.maxsize(height=500, width=500)
window = Canvas(width=500, height=5)
first_boss = ttk.Label(text="First boss")
first_boss_health_text = ttk.Label(text="Health")
first_boss_armor_text = ttk.Label(text="Armor")

first_boss.grid(column=0,row=0, columnspan=2)
first_boss_health_text.grid(column=0,row=1)
first_boss_armor_text.grid(column=1,row=1)



first_boss_head_health = ttk.Button()

tk.mainloop()
