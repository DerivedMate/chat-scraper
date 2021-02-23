import urllib.request as ureq
import pathlib as path

class Emoji():
  def __init__(self, name, url, dir):
    self.name = name
    self.url  = url
    self.path = self.__download(name, url, dir)

  def __download(self, name, url, dir):
    res    = ureq.urlopen(url)
    f_path = path.Path(dir) / f'{name}.png'
    dist   = open(f_path, 'wb') 

    dist.write(res.read())
    dist.flush()
    dist.close()

    return f_path.absolute()

class Premoji():
  def __init__(self, src):
    self.name = src["name"]
    self.url  = src["url"]
