# -*- coding: utf-8 -*-
"""
@author: Sylvain
"""

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import numpy as np
import colorsys
from bokeh.palettes import all_palettes as bokeh_palettes

from Chatoyant_colors import color_dict


class ColorMap:
    def __init__(self, color_map=None, name=None):

        self.color_map = color_map
        self.name = name

    def __repr__(self):
        gradient = np.linspace(0, 1, 255)
        gradient = np.vstack((gradient, gradient))

        float_cmap = self._RGBCMap_to_floatCMap(self.color_map)
        new_cmap = ListedColormap(float_cmap)

        fig, ax = plt.subplots(nrows=1, figsize=(12, 1))
        ax.imshow(gradient, aspect="auto", cmap=new_cmap)
        # ax.set_axis_off()
        ax.set_xticks([]) 
        ax.set_yticks([]) 
        
        fig.tight_layout(pad=0.8)

        return f"Chatoyant ColorMap {self.name}, length {len(self.color_map)}."

    def __str__(self):
        return self.__repr__()

    def __add__(self, cmap2):
        cmap3 = ColorMap(
            color_map=self.color_map + cmap2.color_map,
            name=self.name + "+" + cmap2.name,
        )
        return cmap3

    def __getitem__(self, i):
        if isinstance(i, int):
            return ColorMap(color_map=self.color_map[i : i + 1], name=self.name +  f'[{i}]')
        elif isinstance(i, slice):
            return ColorMap(color_map=self.color_map[i], name=self.name +'-Sliced')

    def __len__(self):
        return len(self.color_map)

    @staticmethod
    def _RGB_to_float(r, g, b):
        return (r / 255.0, g / 255.0, b / 255.0)

    def _RGBCMap_to_floatCMap(self, values):
        return [self._RGB_to_float(r, g, b) for r, g, b in values]

    @staticmethod
    def _hex_to_RGB(value):

        value = value.lstrip("#")
        lv = len(value)
        col = [int(value[i : i + lv // 3], 16) for i in range(0, lv, lv // 3)]

        return col[0], col[1], col[2]

    @staticmethod
    def _RGB_to_hex(red, green, blue):

        return "#%02x%02x%02x" % (red, green, blue)

    @staticmethod
    def _normalize(r):
        return (r - r.min()) / (r.max() - r.min())

    def from_bokeh(self, name="YlGn", n=9):
        if name not in bokeh_palettes.keys():
            raise ValueError(
                f"Available Bokeh palettes are {list(bokeh_palettes.keys())}"
            )
        if n not in bokeh_palettes[name].keys():
            raise ValueError(
                f"Bokeh {name} palette is only available with lengths: {list(bokeh_palettes[name].keys())}"
            )
        hex_map = list(bokeh_palettes[name][n])
        # cmap = []
        # for x in hex_map:

        #     a, b, c = self._hex_to_RGB(x)
        #     cmap.append((a, b, c))
        
        cmap = [(self._hex_to_RGB(x)) for x in hex_map]
        name = name if self.name == None else self.name

        return ColorMap(color_map=cmap, name=name + "-" + str(n))

    def from_matplotlib(self, name="inferno", n=10):

        try:
            plt_map = plt.cm.get_cmap(name, n).colors * 255
        # Many plt Colormaps do not have the .colors attribute. Don't ask why.
        except (ValueError, AttributeError):
            plt_map = plt.cm.get_cmap(name, n)
            plt_map = plt_map(range(n)) * 255
        # Removing alpha channel, converting to int
        plt_map = np.round(plt_map[:, 0:3]).astype(int)
        
        name = name if self.name == None else self.name

        return ColorMap(color_map=list(map(tuple, plt_map)), name=name)

    def from_list(self, color_list=["red", "black"]):
        colors = []
        for color in color_list:

            if isinstance(color, str):
                if color.upper() in color_dict:
                    colors.append(color_dict[color.upper()])
            elif isinstance(color, tuple):
                if len(color) == 3:

                    if all(isinstance(v, int) for v in color):
                        colors.append(color)
            else:
                raise ValueError(
                    f"{color} neither in {color_dict.keys()} nor a valid RGB tuple"
                )
        
        name = "from_list" if self.name == None else self.name
                
        return ColorMap(color_map=colors, name=name)

    def to_matplotlib(self):
        return ListedColormap(self._RGBCMap_to_floatCMap(self.color_map))

    def to_tuple_list(self):
        return [tuple(x) for x in self.color_map]

    def invert(self):
        return ColorMap(color_map=self.color_map[::-1], name=self.name + "-Inverted")

    def to_HLS(self):

        HLS_map = []
        for r, g, b in self.color_map:
            r, g, b = r / 255, g / 255, b / 255

            h, l, s = colorsys.rgb_to_hls(r, g, b)
            h, l, s = int(h * 255), int(l * 255), int(s * 255)

            HLS_map.append((h, l, s))
        return ColorMap(color_map=HLS_map, name=self.name + "-HLS")

    def to_RGB(self):

        RGB_map = []
        for h, l, s in self.color_map:
            h, l, s = h / 255, l / 255, s / 255

            r, g, b = colorsys.hls_to_rgb(h, l, s)
            r, g, b = int(r * 255), int(g * 255), int(b * 255)

            RGB_map.append((r, g, b))
        return ColorMap(color_map=RGB_map, name=self.name + "-RGB")

    def loop(self, n=1):
        color_map = self.color_map
        if not isinstance(color_map, list):
            color_map = list(color_map)
        for i in range(n):
            color_map = color_map + self.color_map
        name = self.name + f"-Looped_{n}"

        return ColorMap(color_map=color_map, name=name)

    def extend(self, n=10):
        # Detour by Numpy to use linspace
        colors = np.asarray(self.color_map)
        cmap = LinearSegmentedColormap.from_list("", colors / 255, 256)
        cmap = cmap(np.linspace(0, 1, n)) * 255
        cmap = cmap[:, 0:3].astype(int)
        color_map = [tuple(x) for x in cmap]  # back to list of tuples for ease of use.

        name = self.name + f"-Extended_{n}"

        return ColorMap(color_map=color_map, name=name)

    def map_to_index(self, i):

        i = self._normalize(i)

        bins = np.linspace(0, i.max(), num=len(self.color_map) + 1)
        bins = bins[:-1]

        indexes = np.digitize(i, bins) - 1

        colors = [self.color_map[i] for i in indexes]

        return colors

    def set_name(self, name=None):
        if isinstance(name, str):
            return ColorMap(color_map=self.color_map, name=name)
        else:
            raise TypeError("Name must be a valid string.")

    def shift_hue(self, by=20):

        return (
            ColorMap(color_map=self.color_map, name=self.name)
            .to_HLS()
            .shift(by=(by, 0, 0))
            .to_RGB()
        )

    def shift(self, by=(0, 0, 0)):
        shifted_map = []
        for r, g, b in self.color_map:

            r += by[0]
            g += by[1]
            b += by[2]

            if r > 255:
                r -= 255
            if g > 255:
                g -= 255
            if b > 255:
                b -= 255
            shifted_map.append((r, g, b))
        return ColorMap(color_map=shifted_map, name=self.name + "-Shifted")

    def add_noise(self, by=(0, 0, 0)):

        noisy_map = []

        for r, g, b in self.color_map:

            r += np.random.uniform(0, by[0])
            g += np.random.uniform(0, by[1])
            b += np.random.uniform(0, by[2])

            if r > 255:
                r -= 255
            if g > 255:
                g -= 255
            if b > 255:
                b -= 255
            noisy_map.append((r, g, b))
        return ColorMap(color_map=noisy_map, name=self.name + "-Noisy")
