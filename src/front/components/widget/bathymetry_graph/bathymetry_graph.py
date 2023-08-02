from os import path
from io import BytesIO
import numpy as np
from matplotlib import pyplot as plt

from kivy.uix.image import Image
from kivy.graphics.texture import Texture

class InvalidFileFormat(Exception):
    """
        Exception that indicate the file format isn't the one expected
    """

class BathymetryGraph():
    def __init__(self, bathymetry_path:str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.separator = None
        self._is_file_format_valid(bathymetry_path)
        self.bathymetry_path: str = bathymetry_path
        self.x_coordinates: list = []
        self.y_coordinates: list = []
        self._save_coordinates()

    def _is_file_format_valid(self, file_path:str) -> None:
        
        with open(file_path, 'r') as file:
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
    
    def _get_line_data(self, line: str, sep: str = None) -> list:
        return line.strip().split(sep)
    
    def _save_coordinates(self) -> None:
         with open(self.bathymetry_path, 'r') as file:
            lines = file.readlines()

            for line in lines[1:]:
                data: list = self._get_line_data(line, self.separator)
                self.x_coordinates.append(float(data[0]))
                self.y_coordinates.append(float(data[1]))

    def generate_graph(self) -> plt:
        plt.plot(self.x_coordinates, self.y_coordinates, marker="o", linestyle="-")
        return plt

           
    def generate_image_widget(self) -> Image:
        graph: plt = self.generate_graph()
        image_buffer: BytesIO = BytesIO()
        
        graph.savefig(image_buffer, format="png")
        graph.close()
        image_buffer.seek(0)
    
        # Load image data from the BytesIO object
        image_data = plt.imread(image_buffer)
        height, width, _ = image_data.shape

        # Invert the image vertically
        image_data = np.flipud(image_data)

        # Convert the image into values from 0 to 255 (8 bits) 
        image_data = (image_data * 255).astype(np.uint8)

        # Create texture from image data
        texture = Texture.create(size=(width, height), colorfmt='rgba')
        texture.blit_buffer(image_data.flatten(), colorfmt='rgba', bufferfmt='ubyte')
        
        image_buffer.close()

        return Image(texture=texture, size=(width, height), fit_mode="contain")


