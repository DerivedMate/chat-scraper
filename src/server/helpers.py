from os import mkdir
def safe_mkdir(path):
  try: 
    mkdir(path)
    return True
  except:
    return False
