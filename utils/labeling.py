import numpy as np
from numba import njit
from numba import float64, int64
from utils.fast_ewma import _ewma
import pandas as pd
# from mlfinlab.util.multiprocess import mpPandasObj

@njit
def std_pct_change(close: np.ndarray, window: int64) -> np.ndarray:
    # Compute percent change of close prices
    pct_change = np.diff(close) / close[:-1]

    # Initialize an array to store std of pct_change
    stds = np.empty(len(pct_change) - window + 1)

    # Compute rolling std of pct_change
    for i in range(len(stds)):
        stds[i] = np.std(pct_change[i:i+window])
    
    return stds

@njit
def ewma_std_pct_change(close: np.ndarray, window: int64) -> np.ndarray:
    # Compute std of pct_change
    stds = std_pct_change(close, window)

    # Initialize an array to store ewma of stds
    ewma_stds = np.empty(len(stds))

    # Compute ewma of stds
    for i in range(len(ewma_stds)):
        ewma_stds[i] = _ewma(stds, window, i+window)

    return ewma_stds

def find_stop_loss_and_profit_taking(close : pd.Series, events: pd.DataFrame, scalers_for_horizontal_barriers : tuple[float,float] , molecule ) -> pd.DataFrame:
    """
    Find stop loss and profit taking levels

    Parameters
    ----------
    close : pd.Series
        Close prices
    events : pd.DataFrame
        DataFrame of events
        Vertical barrier column represents the timestamp of when the vertical barrier is reached
        Side column represents the side of the bet
    scalers_for_horizontal_barriers : tuple(float,float)
        Tuple of scalers for horizontal barriers
    molecule : list
        Indices of events

    Returns
    -------
    pd.DataFrame
        DataFrame of indices of touching barriers
        vertical_barrier column represents the timestamp of when the vertical barrier is reached
        stop_loss column represents the timestamp of when the stop loss barrier is reached
        profit_taking column represents the timestamp of when the profit taking barrier is reached
    """
    events_parallel = events.loc[molecule]
    out = events_parallel[['vertical_barrier']].copy(deep=True)
    # out['stop_loss'] = pd.Series(index=events_parallel.index)
    # out['profit_taking'] = pd.Series(index=events_parallel.index)
    # Get price levels, if horizontal barriers are specified
    if scalers_for_horizontal_barriers[0] > 0:
        pt_level = events_parallel['target'] * scalers_for_horizontal_barriers[0]
    else:
        pt_level = pd.Series(index=events_parallel.index)
    if scalers_for_horizontal_barriers[1] > 0:
        sl_level = -events_parallel['target'] * scalers_for_horizontal_barriers[1]
    else:
        sl_level = pd.Series(index=events_parallel.index)

    # Get events , if vertical barriers are not specified, use the last index of close
    for loc, vertical_barrier in events_parallel['vertical_barrier'].fillna(close.index[-1]).items():
        closing_prices = close.loc[loc:vertical_barrier]
        cum_returns = (closing_prices / close[loc] - 1) * events_parallel.at[loc, 'side']
        out.loc[loc, 'stop_loss'] = cum_returns[cum_returns < sl_level[loc]].index.min()
        out.loc[loc, 'profit_taking'] = cum_returns[cum_returns > pt_level[loc]].index.min()
    return out

