import numpy as np
from scipy.stats import pearsonr, spearmanr, kendalltau


class avstand_beregn:
    def __init__(self, nba_max, nba_mean, nor_max, nor_mean, columns):
        self.nba_max=nba_max
        self.nba_mean=nba_mean
        self.nor_max=nor_max
        self.nor_mean=nor_mean
        self.columns=columns

    def init_nordberg(self, nor_stat, vekt=None, felles_max=None ,felles_mean=None):
        if felles_mean is not None:
            self.nor_mean = felles_mean
            self.nba_mean = felles_mean
        if felles_max is not None:
            self.nor_max = felles_max
            self.nba_max = felles_max
        if vekt is None:
            self.vekt = np.ones(len(nor_stat))
        else:
            self.vekt = vekt

        self.nor_stat = nor_stat

    def init_nba(self,nba_stat):
        assert len(nba_stat) == len(self.nor_stat), 'stat linjer ulik lengde'

        self.nba_stat = nba_stat

    def pearsonish(self):
        num = 0
        x_denum = 0
        y_denum = 0
        for i in range(len(self.columns)):
            x_mean = self.nor_mean[i]/self.nor_max[i]
            y_mean = self.nba_mean[i]/self.nba_max[i]

            xi = self.nor_stat[i]
            yi = self.nba_stat[i]

            num += (xi - x_mean)*(yi - y_mean)
            x_denum += (xi - x_mean)**2
            y_denum += (yi - y_mean)**2

        return num/(np.sqrt(x_denum)*np.sqrt(y_denum))

    def numpy_corr(self):
        corr = np.corrcoef(self.nor_stat, self.nba_stat)
        return min([corr[0][1], corr[1][0]])

    def scipy_corr(self, type='pearson'):
        assert type in ['pearson', 'spearman', 'kendall'], \
            f'type "{type}" not valid! \n type must be either "pearson", "spearman" or "kendall" '
        if type=='pearson':
            return pearsonr(self.nor_stat, self.nba_stat)[0]
        elif type=='spearman':
            return spearmanr(self.nor_stat, self.nba_stat)[0]
        else:
            return kendalltau(self.nor_stat, self.nba_stat)[0]

    def diff(self,  _type='abs'):
        assert len(self.vekt) == len(self.nor_stat), 'vekting mangler/har for mange kolonner'

        s = 0
        for nor, nba, w in zip(self.nor_stat,self.nba_stat, self.vekt):
            if _type== 'abs':
                s += abs(nor - nba)*w
            else:
                s += (nor-nba)*w

        return -abs(s)
