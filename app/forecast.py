import itertools
import numpy as np
import pandas as pd
import statsmodels.api as sm
import os
import pickle
from statsmodels.tsa.stattools import adfuller
from sklearn.metrics import mean_squared_error

def gridSearch(dataset, stationarity):
    p = d = q = range(0, 2)
    pdq = list(itertools.product(p, d, q))
    seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]

    bestParameters = list()
    for param in pdq:
        for param_seasonal in seasonal_pdq:
            try:
                mod = sm.tsa.statespace.SARIMAX(dataset.values,
                                                order=param,
                                                seasonal_order=param_seasonal,
                                                enforce_stationarity=stationarity
                )

                results = mod.fit()
                bestParameters.append([param, param_seasonal, results.aic])
            except:
                continue

    aic_value_list = list()
    for i in range(len(bestParameters)):
        aic_value_list.append(bestParameters[i][2])
    
    minIndex = aic_value_list.index(min(aic_value_list))
    return bestParameters, minIndex

def trainModel(dataset, order, seasonal_order, stationarity):
    mod = sm.tsa.statespace.SARIMAX(dataset,
                                    order=order,
                                    seasonal_order=seasonal_order,
                                    enforce_stationarity=stationarity,
    )

    results = mod.fit()
    return results

def forecastedResult(model, step):
    forecast = model.get_forecast(steps=step)
    forecast_mean = forecast.predicted_mean
    return forecast_mean

def predictedResult(model):
    start = '2001-01-31'
    pred = model.get_prediction(start=pd.to_datetime(start), dynamic=False)

    y_predicted = pred.predicted_mean
    return y_predicted

def createForecastResult(dataset, column, isUpdated):
    modelpath = "./model/"
    model_files = [modelname for modelname in os.listdir(modelpath) if modelname.endswith('.pkl')]
    model_name = f"{column}.pkl"

    if any(md == model_name for md in model_files):
        if isUpdated is False:
            model = pickle.load(open(modelpath + model_name, 'rb'))
        else:
            statistic_test = adfuller(dataset, autolag='AIC')
            if statistic_test[0] > 0.05:
                stationarity = False
            else:
                stationarity = True

            AIC, minIndex = gridSearch(dataset, stationarity)
            
            order = AIC[minIndex][0]
            seasonal_order = AIC[minIndex][1]
            model = trainModel(dataset, order, seasonal_order, stationarity)
            pickle.dump(model, open(modelpath + model_name, 'wb'))
    else:
        statistic_test = adfuller(dataset, autolag='AIC')
        if statistic_test[0] > 0.05:
            stationarity = False
        else:
            stationarity = True

        AIC, minIndex = gridSearch(dataset, stationarity)
        
        order = AIC[minIndex][0]
        seasonal_order = AIC[minIndex][1]
        model = trainModel(dataset, order, seasonal_order, stationarity)
        pickle.dump(model, open(modelpath + model_name, 'wb'))

    step = 36
    predicted_result = predictedResult(model)
    forcasted_result = forecastedResult(model, step)

    return predicted_result, forcasted_result

def createForecastDataframe(dataset, isUpdated):
    df_forecast = pd.DataFrame({'' : []})
    df_predict = pd.DataFrame({'' : []})
    df_columns = dataset.columns
    for i in range(len(df_columns)):
        if i == 0:
            predict, forecast = createForecastResult(dataset[df_columns[i]], df_columns[i], isUpdated)
            df_predict = predict.to_frame(name=df_columns[i])
            df_forecast = forecast.to_frame(name=df_columns[i])
        else:
            df_predict[df_columns[i]], df_forecast[df_columns[i]] = createForecastResult(dataset[df_columns[i]], df_columns[i], isUpdated)
    return df_predict, df_forecast

def modelEvaluation(actual, predict):
    rmspe_error = list()
    df_columns = actual.columns
    for column in df_columns:
        y_pred = predict[column]
        y_truth = actual[column]['2001-01-31':]
        rmspe = 100 - ((np.sqrt(np.mean(np.square((y_truth - y_pred) / y_truth)))) * 100)
        rmspe_error.append(rmspe)
    return rmspe_error