def get_events(close : pd.DataFrame, sampling_indices : pd.Series , scalers_for_horizontal_barriers : tuple[float,float],target : pd.Series, min_return : float, num_threads : int , vertical_barriers : pd.Series, side : pd.Series = None) -> pd.DataFrame:
    """
    get first touch indices

    Parameters
    ----------
    close : pd.DataFrame
        Close prices
    sampling_indices : pd.Series
        Indices of sampling
    scalers_for_horizontal_barriers : tuple(float,float)
        Tuple of scalers for horizontal barriers
    target : pd.Series
        Target values
    min_return : float
        Minimum return
    num_threads : int
        Number of threads
    vertical_barriers : pd.Series
        Vertical barriers

    Returns
    -------
    pd.DataFrame
        DataFrame of indices of touching barriers
        first_touch_index column represents the timestamp of when the first touch barrier is reached
        target column represents the target returns
    """
    # if target is in ticks index
    if len(target) >= len(sampling_indices):
        target = target.loc[sampling_indices]
    target = target[target > min_return]
    # get vertical barriers
    if vertical_barriers is None:
        vertical_barriers = pd.Series(pd.NaT, index=sampling_indices)
    # Construct events object
    if side is None:
        betting_side = pd.Series(1., index=target.index)
        # protection against asymmetric targets when side is not provided
        scalers_for_horizontal_barriers = [scalers_for_horizontal_barriers[0],scalers_for_horizontal_barriers[0]]
    else:
        betting_side = side.loc[target.index]
    events = pd.concat({'side': betting_side,
                        'vertical_barrier': vertical_barriers,
                        'target': target}, axis=1).dropna(subset=['target'])

    # Get events when first touch barrier is reached
    # if num_threads == 1:
    first_touch_events = find_stop_loss_and_profit_taking(close, events, scalers_for_horizontal_barriers, events.index)
    # else:
    #     first_touch_events = mpPandasObj(find_stop_loss_and_profit_taking, ('molecule', sampling_indices), num_threads, close=close, events=events, scalers_for_horizontal_barriers=scalers_for_horizontal_barriers)
    events['first_touch_index'] = first_touch_events.dropna(how='all').min(axis=1).astype(int)
    if side is None:
        events = events.drop(columns=['side'])
    return events

def get_labels(events : pd.DataFrame, close : pd.Series) -> pd.DataFrame:
    """
    Compute labels or meta-labels

    Parameters
    events : pd.DataFrame
        DataFrame of events
        first_touch_index column represents the timestamp of when the first touch barrier is reached
        target column represents the target returns
        side column represents the side of the bet (Optional)
    close : pd.Series
        Close prices
    
    Returns
    -------
    pd.DataFrame
        DataFrame of labels
        label column represents the label
        return column represents the return
    """
    # Get events when first touch barrier is reached
    events_ = events.dropna(subset=['first_touch_index']).copy()
    relevant_close = close.reindex(events_.index.union(events_['first_touch_index']).drop_duplicates())
    # Create out object
    out = pd.DataFrame(index=events_.index)
    out['return'] = relevant_close.loc[events_['first_touch_index']].values / relevant_close.loc[events_.index] - 1
    #meta-labeling
    if 'side' in events_:
        out['return'] *= events_['side']
    # label is set to -1 or 1
    out['label'] = np.sign(out['return'])
    #meta-labeling
    if 'side' in events_:
        out.loc[out['return'] <= 0, 'label'] = 0
        # change name of label column to meta_label
        out = out.rename(columns={'label':'meta_label'})
    else:
        # any label where first touch index == vertical barrier is set to 0
        out.loc[events_['vertical_barrier'] == events_['first_touch_index'], 'label'] = 0
    return out

def get_vertical_barriers(ticks_indices : pd.Series,rb_indices : pd.Series,num_ticks : int = 100) -> pd.Series:
    """
    Get vertical barriers

    Parameters
    ----------
    ticks_indices : pd.Series
        Indices of ticks (id)
    rb_indices : pd.Series
        Indices of dollar bars (id)
    num_ticks : int
        Number of bars
    
    Returns
    -------
    pd.Series
        Series of vertical barriers
    """
    vertical_barriers = np.zeros(len(rb_indices),dtype=int)
    for i in range(len(rb_indices)):
        if rb_indices[i] + num_ticks < ticks_indices[len(ticks_indices)-1]:
            vertical_barriers[i] = rb_indices[i]+num_ticks
        else:
            vertical_barriers[i] = ticks_indices[len(ticks_indices)-1]
    vertical_barriers = pd.Series(vertical_barriers,index=rb_indices)
    return vertical_barriers