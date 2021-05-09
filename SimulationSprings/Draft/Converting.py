import numpy as np
import cv2

class cvWriter:
    # Define the codec and create VideoWriter object

    def __init__(self, filePathName, frameDim, frate=24., codec='MP42'):
        # For whatever reason OPENCV needs dimensions in the opposite order
        frameDimT = (frameDim[1], frameDim[0])

        fourcc = cv2.VideoWriter_fourcc(*codec)
        self._out = cv2.VideoWriter(filePathName, fourcc, float(frate), frameDimT, isColor=False)

    # Just necessary to use 'with' command
    def __enter__(self):
        return self

    # Destructor for the 'with' command
    # Release everything if job is finished
    def __exit__(self, exc_type, exc_value, traceback):
        self._out.release()
        # cv2.destroyAllWindows()

    # Write matrix frame to file
    def write(self, mat):
        self._out.write(mat.astype(np.uint8))


def convert_to_movie(list_frames: list, height: int, width: int, filePathName: str, num_frames: int = 10):
    """
    Given a list of frames, converts it into a movie.
    :param list_frames: List of frames (matrices).
    :type list_frames: list of np.array
    :param height: height of a frame
    :type height: int
    :param width: width of a frame
    :type width: int
    :param filePathName: the path where to save the movie
    :type filePathName: str
    :param num_frames: number of frames per image.
    :type num_frames: int
    """
    base_matrix = np.zeros((width, height, 4))
    base_matrix[:, :, 3] = 255 * np.ones((width, height))

    FrameDim = (width, height)
    with cvWriter(filePathName, FrameDim) as vidwriter:
        for frame in list_frames:
            base_matrix[:, :, 1] = frame
            for _ in range(num_frames):
                vidwriter.write(base_matrix)
    return base_matrix
