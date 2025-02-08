from pathlib import Path

import cv2
import numpy as np


class Image:
    def __init__(self, data) -> None:
        self._rbga: np.ndarray = data

    def to_numpy(self) -> np.ndarray:
        """
        :return: rgba image as np.uint8 array
        """
        return self._rbga

    def to_bytes(self) -> bytes:
        return cv2.imencode('.png', self._rbga)[1].tobytes()

    def to_file(self, p: Path) -> None:
        p.write_bytes(self.to_bytes())

    @staticmethod
    def from_numpy(rgba: np.ndarray) -> "Image":
        assert rgba.dtype == np.uint8, (
            'The image must have uint8 dtype'
        )
        return Image(rgba)

    @staticmethod
    def from_bytes(b: bytes) -> "Image":
        nparr = np.frombuffer(b, np.uint8)
        rgba = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)
        print(rgba.shape)
        return Image(rgba)

    @staticmethod
    def from_file(p: Path) -> "Image":
        return Image.from_bytes(p.read_bytes())
