import matplotlib.pyplot as plt
from matplotlib.pyplot import Figure, Axes
import matplotlib.animation as animation
import sys
import numpy as np
from abc import ABC, abstractmethod

class PlotInterface(ABC):
  @abstractmethod
  def __init__(self):
    pass

  @abstractmethod
  def render(self):
    pass

  @abstractmethod
  def update(self, data):
    pass

  @abstractmethod
  def save(self, path: str):
    pass

class HBarPlot(PlotInterface):
  __fig__         : Figure
  __ax__          : Axes
  __data__        = {}
  __render_time__ = 0.01

  def __init__(self, title):
    self.__fig__, self.__ax__ = plt.subplots(figsize=(10, 12))
    self.__ax__.set_title(title)
    plt.ion()
    plt.show()
    plt.pause(self.__render_time__)

    self.render()

  def __sort__(self):
    self.__data__ = dict(sorted(self.__data__.items(), key=lambda t: t[1]))

  def __plot__(self, xs, ys):
    if len(xs) == 0:
      return
    y_pos = np.arange(len(ys))

    self.__ax__.clear()
    self.__ax__.barh(y_pos, ys, align='center', color='aqua')
    self.__ax__.set_yticks(y_pos)
    self.__ax__.set_yticklabels(xs)
    self.__ax__.set_xlim(right=ys[0] + 1)
    self.__ax__.invert_yaxis()

  def render(self):
    limit = 20

    self.__sort__()
    xs, ys = self.__data__.keys(), self.__data__.values()
    xs, ys = list(xs)[::-1][:limit], list(ys)[::-1][:limit]
    self.__plot__(xs, ys)
    
    plt.show()
    plt.pause(self.__render_time__)

  def update(self, data):
    self.__data__ = data

  def save(self, path):
    self.__fig__.savefig(path)

