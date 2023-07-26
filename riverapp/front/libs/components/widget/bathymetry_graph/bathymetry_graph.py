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
        self._file_extension: str = None
        self._is_file_format_valid(bathymetry_path)
        self.bathymetry_path:str = bathymetry_path

    def _is_file_format_valid(self, file_path:str) -> None:
        self._file_extension = path.splitext(file_path)[1]
        
        with open(file_path, 'r') as file:
            lines: list = file.readlines()

            first_line: list = self._get_line_data(lines[0])
            if len(first_line) != 2 or first_line[0] != "x" or first_line[1] != "y":
                raise InvalidFileFormat("The expected format is explained in the documentation")
            
            for line in lines[1:]:
                data: list = self._get_line_data(line)
                if len(data) != 2 or not data[0].replace('.','',1).isdigit() or not data[1].replace('.','',1).isdigit():
                    raise InvalidFileFormat("The expected format is explained in the documentation")
    
    def _get_line_data(self, line: str) -> list:
        return line.strip().split("," if self._file_extension == ".txt" else (";" if self._file_extension == ".csv" else None))

    def generate_graph(self) -> plt:
        x_coordinates: list = []
        y_coordinates: list = []

        with open(self.bathymetry_path, 'r') as file:
            lines = file.readlines()

            for line in lines[1:]:
                data: list = self._get_line_data(line)
                x_coordinates.append(float(data[0]))
                y_coordinates.append(float(data[1]))
        
        plt.plot(x_coordinates, y_coordinates, marker="o", linestyle="-")
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


