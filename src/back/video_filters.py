"""
Module for applying filters to videos
"""

from os.path import exists, basename, splitext
import cv2
import numpy as np


class Filters:
    """
    Class for applying filters to videos

    This class provides functions for applying various image filters to video frames
    and saving the processed video to a specified output file.

    Methods
    -------

    - `_get_video_cap(self, video: str) -> cv2.VideoCapture`
        - Opens a video capture object for a specified video file.

    - `_get_video_output(self, output: str, cap: cv2.VideoCapture) -> cv2.VideoWriter`
        - Creates a video writer object for writing video frames to a specified output file.

    - `_release(self, cap: cv2.VideoCapture, out: cv2.VideoWriter) -> None`
        - Releases the video capture and writer objects.

    - `gamma_on_image(self, image: list, gamma: int | float) -> list`
        - Applies gamma correction to an image.

    - `gamma_on_video(self, video: str, gamma: int | float, output: str) -> None`
        - Applies gamma correction to a video and saves the result.

    - `black_white_filter_on_image(self, image) -> list`
        - Applies a black and white filter to an image.

    - `black_white_filter_on_video(self, video: str, output: str) -> None`
        - Applies a black and white filter to a video and saves the result.

    - `apply_multi_filter_on_video(self, filters: list, video: str, output: str, **kwargs) -> None`
        - Applies multiple filters to a video and saves the result.

    Notes
    -----

    - This class utilizes OpenCV (cv2) for video processing and image manipulation.
    - Helper functions (`_get_video_cap`, `_get_video_output`, `_release`) are used for
      common video capture, output configuration, and resource management tasks.
    - The class provides functions for applying individual filters (gamma correction,
      black and white) as well as a function to apply a sequence of filters from a
      provided list.

    """

    def _get_video_cap(self, video: str) -> cv2.VideoCapture:
        """
        Opens a video capture object for a specified video file

        This function attempts to open a video capture object using OpenCV (`cv2`)
        for the provided video file path.

        Parameters
        ----------

        - `video` (`str`): The path to the video file.

        Returns
        -------

        - `cv2.VideoCapture`: A cv2 VideoCapture object representing the opened video.

        Raises
        ------

        - `FileNotFoundError`: If the specified video file does not exist.
        - `RuntimeError`: If the video capture object could not be opened, even if the
          file exists. This could be due to issues with the video format or codec
          support.

        Notes
        -----

        - This function uses the `cv2.VideoCapture` class from OpenCV to open the
          video.
        - The function first checks if the video file exists before attempting to open it.

        """
        if not exists(video):
            raise FileNotFoundError(f"Video not found : {video}")
        cap: cv2.VideoCapture = cv2.VideoCapture(video)

        if not cap.isOpened():
            raise RuntimeError(f"Could not open the video : {video}")

        return cap


    def _get_video_output(self, output: str, cap: cv2.VideoCapture) -> cv2.VideoWriter:
        """
        Creates a video writer object for video output

        This function creates a cv2 VideoWriter object for writing video frames to a
        specified output file. It attempts to automatically set the output format to
        MP4 if no extension is provided.

        Parameters
        ----------

        - `output` (`str`): The desired path and filename for the output video.
        - `cap` (`cv2.VideoCapture`): A cv2 VideoCapture object representing the
          source video used to determine frame properties (FPS, width, height).

        Returns
        -------

        - `cv2.VideoWriter`: A cv2 VideoWriter object for writing video frames to
          the specified output file.

        Notes
        -----

        - This function uses the `cv2.VideoWriter` class from OpenCV to create the
          video writer object.
        - The function checks the provided `output` filename extension. If no extension
          is provided (ends with a dot '.'), the output filename is automatically
          appended with ".mp4" extension.
        - The video writer is configured with the following properties obtained from
          the provided `cap` object (cv2 VideoCapture):
            - Frame rate (FPS)
            - Frame width
            - Frame height

        """
        out = cv2.VideoWriter(
            output if splitext(basename(output))[1] == ".mp4" else f"{output}.mp4",
            cv2.VideoWriter_fourcc(*'mp4v'),
            round(cap.get(cv2.CAP_PROP_FPS)),
            (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        )

        return out

    def _release(self, cap: cv2.VideoCapture, out: cv2.VideoWriter) -> None:
        cap.release()
        out.release()
        cv2.destroyAllWindows()

    def gamma_on_image(self, image: list, gamma: int | float) -> list:
        """
        Applies gamma correction to an image

        This function applies gamma correction to an image and returns the processed image.

        Parameters
        ----------

        - `image` (`list` of `int`): A list representation of the image in grayscale format,
          where each element represents the intensity of a pixel (0-255).
        - `gamma` (`int | float`): Gamma correction factor. A value of 1.0 corresponds to
          no correction. Values less than 1.0 result in darker areas becoming darker
          (increased contrast) and values greater than 1.0 result in brighter areas
          becoming brighter (decreased contrast).

        Returns
        -------

        - `list` of `int`: A list representing the gamma-corrected grayscale image.

        Notes
        -----

        - This function utilizes OpenCV's `cv2.LUT` (Lookup Table) function for efficient
          gamma correction.
        - It creates a lookup table (LUT) by calculating the gamma-corrected intensity
          values for each possible pixel value (0-255).
        - The function then applies the LUT to the input image using `cv2.LUT` to
          achieve the desired gamma correction.

        """
        return cv2.LUT(image,
                       np.array(np.clip(pow(np.array(range(256)) / 255.0, gamma) * 255.0, 0, 255),
                                np.uint8))

    def gamma_on_video(self, video: str, gamma: int | float, output: str) -> None:
        """
        Applies gamma correction to a video and saves the result

        This function applies gamma correction to each frame of a video and saves the
        processed video to a specified output file.

        Parameters
        ----------

        - `video` (`str`): The path to the input video file.
        - `gamma` (`int | float`): Gamma correction factor. A value of 1.0 corresponds to
          no correction. Values less than 1.0 result in darker areas becoming darker
          (increased contrast) and values greater than 1.0 result in brighter areas
          becoming brighter (decreased contrast).
        - `output` (`str`): The path and filename for the output video file.

        Returns
        -------

        - `None`

        Notes
        -----

        - This function utilizes the following helper functions:
            - `_get_video_cap` to open the input video.
            - `_get_video_output` to create the output video writer.
            - `gamma_on_image` (assumed to be implemented elsewhere) to adjust gamma
              correction of a frame.
        - The function iterates over each frame of the video using a loop that continues
          until there are no more frames to read.
        - For each frame, the function calls the `gamma_on_image` helper function to
          adjust the gamma correction using the provided `gamma` value.
        - The processed frame is then written to the output video using the `out.write`
          method.
        - Finally, the function calls the `_release` helper function (assumed to be
          implemented elsewhere) to release the video capture and writer objects.
        """
        cap = self._get_video_cap(video)
        out = self._get_video_output(output, cap)

        while True:
            ret, frame = cap.read()

            if not ret:
                break

            frame = self.gamma_on_image(frame, gamma)

            out.write(frame)

        self._release(cap, out)

    def black_white_filter_on_image(self, image) -> list:
        """
        Applies a black and white filter to an image

        This function converts an image to grayscale (black and white) and returns it.

        Parameters
        ----------

        - `image` (`numpy.ndarray`): A NumPy array representing the image in BGR color
          format.

        Returns
        -------

        - `list` (of `int`): A list representation of the grayscale image. While OpenCV
          typically uses NumPy arrays for image data, some functions might return lists.
          It's recommended to convert the returned list back to a NumPy array for further
          processing using OpenCV functions.

        """
        return cv2.cvtColor(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2BGR)

    def black_white_filter_on_video(self, video: str, output: str):
        """
        Applies black and white filter to a video and saves the result

        This function applies a black and white filter to each frame of a video
        and saves the processed video to a specified output file.

        Parameters
        ----------

        - `video` (`str`): The path to the input video file.
        - `output` (`str`): The path and filename for the output video file.

        Returns
        -------

        - `None`

        Notes
        -----

        - This function utilizes the following helper functions:
            - `_get_video_cap` to open the input video.
            - `_get_video_output` to create the output video writer.
            - `black_white_filter_on_image` (assumed to be implemented elsewhere) to
              convert a frame to grayscale.
        - The function iterates over each frame of the video using a loop that continues
          until there are no more frames to read.
        - For each frame, the function calls the `black_white_filter_on_image` helper
          function to convert the frame to grayscale.
        - The processed frame is then written to the output video using the `out.write`
          method.
        - Finally, the function calls the `_release` helper function (assumed to be
          implemented elsewhere) to release the video capture and writer objects.

        """
        cap = self._get_video_cap(video)
        out = self._get_video_output(output, cap)

        while True:
            ret, frame = cap.read()

            if not ret:
                break

            frame = self.black_white_filter_on_image(frame)

            out.write(frame)

        self._release(cap, out)

    def apply_multi_filter_on_video(self, filters: list, video: str, output: str, **kwargs) -> None:
        """
        Applies multiple filters to a video and saves the result

        This function applies a sequence of image filters to each frame of a video
        and saves the processed video to a specified output file.

        Parameters
        ----------

        - `filters` (`list` of `str`): A list of filter names to be applied to the
          video frames in the order they are specified in the list. Supported filters
          include:
             - "black_white" (converts the frame to grayscale)
             - "gamma" (adjusts gamma correction of the frame - requires additional
                          keyword argument)
        - `video` (`str`): The path to the input video file.
        - `output` (`str`): The path and filename for the output video file.

        Kwargs
        ------

        - `gamma` (`float`, optional): Gamma correction factor for the "gamma" filter.
          Defaults to 1.0 (no correction).

        Returns
        -------

        - `None`

        Notes
        -----

        - This function utilizes the following helper functions:
            - `_get_video_cap` to open the input video.
            - `_get_video_output` to create the output video writer.
            - `black_white_filter_on_image` to convert a frame to grayscale.
            - `gamma_on_image` to adjust gamma correction of a frame.
        - The function iterates over each frame of the video using a loop that continues
          until there are no more frames to read.
        - For each frame, the function checks if the corresponding filter name ("black_white"
          or "gamma") is present in the `filters` list. If a filter is present, the
          corresponding helper function is called to apply the filter to the frame.
        - The processed frame is then written to the output video using the `out.write`
          method.
        - Finally, the function calls the `_release` helper function (assumed to be
          implemented elsewhere) to release the video capture and writer objects.

        """
        cap = self._get_video_cap(video)
        out = self._get_video_output(output, cap)

        while True:
            ret, frame = cap.read()

            if not ret:
                break

            if 'black_white' in filters:
                frame = self.black_white_filter_on_image(frame)

            if 'gamma' in filters:
                frame = self.gamma_on_image(frame, kwargs.get("gamma", 1.0))

            out.write(frame)

        self._release(cap, out)
