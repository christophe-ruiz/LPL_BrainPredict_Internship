from miscellanous.tools import Tools


class Data:
    def __init__(self, predictions=None, areas=None, left=None, right=None):
        self.predictions = Tools.read_csv(predictions)
        self.areas = Tools.read_csv(areas, '\t')
        self.left = left
        self.right = right

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
        if isinstance(predictions, str):
            self.predictions = Tools.read_csv(predictions)
        else:
            print('Predictions passed as parameters of set_predictions() is not of type', str.__name__)

    def set_areas(self, areas):
        if isinstance(areas, str):
            self.areas = Tools.read_csv(areas, '\t')
        else:
            print('Areas passed as parameters of set_areas() is not of type', str.__name__)
