
import cv2
from Simulate_springs import SpringsSystem
import numpy as np

def create_video(data, title="SimulationSprings.mp4", size=(720, 720), normalize=(200., 300.), fps=24):
    """
    Create a video with a simulation.
    Arguments:
        data (pd.DataFrame): Simulated data.
        title (str): title of the file
        size (tuple): size of the video
        normalize (tuple) : where to place the bodies inside the picture
        fps (int) : speed of video
    """

    min_ = np.min(data.values)
    max_ = np.max(data.values)
    a = normalize[0]/(max_ - min_)
    b = normalize[1] - normalize[0]*min_/(max_ - min_)
    normalized_data = a*data + b
    normalized_data = normalized_data.astype(int)
    min_norm = np.min(normalized_data.values)
    max_norm = np.max(normalized_data.values)
    duration = len(normalized_data.index)
    out = cv2.VideoWriter(title, cv2.VideoWriter_fourcc(*'mp4v'), fps, (size[1], size[0]), False)
    for d in range(duration):
        mat = np.zeros(size, dtype='uint8')
        mat[min_norm, size[1]//2 - 10:size[1]//2 + 10] = 250
        mat[max_norm, size[1]//2 - 10:size[1]//2 + 10] = 250
        #mat[mat.shape[0]-100:, mat.shape[1]-10:] = 250
        for col in normalized_data:
            if col[0] == 'x':
                mat[normalized_data[col].iloc[d]:normalized_data[col].iloc[d]+5, size[1]//2:size[1]//2 + 5] = 200
        out.write(mat)
    out.release()
