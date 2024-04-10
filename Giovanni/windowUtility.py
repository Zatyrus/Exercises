import numpy as np
import plotly.graph_objects as go
from plotly.offline import iplot, init_notebook_mode
import matplotlib.pyplot as plt


## Class to handle the windowing of the data

class WindowUtility(object):
    
    data:np.ndarray
    seeds:list
    
    def __init__(self, data:np.ndarray, seeds:list) -> None:
        self.__data = data
        self.__seeds = seeds
            
    # Properties
    @property
    def data(self) -> np.ndarray:
        return self.__data
    @data.setter
    def data(self, data:np.ndarray) -> None:
        self.__data = data
    
    @property
    def seeds(self) -> list:
        return self.__seeds
    @seeds.setter
    def seeds(self, seeds:list) -> None:
        self.__seeds = seeds
    
    # Methods
    def setup_windows(self, window_size_row:int=5, window_size_column:int = 5) -> np.ndarray:
        """Window the data using the seeds and window size."""
        # Get the shape of the data
        shape = (2*window_size_row+1, 2*window_size_column+1)
        # Create new dictionary to hold the windows
        windowed_data = {seed:np.zeros(shape=shape) for seed in self.__seeds}
        # Loop through the seeds
        for seed in self.__seeds:
            # Get the coordinates of the seed
            x, y = seed[0], seed[1]
            # Get the windowed data
            windowed_data[seed] = self.data[x-window_size_row:x+window_size_row+1, y-window_size_column:y+window_size_column+1]
        return windowed_data
    
    def get_window_argmax(self, windowed_data:dict) -> dict:
        """Get the argmax of the windowed data."""
        return {seed:np.unravel_index(np.argmax(window, axis=None), window.shape) for seed, window in windowed_data.items()}
       
    # Helper
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        pass

class WindowUtilityStatic(object):
    @staticmethod
    def quick_window(data:np.ndarray, seeds:list, window_size_row:int=5, window_size_column:int = 5)->dict:
        with WindowUtility(data, seeds) as engine:
            return engine.setup_windows(window_size_row, window_size_column)
    
    @staticmethod
    def multi_window(data:dict, seeds:list, window_size_row:int=5, window_size_column:int = 5)->dict:
        windowed_data = {}
        for key in data:
            with WindowUtility(data[key], seeds) as engine:
                windowed_data[key] = engine.setup_windows(window_size_row, window_size_column)
        return windowed_data
    
    @staticmethod
    def quick_winMax(data:np.ndarray, seeds:list, window_size_row:int=5, window_size_column:int = 5)->dict:
        with WindowUtility(data, seeds) as engine:
            windowed_data = engine.setup_windows(window_size_row, window_size_column)
            win_argmax = engine.get_window_argmax(windowed_data)
            try:
                assert np.all([(window_size_row, window_size_column) == win_argmax[seed] for seed in seeds])
            except AssertionError:
                print("Window size and argmax do not match.\nThus, the max is not in the center of the window.\nPlease check the window size and seeds.")
            return win_argmax
        
    @staticmethod
    def plot_window(data:dict, seed:tuple, window_size_row:int=5, window_size_column:int = 5, figsize:tuple=(800,800), alpha:float = 0.70, is_notebook: bool = True) -> (plt.Figure, plt.Axes):
        if is_notebook:
            init_notebook_mode()
        # Get the data to plot
        plot_data = []
        for key in data:
            with WindowUtility(data[key], [seed]) as engine:
                plot_data.append(engine.setup_windows(window_size_row, window_size_column)[seed])    
                    
        plot_data = [go.Surface(z = data, opacity=alpha, colorscale=cmap, showscale=False) for data, cmap in zip(plot_data, ["Reds", "Greens", "Blues", "Oranges", "Purples", "Greys", "YlOrBr", "YlOrRd", "Bluered", "RdBu", "Reds", "Blues", "Greens", "YlGnBu", "YlGn"])]
        
        # Create the figure
        fig = go.Figure(data=plot_data)
        
        fig.update_traces(contours_z=dict(show=True, usecolormap=True,
                                  highlightcolor="black", project_z=True))

        fig.update_layout(title='Surface Comaparison', autosize=False,
                        scene_camera_eye=dict(x=1.87, y=0.88, z=-0.64),
                        width=figsize[0], height=figsize[1],
                        margin=dict(l=65, r=50, b=65, t=90)
                        )  
        
        return iplot(fig)
