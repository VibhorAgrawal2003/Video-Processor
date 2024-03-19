from PyQt5.QtWidgets import QLabel

class AspectLabel(QLabel):
  def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.aspect_ratio = 3/4

  def resizeEvent(self, event):
      super().resizeEvent(event)
      self.setFixedHeight(int(self.width() * self.aspect_ratio))