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
        return self._rbga.tobytes()

    @staticmethod
    def from_numpy(rgba: np.ndarray) -> "Image":
        assert len(rgba.shape) == 4 and rgba.dtype == np.uint8, (
            'The image must have 4 channels (RGBA) and uint8 dtype'
        )
        return Image(rgba)

    @staticmethod
    def from_bytes(b: bytes) -> "Image":
        rgba = np.frombuffer(b, np.uint8)
        return Image(rgba)
