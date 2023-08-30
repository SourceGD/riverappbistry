from os.path import exists, basename, splitext
import cv2
import numpy as np

from libs.pyorc import Frames


class Filters():

    def _get_video_cap(self, video: str) -> cv2.VideoCapture:
        if not exists(video):
            raise FileNotFoundError(f"Video not found : {video}")
        
        cap: cv2.VideoCapture = cv2.VideoCapture(video)

        if not cap.isOpened():
            raise RuntimeError(f"Could not open the video : {video}")

        return cap
    
    def _get_video_output(self, output: str, cap: cv2.VideoCapture) -> cv2.VideoWriter:
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
        return cv2.LUT(image, np.array(np.clip(pow(np.array(range(256)) / 255.0, gamma) * 255.0, 0, 255), np.uint8))
    
    def gamma_on_video(self, video: str, gamma: int | float, output: str) -> None:
        cap = self._get_video_cap(video)
        out = self._get_video_output(output, cap)

        while True:
            ret, frame = cap.read()

            if not ret:
                break

            frame = self.gamma_on_image(frame, gamma)

            out.write(frame)

        self._release(cap, out)
        return

    def black_white_filter_on_image(self, image) -> list:
        return cv2.cvtColor(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2BGR)
    
    def black_white_filter_on_video(self, video: str, output: str) -> None:
        cap = self._get_video_cap(video)
        out = self._get_video_output(output, cap)
        
        while True:
            ret, frame = cap.read()

            if not ret:
                break

            frame = self.black_white_filter_on_image(frame)

            out.write(frame)

        self._release(cap, out)
        return
    
    """ def normalize_on_image(self, image, samples: int = 15) -> list:
        return Frames(image).normalize(samples)

    def normalise_on_video(self, video: str, output: str) -> None:
        cap = self._get_video_cap(video)
        out = self._get_video_output(output, cap)
        
        while True:
            ret, frame = cap.read()

            if not ret:
                break

            frame = self.normalise_on_video(frame)

            out.write(frame)

        self._release(cap, out)
        return

    def time_diff_on_image(self, image, threshold: float = 2, abs: bool = False) -> list:
        return Frames(image).time_diff(threshold, abs)
    
    def edge_detect(self, image, wdw_1: int = 2, wdw_2: int = 2) -> list:
        return Frames(image).edge_detect(wdw_1, wdw_2) """
    
    def apply_multi_filter_on_video(self, filters: list, video: str, output: str, **kwargs) -> None:
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
            
            """ if 'normalize' in filters:
                frame = self.normalize_on_image(frame, kwargs.get("samples", 15)) """

            out.write(frame)

        self._release(cap, out)
        return

