#!/usr/bin/env python3

import pytest
import os
import pathlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import logging
import math
import torch

from neuralprophet import NeuralProphet, set_random_seed, forecaster
from neuralprophet import df_utils

log = logging.getLogger("NP.test")
log.setLevel("WARNING")
log.parent.setLevel("WARNING")

DIR = pathlib.Path(__file__).parent.parent.absolute()
DATA_DIR = os.path.join(DIR, "tests", "test-data")
PEYTON_FILE = os.path.join(DATA_DIR, "wp_log_peyton_manning.csv")
AIR_FILE = os.path.join(DATA_DIR, "air_passengers.csv")
YOS_FILE = os.path.join(DATA_DIR, "yosemite_temps.csv")
NROWS = 256
EPOCHS = 1
BATCH_SIZE = 128
LR = 1.0

PLOT = False


def test_trend_global_local_modeling():
    ### TREND GLOBAL LOCAL MODELLING - NO EXOGENOUS VARIABLES
    log.info("Global Modeling + Global Normalization")
    df = pd.read_csv(PEYTON_FILE, nrows=512)
    df1_0 = df.iloc[:128, :].copy(deep=True)
    df1_0["ID"] = "df1"
    df2_0 = df.iloc[128:256, :].copy(deep=True)
    df2_0["ID"] = "df2"
    df3_0 = df.iloc[256:384, :].copy(deep=True)
    df3_0["ID"] = "df3"
    m = NeuralProphet(
        n_forecasts=2, n_lags=10, epochs=EPOCHS, batch_size=BATCH_SIZE, learning_rate=LR, trend_global_local="local"
    )
    train_df, test_df = m.split_df(pd.concat((df1_0, df2_0, df3_0)), valid_p=0.33, local_split=True)
    m.fit(train_df)
    future = m.make_future_dataframe(test_df)
    forecast = m.predict(future)
    metrics = m.test(test_df)
    forecast_trend = m.predict_trend(test_df)
    forecast_seasonal_componets = m.predict_seasonal_components(test_df)
    if PLOT:
        for key, df in forecast.groupby("ID"):
            fig1 = m.plot(df)
            fig2 = m.plot_parameters(df_name=key)
            fig3 = m.plot_parameters()


def test_regularized_trend_global_local_modeling():
    ### TREND GLOBAL LOCAL MODELLING - NO EXOGENOUS VARIABLES
    log.info("Global Modeling + Global Normalization")
    df = pd.read_csv(PEYTON_FILE, nrows=512)
    df1_0 = df.iloc[:128, :].copy(deep=True)
    df1_0["ID"] = "df1"
    df2_0 = df.iloc[128:256, :].copy(deep=True)
    df2_0["ID"] = "df2"
    df3_0 = df.iloc[256:384, :].copy(deep=True)
    df3_0["ID"] = "df3"
    m = NeuralProphet(n_lags=10, epochs=EPOCHS, trend_global_local="local", trend_reg=1)
    train_df, test_df = m.split_df(pd.concat((df1_0, df2_0, df3_0)), valid_p=0.33, local_split=True)
    m.fit(train_df)
    future = m.make_future_dataframe(test_df)
    forecast = m.predict(future)
    metrics = m.test(test_df)
    forecast_trend = m.predict_trend(test_df)
    forecast_seasonal_componets = m.predict_seasonal_components(test_df)


def test_seasonality_global_local_modeling():
    ### SEASONALITY GLOBAL LOCAL MODELLING - NO EXOGENOUS VARIABLES
    log.info("Global Modeling + Global Normalization")
    df = pd.read_csv(PEYTON_FILE, nrows=512)
    df1_0 = df.iloc[:128, :].copy(deep=True)
    df1_0["ID"] = "df1"
    df2_0 = df.iloc[128:256, :].copy(deep=True)
    df2_0["ID"] = "df2"
    df3_0 = df.iloc[256:384, :].copy(deep=True)
    df3_0["ID"] = "df3"
    m = NeuralProphet(
        n_forecasts=2, n_lags=10, epochs=EPOCHS, batch_size=BATCH_SIZE, learning_rate=LR, season_global_local="local"
    )
    train_df, test_df = m.split_df(pd.concat((df1_0, df2_0, df3_0)), valid_p=0.33, local_split=True)
    m.fit(train_df)
    future = m.make_future_dataframe(test_df)
    forecast = m.predict(future)
    metrics = m.test(test_df)
    forecast_trend = m.predict_trend(test_df)
    forecast_seasonal_componets = m.predict_seasonal_components(test_df)
    if PLOT:
        for key, df in forecast.groupby("ID"):
            fig1 = m.plot(df)
            fig2 = m.plot_parameters(df_name=key)
            fig3 = m.plot_parameters()