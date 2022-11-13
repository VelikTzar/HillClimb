import tkinter as tk
from settings.settings import Settings
from tkinter import ttk


def get_slider_value(slider, var):
    var.set(f'{slider.get(): .2f}')


class OptionsWindow:
    def __init__(self, app, master):
        self.frame = tk.Frame(master=master)
        self.app = app
        self.frame.pack()
        self.curr_settings = self.app.curr_settings

    def run(self):
        gravity_label = tk.Label(master=self.frame, text='Gravity')
        gravity_var = tk.DoubleVar()
        gravity_slider = ttk.Scale(master=self.frame, from_=0, to=2000, variable=gravity_var,
                                   command=lambda x: get_slider_value(gravity_slider, gravity_text_var))
        gravity_var.set(self.curr_settings.gravity)
        gravity_text_var = tk.StringVar()
        gravity_text_var.set(self.curr_settings.gravity)
        gravity_value_label = tk.Label(master=self.frame, textvariable=gravity_text_var)

        terrain_smoothness_label = tk.Label(master=self.frame, text='Terrain smoothness')
        terrain_smoothness_var = tk.DoubleVar()
        terrain_smoothness_slider = ttk.Scale(master=self.frame, from_=5, to=10, variable=terrain_smoothness_var,
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
        map_length_slider = ttk.Scale(master=self.frame, from_=200, to=10000, variable=map_length_var,
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
        car_max_force_slider = ttk.Scale(master=self.frame, from_=0, to=10000000, variable=car_max_force_var,
                                         command=lambda x:
                                         get_slider_value(car_max_force_slider, car_max_force_text_var))
        car_max_force_var.set(self.curr_settings.car_max_force)
        car_max_force_text_var = tk.StringVar()
        car_max_force_text_var.set(self.curr_settings.car_max_force)
        car_max_force_value_label = tk.Label(master=self.frame, textvariable=car_max_force_text_var)

        load_sprites_label = tk.Label(master=self.frame, text='Load sprites')
        load_sprites_var = tk.BooleanVar(self.frame)
        load_sprites_var.set(self.curr_settings.load_sprites)
        load_sprites_check_button = tk.Checkbutton(master=self.frame, variable=load_sprites_var)

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
        load_sprites_check_button.grid(row=7, column=1)
