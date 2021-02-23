from emoji import Premoji

class Response():
  # username       : str
  # badges         : list(str)
  # msg            : str
  # emojis         : list(Premoji)
  # is_highlighted : bool
  # links          : list(str)

  def __init__(self, src):
    self.username       = src["username"]
    self.badges         = src["badges"]
    self.msg            = src["msg"]
    self.emojis         = [Premoji(e) for e in src["emojis"]]
    self.is_highlighted = src["is_highlighted"]
    self.links          = src["links"]

  @staticmethod
  def from_json(dict):
    if all([k in dict for k in ["username", "msg"]]):
      return Response(dict)

    else:
      return dict
