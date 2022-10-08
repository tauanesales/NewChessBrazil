class Casa:
  def __init__(self, forma, x, y, width, height):
    self.forma = forma
    self.x = x
    self.y = y
    self.width = width
    self.height = height

  def clicou_na_casa(self, x, y):
    return (self.x * self.width) <= x < (self.x + 1) * self.width \
        and (self.y * self.height) <= y < (self.y + 1) * self.height

  def retornar_coord(self, x, y):
    return self.x, self.y