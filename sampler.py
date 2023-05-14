from lib import *

def read_data(date, instrument, time_step):
	path = os.path.join(PRICE_FLD, date, instrument+'.csv')
	if not os.path.exists(path):
		print('no such file: '+path)
		return None

	df_raw = pd.read_csv(path, parse_dates=['time'], index_col='time')
	df = df_raw.resample(time_step, how='last').fillna(method='ffill')
	return df['spot'].values



