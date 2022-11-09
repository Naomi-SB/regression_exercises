#plot_residuals(y, yhat): creates a residual plot

#regression_errors(y, yhat): returns the following values:
    #sum of squared errors (SSE)
    #explained sum of squares (ESS)
    #total sum of squares (TSS)
    #mean squared error (MSE)
    #root mean squared error (RMSE)
#baseline_mean_errors(y): computes the SSE, MSE, and RMSE for the baseline model
#better_than_baseline(y, yhat): returns true if your model performs better than the baseline, otherwise false
#We will compute evaluation metrics, such as Mean Squared Error, 
# #Root Mean Squared Error, or Median Absolute Error, for the model and the baseline, 
# and compare them to each other.


def plot_residuals(y, yhat):
    
    residuals = y - yhat
  
    sns.scatterplot(x=y, y= yhat)
    plt.title('Plot of Residuals vs. Target Variable')
    plt.show()


def regression_errors(y, yhat):
    '''
    Takes in y and yhat and returns sum of squared errors (SSE) 
    explained sum of squares (ESS), total sum of squares (TSS) 
    mean squared error (MSE), and root mean squared error (RMSE)
    '''

    MSE = metric.mean_squared_error(y, yhat)
    SSE = MSE*len(y)
    ESS = sum((yhat - y.mean())**2)
    TSS = ESS + SSE
    RMSE = sqrt(MSE)
    
    return SSE, ESS, TSS, MSE, RMSE
    
def baseline_mean_errors(y):
    '''
    Takes in y and returns SSE, MSE and RMSE for baseline
    '''
    baseline = np.repeat(y.mean(), len(y))
    
    MSE = metric.mean_squared_error(y, baseline)
    SSE = MSE*len(y)
    RSME = sqrt(MSE)
    
    return SSE_baseline, MSE_baseline, RMSE_baseline

def better_than_baseline(y, yhat):
    '''
    Takes in y and yhat and compares SSE and SSE_baseline and 
    returns True if your model is better than baseline 
    and False if it is not.
    '''
    SSE, ESS, TSS, MSE, RMSE = regression_errors(y, yhat)
    
    SSE_baseline, MSE_baseline, RMSE_baseline = baseline_mean_errors(y)
    
    if SSE < SSE_baseline:
        return True