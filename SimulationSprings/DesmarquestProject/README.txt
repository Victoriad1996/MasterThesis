READ ME:

The project aims to set an environment for simulation of n bodies connected by springs.

SimulationNotebook.ipynb : In the notebook SimulationNotebook.ipynb you will find figures and explanation of the model. Moreover, some examples have been ran in the notebook.

Simulate_springs.py : Contains the main class SpringsSystem. It has different method for initialization(__init__), derivation of the system (vectorfield), simulation for a time frame t (simulate), save the data (save_data), the constraint to which the system submitted to (constraint), plot the positon of the masses (plot_position), plot the velocity of the masses (plot_velocity)

integration_methods.py : Contains the integration methods for the simulation. Two are available (they are explained in the notebook): EulerScheme, and ImplicitMidpoint.

create_video.py : Contains one method that creates a video that records the activity of the masses (create_video). Needed for this: package cv2 (pip install opencv-python). Not mandatory to run the simulation ! There is a video in the folder.

SimulationSpring.mp4 : A video that records the activity of the masses.

Requirements: 
numpy
csv
pandas
matplotlib.pyplot

If want to create video: 
Requirements:
cv2 (pip install opencv-python)