"""

A helper module for plotting various parameters derived by SED fitting module CIGALE (cigale.lam.fr)

Author: A.J. Uppal (c) 2022

"""

import matplotlib.pyplot as plt
import pandas as pd

from random import sample
from sys import argv

SALPETER_DIR = argv[1] if len(argv) > 1 else "./out"
CHABRIER_DIR = argv[2] if len(argv) > 2 else "./20220404_235156_out"

class CPlotter:
	"""
		Contains comparison plotting methods for Chabrier, Salpeter IMFs. Assumes identical parameters EXCEPT imf=0,1
	"""
	def __init__(self, sdir=SALPETER_DIR, cdir=CHABRIER_DIR):
		"""
			initialize the CPlotter() instance
			params:
				sdir [directory -> salpeter] e.g. "./out" note the leading "/" and no trailing "/"
				cdir [director -> chabrier)
		"""
		self.df_c = pd.read_table(open(cdir+"/results.txt"), delim_whitespace=True)
		self.df_s = pd.read_table(open(sdir+"/results.txt"), delim_whitespace=True)
		self.param_set = set(self.df_c.columns).intersection(set(self.df_s.columns))
	def list_params(self):
		"""
		Lists all the available parameters
		"""
		print("\n".join(list(self.param_set)))

	def scatter(self, param1, param2, src=["s", "c"], axis=None):
		"""
		2 dimensional scatter plot of 2 parameters
		params:
			param1: 1st parameter
			param2: 2nd parameter
			src: either "s" (salpeter), "c" (chabrier), or both (default)
		"""
		if not len(src):
			return 'Must declare at least one member of src = ["s", "c"]'
		if not all(param in self.param_set for param in [param1, param2]):
			return "Invalid param(s)"
		ax = axis or plt.axes()
		if len(src) == 1:
			df = {'s': self.df_s, 'c': self.df_c}[src[0]]
			plt.title({"s": "Salpeter", "c": "Chabrier"}[src[0]])
			ax.scatter(df[param1], df[param2])
		else:
			for df, label in zip([self.df_s, self.df_c], ["Salpeter", "Chabrier"]):
				ax.scatter(df[param1], df[param2], label=label)
			plt.legend()
		ax.set_xlabel(" ".join(word.capitalize() for word in param1.split('.')))
		ax.set_ylabel(" ".join(word.capitalize() for word in param2.split('.')))
		if not axis:
			plt.show(block=True)

	def scatter3D(self, param1, param2, param3, src=["s", "c"], axis=None):
		"""
		3 dimensional scatter plot of 3 parameters
		params:
			param1: 1st parameter
			param2: 2nd parameter
			param3: 3rd parameter
			src: either "s" (salpeter), "c" (chabrier), or both (default)
		"""
		if not len(src):
			return 'Must declare at least one member of src = ["s", "c"]'
		if not all(param in self.param_set for param in [param1, param2, param3]):
			return "Invalid param(s)"
		ax = axis or plt.axes(projection='3d')
		if len(src) == 1:
			df = {'s': self.df_s, 'c': self.df_c}[src[0]]
			plt.title({"s": "Salpeter", "c": "Chabrier"}[src[0]])
			ax.scatter3D(df[param1], df[param2], df[param3])
		else:
			for df, label in zip([self.df_s, self.df_c], ["Salpeter", "Chabrier"]):
				ax.scatter3D(df[param1], df[param2], df[param3], label=label)
			plt.legend()
		ax.set_xlabel(" ".join(word.capitalize() for word in param1.split('.')))
		ax.set_ylabel(" ".join(word.capitalize() for word in param2.split('.')))
		ax.set_zlabel(" ".join(word.capitalize() for word in param3.split('.')))
		if not axis:
			plt.show(block=True)

	def randomScatter(self, src=["s", "c"], w=3):
		if w not in range(1, 6):
			return "w must be integer in range 1..5"
		params = sample(self.param_set - {'best.universe.redshift'}, w**2)
		for i, p in zip(range(1, w**2+1), params):
			ax = plt.subplot(w, w, i)
			self.scatter('best.universe.redshift', p, src, ax)
		plt.tight_layout()
		plt.show(block=True)

if __name__ == "__main__":
	cp = CPlotter()
	cp.randomScatter(w=3)
	cp.scatter3D('best.universe.redshift', 'best.stellar.m_star_old', 'best.stellar.m_star_young')
