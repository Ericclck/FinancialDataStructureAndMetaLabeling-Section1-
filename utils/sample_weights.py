import pandas as pd
import numpy as np

def get_concurrency(price_indices: pd.Series, first_touch : pd.Series, molecule : pd.Series = None) -> pd.Series:
    """
    Compute the concurrency of price bars

    Parameters
    ----------
    price_indices : pd.Series
        The index of the price bars
    first_touch : pd.Series
        The Series containing the first_touch
        index represents the start of the bar
        first_touch is the timestamp of the first touch of the barrier
    molecule : pd.Series
        The subset of price indices to be used
    
    Returns
    -------
    pd.Series
        The concurrency of price bars
    
    """
    # molecule[0] , first_touch[molecule].max() , first_touch[first_touch[molecule[-1]]]
    # molecule includes portion A, first_touch includes portion A,B, concurrency includes portion A,B,C
    # close unclosed first_touch
    first_touch = first_touch.fillna(price_indices[-1])
    # truncate first_touch
    if molecule is None:
        molecule = first_touch.index
    if not first_touch.index.is_monotonic_increasing:
        raise ValueError('first_touch.index must be monotonic increasing')
    first_touch = first_touch.loc[molecule[0] : first_touch[molecule].max()]
    # truncate price indices to first_touch.index[0] to first_touch.max()
    loc = price_indices.searchsorted(np.array([first_touch.index[0],first_touch.max()]))
    # for each sample in molecule[0] to first_touch[molecule].max(), add 1 to its span (start,end) in concurrency
    concurrency = pd.Series(0,index=price_indices[loc[0]:loc[1]+1])
    for start,end in first_touch.items():
        concurrency.loc[start:end] += 1
    # truncate concurrency to portion A,B
    return concurrency.loc[molecule[0]:first_touch[molecule].max()]


def get_uniqueness_from_concurrency(first_touch : pd.Series, concurrency: pd.Series, molecule : pd.Series = None) -> pd.Series:
    """
    Compute uniqueness per sample

    Parameters
    ----------
    first_touch : pd.Series
        The Series containing the first_touch
        index represents the start of the bar
        first_touch is the timestamp of the first touch of the barrier
    concurrency : pd.Series
        The concurrency of price bars
    molecule : pd.Series
        The subset of price indices to be used

    Returns
    -------
    pd.Series
        The concurrent weight of price bars
    """
    if molecule is None:
        molecule = first_touch.index
    uniqueness = pd.Series(0, index = molecule)
    # concurrent weight is sample harmonic average of concurrency
    for start,end in first_touch[molecule].items():
        uniqueness.loc[start] = (1/concurrency.loc[start : end]).mean()
    return uniqueness

def get_sample_weights(first_touch : pd.Series, concurrency : pd.Series, prices : pd.Series, molecule : pd.Series = None) -> pd.Series:
    """
    Compute the sample weights

    Parameters
    ----------
    first_touch : pd.Series
        The Series containing the first_touch
        index represents the start of the bar
        first_touch is the timestamp of the first touch of the barrier
    concurrency : pd.Series
        The concurrency of price bars
    prices : pd.Series
        The prices
    molecule : pd.Series
        The subset of price indices to be used
    
    Returns
    -------
    pd.Series
        The sample weights
    """
    # compute returns
    returns = np.log(prices).diff()
    # compute sample weights per sample
    if molecule == None:
        molecule = first_touch.index
    weights = pd.Series(index=first_touch.index)
    for start,end in first_touch.iteritems():
        weights[start] = (returns.loc[start:end]/concurrency.loc[start:end]).sum()
    return weights.abs()

def get_uniqueness_decay(uniqueness : pd.Series, c : float) -> pd.Series:
    """
    Compute decay factors

    Parameters
    ----------
    uniqueness : pd.Series
        The uniqueness of sample bars
    c : float
        A parameter that controls where linear function 'lands' on first quadrant
        c = -1 to 1

    Returns
    -------
    pd.Series
        The decay factors
    """
    x = uniqueness.sort_index().cumsum()
    if c >= 0:
        slope = (1-c)/x.iloc[-1]
    else:
        slope = 1/((1+c)*x.iloc[-1])
    constant = 1 - slope*x.iloc[-1]
    y = slope*x + constant
    y[y<0] = 0
    return y