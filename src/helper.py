# CENG 487 Assignment by
# Oğuzhan Özer
# StudentId: 260201039
# November 2021

import random


class Helper:
    def __init__(self) -> None:
        pass

    @staticmethod
    def rgb(n):  # generate n number of rgb colors
        """Generate n number of rgb colors

        Args:
            n (int): Amount of colors to be created

        Returns:
            list[tuple]: A tuple list which contains rgn tuples (colors)
        """
        rgb_arr = []
        for i in range(n):
            rgb = (0, 0, 0)
            for j in range(3):
                rgb[j] = random.uniform(0, 1.0)
            rgb_arr.append(rgb)
        return rgb_arr
