import tkinter as tk

from game.game import Game
from settings.settings import Settings
from tkinter import ttk
from tkinter import messagebox


def get_slider_value(slider, var):
    var.set(f'{slider.get(): .2f}')


def change_btn_value(btn, var, text_var):
    var.set(not var.get())
    text_var.set(f'{var.get()}')


class OptionsWindow:
    def __init__(self, app, menu, master):
        self.frame = tk.Frame(master=master)
        self.app = app
        self.menu = menu
        self.frame.pack()
        self.curr_settings = self.app.curr_settings

    def run(self):
        gravity_label = tk.Label(master=self.frame, text='Gravity')
        gravity_var = tk.DoubleVar()
        gravity_slider = ttk.Scale(master=self.frame, from_=1, to=2000, variable=gravity_var,
                                   command=lambda x: get_slider_value(gravity_slider, gravity_text_var))
        gravity_var.set(self.curr_settings.gravity)
        gravity_text_var = tk.StringVar()
        gravity_text_var.set(self.curr_settings.gravity)
        gravity_value_label = tk.Label(master=self.frame, textvariable=gravity_text_var)

        terrain_smoothness_label = tk.Label(master=self.frame, text='Terrain smoothness')
        terrain_smoothness_var = tk.DoubleVar()
        terrain_smoothness_slider = ttk.Scale(master=self.frame, from_=0, to=15, variable=terrain_smoothness_var,
                                              command=lambda x:
                                              get_slider_value(terrain_smoothness_slider, terrain_smoothness_text_var))
        terrain_smoothness_var.set(self.curr_settings.terrain_smoothness)
        terrain_smoothness_text_var = tk.StringVar()
        terrain_smoothness_text_var.set(self.curr_settings.terrain_smoothness)
        terrain_smoothness_value_label = tk.Label(master=self.frame, textvariable=terrain_smoothness_text_var)

        terrain_spacing_label = tk.Label(master=self.frame, text='Terrain spacing')
        terrain_spacing_var = tk.DoubleVar()
        terrain_spacing_slider = ttk.Scale(master=self.frame, from_=1, to=50, variable=terrain_spacing_var,
                                           command=lambda x:
                                           get_slider_value(terrain_spacing_slider, terrain_spacing_text_var))
        terrain_spacing_var.set(self.curr_settings.terrain_spacing)
        terrain_spacing_text_var = tk.StringVar()
        terrain_spacing_text_var.set(self.curr_settings.terrain_spacing)
        terrain_spacing_value_label = tk.Label(master=self.frame, textvariable=terrain_spacing_text_var)

        terrain_amplitude_label = tk.Label(master=self.frame, text='Terrain amplitude')
        terrain_amplitude_var = tk.DoubleVar()
        terrain_amplitude_slider = ttk.Scale(master=self.frame, from_=0, to=1, variable=terrain_amplitude_var,
                                             command=lambda x:
                                             get_slider_value(terrain_amplitude_slider, terrain_amplitude_text_var))
        terrain_amplitude_var.set(self.curr_settings.terrain_amplitude)
        terrain_amplitude_text_var = tk.StringVar()
        terrain_amplitude_text_var.set(self.curr_settings.terrain_amplitude)
        terrain_amplitude_value_label = tk.Label(master=self.frame, textvariable=terrain_amplitude_text_var)

        map_length_label = tk.Label(master=self.frame, text='Map length')
        map_length_var = tk.DoubleVar()
        map_length_slider = ttk.Scale(master=self.frame, from_=Game.DISPLAY_W, to=10000, variable=map_length_var,
                                      command=lambda x:
                                      get_slider_value(map_length_slider, map_length_text_var))
        map_length_var.set(self.curr_settings.map_length)
        map_length_text_var = tk.StringVar()
        map_length_text_var.set(self.curr_settings.map_length)
        map_length_value_label = tk.Label(master=self.frame, textvariable=map_length_text_var)

        car_rate_label = tk.Label(master=self.frame, text='Motor rate')
        car_rate_var = tk.DoubleVar()
        car_rate_slider = ttk.Scale(master=self.frame, from_=0, to=500, variable=car_rate_var,
                                    command=lambda x:
                                    get_slider_value(car_rate_slider, car_rate_text_var))
        car_rate_var.set(self.curr_settings.car_rate)
        car_rate_text_var = tk.StringVar()
        car_rate_text_var.set(self.curr_settings.car_rate)
        car_rate_value_label = tk.Label(master=self.frame, textvariable=car_rate_text_var)

        car_max_force_label = tk.Label(master=self.frame, text='Motor max force')
        car_max_force_var = tk.DoubleVar()
        car_max_force_slider = ttk.Scale(master=self.frame, from_=0.1, to=10000000, variable=car_max_force_var,
                                         command=lambda x:
                                         get_slider_value(car_max_force_slider, car_max_force_text_var))
        car_max_force_var.set(self.curr_settings.car_max_force)
        car_max_force_text_var = tk.StringVar()
        car_max_force_text_var.set(self.curr_settings.car_max_force)
        car_max_force_value_label = tk.Label(master=self.frame, textvariable=car_max_force_text_var)

        load_sprites_label = tk.Label(master=self.frame, text='Load sprites')
        load_sprites_var = tk.BooleanVar()
        load_sprites_var.set(self.curr_settings.load_sprites)
        load_sprites_text_var = tk.StringVar()
        load_sprites_text_var.set(f'{load_sprites_var.get()}')
        load_sprites_button = tk.Button(master=self.frame,
                                        textvariable=load_sprites_text_var, command=
                                        lambda: change_btn_value(load_sprites_button, load_sprites_var,
                                                                 load_sprites_text_var))

        apply_settings_btn = tk.Button(master=self.frame, text='Apply settings',
                                       command=lambda: self.apply_settings(
                                           float(gravity_slider.get()),
                                           int(terrain_smoothness_slider.get()),
                                           int(terrain_spacing_slider.get()),
                                           float(terrain_amplitude_slider.get()),
                                           int(map_length_slider.get()),
                                           float(car_rate_slider.get()),
                                           float(car_max_force_slider.get()),
                                           load_sprites_var.get()
                                       ))
        apply_default_btn = tk.Button(master=self.frame, text='Apply default',
                                      command=lambda: self.apply_default_settings())

        gravity_label.grid(row=0, column=0)
        gravity_slider.grid(row=0, column=1)
        gravity_value_label.grid(row=0, column=2)

        terrain_smoothness_label.grid(row=1, column=0)
        terrain_smoothness_slider.grid(row=1, column=1)
        terrain_smoothness_value_label.grid(row=1, column=2)

        terrain_spacing_label.grid(row=2, column=0)
        terrain_spacing_slider.grid(row=2, column=1)
        terrain_spacing_value_label.grid(row=2, column=2)

        map_length_label.grid(row=3, column=0)
        map_length_slider.grid(row=3, column=1)
        map_length_value_label.grid(row=3, column=2)

        terrain_amplitude_label.grid(row=4, column=0)
        terrain_amplitude_slider.grid(row=4, column=1)
        terrain_amplitude_value_label.grid(row=4, column=2)

        car_rate_label.grid(row=5, column=0)
        car_rate_slider.grid(row=5, column=1)
        car_rate_value_label.grid(row=5, column=2)

        car_max_force_label.grid(row=6, column=0)
        car_max_force_slider.grid(row=6, column=1)
        car_max_force_value_label.grid(row=6, column=2)

        load_sprites_label.grid(row=7, column=0)
        load_sprites_button.grid(row=7, column=1)

        apply_settings_btn.grid(row=8, columnspan=3)
        apply_default_btn.grid(row=9, columnspan=3)

    def apply_settings(self, *args):
        settings = Settings(*args)
        tk.messagebox.showinfo('Settings applied', 'You will return to the main menu')
        self.frame.master.destroy()
        self.app.curr_settings = settings
        print(self.app.curr_settings)
        print(self.app.curr_settings.car_rate)
        print(self.app.curr_settings.car_max_force)
        print(self.app.curr_settings.load_sprites)

    def apply_default_settings(self):
        settings = Settings()
        tk.messagebox.showinfo('Default settings applied', 'You will return to the main menu')
        self.frame.master.destroy()
        self.app.curr_settings = settings
