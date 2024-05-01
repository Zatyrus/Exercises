## Created by @Zatyrus
## Created at 2024-05-01

## Dependencies
import numpy as np
from typing import Tuple, NoReturn
from tqdm import tqdm, tgrange, trange
import matplotlib.pyplot as plt
import datashader as ds
import pandas as pd
import holoviews as hv
import colorcet as cc


## params
n:int = 25000
odds:float = 0.7
seed:int = 1
interactive:bool = False

## change default recursion limit
#import sys
#sys.setrecursionlimit(n+4)

## transformation matrices
A:np.ndarray = np.array(([0.5, 0.5], [-0.5, 0.5]))
B:np.ndarray = np.array(([0.5, -0.5], [0.5, 0.5]))
offset:np.ndarray = np.array([0.5, 0.5])

## util
def seed_random(seed:int)->NoReturn:
    np.random.seed(seed)

def transformation_step(x:np.ndarray, A:np.ndarray, B:np.ndarray, offset:np.ndarray)->tuple[np.ndarray, np.ndarray]:
    x1 = np.dot(A, x)
    x2 = np.dot(B, x) - offset
    return x1, x2

def choose_next_point(last_points:tuple[np.ndarray, np.ndarray], odds:float)->np.ndarray:
    if np.random.rand() < odds:
        return last_points[0]
    else:
        return last_points[1]

## generation works, but is limited due to pythons recursion limit
def generate_dragon_recursive(points:list, odds:float, n:int, A:np.ndarray, B:np.ndarray, offset:np.ndarray)->np.ndarray:
    if len(points) < n:
        
        if len(points) == 0:
            points = [np.random.random(2)]
            x = points[-1]
        else:
            x = choose_next_point(points[-1], odds)

        return generate_dragon_recursive(points = points + [transformation_step(x, A, B, offset)],
                                         odds = odds,
                                         n = n,
                                         A = A,
                                         B = B,
                                         offset = offset)
    else:
        return np.row_stack(points)    
        
## easy straight forward generation. it even is faster than the recursive one
def generate_dragon_loop(n:int, 
                         odds:float, 
                         A:np.ndarray, 
                         B:np.ndarray, 
                         offset:np.ndarray)->np.ndarray:    
    # random start
    x = np.random.random(2)
    points = [x]
    # loop
    for _ in trange(n):
        points.append(transformation_step(x, A, B, offset))
        x = choose_next_point(points[-1],
                              odds=odds)
    return np.row_stack(points)

def plot_dragon_curve(points:np.ndarray)->NoReturn:
    
    fig, ax = plt.subplots(1,1, figsize = (10, 10), dpi = 100)
    
    # plot
    ax.scatter(points[:, 0], points[:, 1], s = 2, c = np.arange(len(points)), cmap = 'plasma')
    fig.tight_layout()
    plt.show()
    
def plot_dragon_curve_datashader(points:np.ndarray)->NoReturn:
    
    df = pd.DataFrame(points, columns = ['x', 'y'])
    df['c'] = np.arange(len(df))
    cvs = ds.Canvas(plot_width=800, plot_height=800)
    cvs.color_key_cmap = 'plasma'
    cvs.color_key = 'c'
    agg = cvs.points(df, 'x', 'y')
    img = ds.transfer_functions.shade(agg)
    ds.transfer_functions.set_background(img, 'black')
    img.to_pil().show()
    
def plot_dragon_curve_datashader_cmap(points:np.ndarray)->NoReturn:
    df = pd.DataFrame(points, columns = ['x', 'y'])
    df['c'] = np.arange(len(df))
    
    agg = ds.Canvas().points(df, 'x', 'y')
    ds.tf.set_background(ds.tf.shade(agg, cmap=cc.fire), "black")
    ds.tf.shade(agg, cmap=cc.fire).to_pil().show() # to...x
    
def save_dragon_curve_datashader_cmap(points:np.ndarray)->NoReturn:
    df = pd.DataFrame(points, columns = ['x', 'y'])
    df['c'] = np.arange(len(df))
    
    agg = ds.Canvas().points(df, 'x', 'y')
    ds.tf.set_background(ds.tf.shade(agg, cmap=cc.fire), "black")
    ds.tf.shade(agg, cmap=cc.fire).to_pil().save('dragon_curve.png') # to...x
    
def plot_dragon_curve_holoviews(points:np.ndarray)->NoReturn:
    
    df = pd.DataFrame(points, columns = ['x', 'y'])
    df['c'] = np.arange(len(df))
    hv.extension('bokeh')
    points:hv.Points = hv.Points(df)
    points.opts(width=800, height=800, color = 'c', cmap = 'fire', tools=['hover'], size=2)
    hv.save(points, 'dragon_curve.html')

if __name__ == "__main__":   
    seed_random(seed) 
    points = generate_dragon_loop(n = n, 
                                  odds = odds,
                                  A = A,
                                  B = B,
                                  offset = offset)
    plot_dragon_curve_holoviews(points)

else:
    pass
