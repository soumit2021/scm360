from lib import *

def read_data(date, instrument, time_step):
	path = os.path.join(PRICE_FLD, date, instrument+'.csv')
	if not os.path.exists(path):
		print('no such file: '+path)
		return None

	df_raw = pd.read_csv(path, parse_dates=['time'], index_col='time')
	df = df_raw.resample(time_step, how='last').fillna(method='ffill')
	return df['spot'].values



class Sampler:

	def load_db(self, fld):

		self.db = pickle.load(open(os.path.join(fld, 'db.pickle'),'rb'))
		param = json.load(open(os.path.join(fld, 'param.json'),'rb'))
		self.i_db = 0
		self.n_db = param['n_episodes']
		self.sample = self.__sample_db
		for attr in param:
			if hasattr(self, attr):
				setattr(self, attr, param[attr])
		self.title = 'DB_'+param['title']


	def build_db(self, n_episodes, fld):
		db = []
		for i in range(n_episodes):
			prices, title = self.sample()
			db.append((prices, '[%i]_'%i+title))
		os.makedirs(fld)
		pickle.dump(db, open(os.path.join(fld, 'db.pickle'),'wb'))
		param = {'n_episodes':n_episodes}
		for k in self.attrs:
			param[k] = getattr(self, k)
		json.dump(param, open(os.path.join(fld, 'param.json'),'w'))


	def __sample_db(self):
		prices, title = self.db[self.i_db]
		self.i_db += 1
		if self.i_db == self.n_db:
			self.i_db = 0
		return prices, title



