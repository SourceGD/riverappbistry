from matplotlib import pyplot as plt

from src.utils import plot_to_image

class InvalidFileFormat(Exception):
    """
        Exception that indicate the file format isn't the one expected
    """

class BathymetryGraph():
    def __init__(self, bathymetry:str | tuple, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.separator = None
        self._check_bathymetry(bathymetry)
        self.bathymetry: str = bathymetry
        self.x_coordinates: list = []
        self.y_coordinates: list = []
        self._save_coordinates()

    def _check_bathymetry(self, bathymetry: str | tuple) -> None:
        
        if not isinstance(bathymetry, tuple):
            with open(bathymetry, 'r', encoding="utf-8") as file:
                lines: list = file.readlines()

                separators : list = [",", ";", " "]

                for separator in separators:
                    first_line = self._get_line_data(lines[0], separator)

                    if len(first_line) == 2 and (first_line[0] != "x" or first_line[0] != "X") and (first_line[1] != "y" or first_line[1] != "Y"):
                        self.separator = separator
                        return
                    
                if self.separator is None:
                    raise InvalidFileFormat("The expected format is explained in the documentation")
                
                for line in lines[1:]:
                    data: list = self._get_line_data(line, self.separator)
                    if len(data) != 2 or not data[0].replace('.','',1).isdigit() or not data[1].replace('.','',1).isdigit():
                        raise InvalidFileFormat("The expected format is explained in the documentation")
    
        else :
            if not isinstance(bathymetry[0], list) or not isinstance(bathymetry[1], list):
                raise TypeError("The expected tuple format is explained in the documentation")

            if len(bathymetry[0]) != len(bathymetry[1]):
                raise TypeError("The expected tuple format is explained in the documentation")
            
            for coord in bathymetry:
                if not all(isinstance(val, (int, float)) for val in coord):
                    raise TypeError("The expected tuple format is explained in the documentation")

    def _get_line_data(self, line: str, sep: str = None) -> list:
        return line.strip().split(sep)
    
    def _save_coordinates(self) -> None:
        if not isinstance(self.bathymetry, tuple):
            with open(self.bathymetry, 'r', encoding="utf-8") as file:
                lines = file.readlines()

                for line in lines[1:]:
                    data: list = self._get_line_data(line, self.separator)
                    self.x_coordinates.append(float(data[0]))
                    self.y_coordinates.append(float(data[1]))

        else:
            self.x_coordinates = self.bathymetry[0]
            self.y_coordinates = self.bathymetry[1]

    def generate_graph(self) -> plt:
        plt.plot(self.x_coordinates, self.y_coordinates, marker="o", linestyle="-")
        return plt

           
    def generate_image_widget(self):
        return plot_to_image(self.generate_graph())


