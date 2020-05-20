from miscellanous.tools import Tools
from PyQt5.QtCore import pyqtSignal


class Data:
    def __init__(self, predictions=None, areas=None, left=None, right=None):
        self.predictions = Tools.read_csv(predictions)
        self.areas = Tools.read_csv(areas, '\t')
        self.left = left
        self.right = right
        self.changed = pyqtSignal()

    """
        GETTERS
    """
    def get_predictions(self):
        return self.predictions
    
    def get_areas(self):
        return self.areas
    
    def get_left(self):
        return self.left

    def get_right(self):
        return self.right
    """
        SETTERS
    """
    def set_right(self, right):
        self.right = right
        
    def set_left(self, left):
        self.left = left
        
    def set_predictions(self, predictions):
        self.predictions = Tools.read_csv(predictions)

    def set_areas(self, areas):
        self.areas = Tools.read_csv(areas, '\t')

