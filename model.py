import statsmodels.api         as sm
import statsmodels.formula.api as smf
from scipy import stats

class LinearModel:

    def __init__(self, X, y, columns):
        self.X = X
        self.y = y
        self.columns = columns
        self.model = None


    def train(self,fts=None):
        if(fts == None):
            # If None fts, use all features by default
            fts = self.X.columns

        Xtr = self.X[fts].to_numpy()
        Xtr = sm.add_constant(Xtr)
        model = sm.OLS(self.y.to_numpy(), Xtr).fit()

        self.model = model
        return model


    def predict(self,Xtt):
        return self.model.predict(Xtt)

    def get_X(self):
        return self.X
    
    def get_columns(self):
        return self.columns
    
    def get_y(self):
        return self.y

