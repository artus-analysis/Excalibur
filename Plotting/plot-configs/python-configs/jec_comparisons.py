#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Excalibur.Plotting.harryinterface as harryinterface
import Excalibur.Plotting.utility.colors as colors

import argparse
import copy


# TODO to more general location
def get_list_slice(lists, arg):
	if arg is False:
		return lists
	else:
		return [[l[arg]] for l in lists]


# TODO to more general location
def get_special_parser(args):
	parser = argparse.ArgumentParser()
	# if these arguments are set true the function will not iterate over the respective quantities
	#	by default, argument ist False -> whole list is taken and iterated over
	#	if set without arguments: first item of list is taken, no iteration
	#	if set with arguments N: N-th item of list is taken, no iteration
	parser.add_argument('--no-quantities', type=int, nargs='?', default=False, const=0)
	parser.add_argument('--no-methods', type=int, nargs='?', default=False, const=0)
	if args is None:
		known_args, args = parser.parse_known_args()
	else:
		known_args, args = parser.parse_known_args(args)
	return known_args, args


def response_comparisons(args2=None, additional_dictionary=None):
	"""Response (MPF/pTbal) vs zpt npv abs(jet1eta), with ratio"""

	known_args, args = get_special_parser(args2)

	plots = []
	# TODO put these default binning values somewhere more globally
	for quantity, bins in zip(*get_list_slice([
		['zpt', 'npv', 'abs(jet1eta)'],
		['zpt', 'npv','abseta']
	], known_args.no_quantities)):
		for method in get_list_slice([['ptbalance', 'mpf']], known_args.no_methods)[0]:
			d = {
				'y_expressions': [method],
				'x_expressions': [quantity],
				'x_bins': bins,
				'y_lims': [0.7, 1.15],
				'x_errors': [1],
				'tree_draw_options': 'prof',
				'markers': ['.', '*'],
				'legend': 'best',
				'cutlabel': True,

				'analysis_modules': ['Ratio'],

				'filename': method + "_" + quantity.replace("(", "").replace(")", ""),
				
				'y_subplot_lims': [0.9, 1.1],
			}
			if quantity == 'abs(jet1eta)':
				d['zjetfolders'] = ["noetacuts"]
				d['y_lims'] = [0.6, 1.1],
			if quantity == 'zpt':
				d['x_log'] = True
				d['x_ticks'] = [30, 50, 70, 100, 200, 400, 1000]
			if additional_dictionary != None:
				d.update(additional_dictionary)
			plots.append(d)
	harryinterface.harry_interface(plots, args)


def basic_comparisons(args=None, additional_dictionary=None, data_quantities=True):
	"""Comparison of: zpt zy zmass zphi jet1pt jet1eta jet1phi npv, both absolute and normalized"""
	
	plots = []
	for quantity in ['zpt', 'zy', 'zmass', 'zphi', 'jet1pt', 'jet1eta', 'jet1phi',
			 'npv', 'metpt', 'metphi', 'rawmetpt', 'rawmetphi',
			 'mu1pt', 'mu1eta', 'mu1phi', 'mu2pt', 'mu2eta', 'mu2phi',
			 'ptbalance', 'mpf', 'jet2pt', 'jet2eta', 'jet2phi',
			 'muminusphi', 'muminuseta', 'muminuspt', 'muplusphi', 'mupluseta', 'mupluspt'] \
			 + (['run', 'lumi', 'event'] if data_quantities else ['npu', 'npumean']):
		# normal comparison
		d = {
			'x_expressions': [quantity],
			'cutlabel': True,
			'analysis_modules': ['Ratio'],
			'y_subplot_lims': [0, 2],
		}
		if quantity in ['jet1pt', 'zpt']:
			d["y_log"] = True
			d["x_bins"] = ["25,0,400"]
		# TODO move this to more general location
		xbins_dict = {
			'npv': ["41,-0.5,40.5"],
			'npu': ["41,-0.5,40.5"],
			'npumean': ["41,-0.5,40.5"],
			'mu1pt': ["25,0,150"],
			'mupluspt': ["25,0,150"],
			'muminuspt': ["25,0,150"],
			'metpt': ["25,0,125"],
			'rawmetpt': ["25,0,125"],
			'ptbalance': ["25,0,2"],
			'mpf': ["25,0,2"],
			'jet2pt': ["25,0,100"],
			'jet2eta': ["20,-5,5"],
			'zpt': ["25,0,600"],
		}
		if quantity in xbins_dict:
			d.update({"x_bins": xbins_dict[quantity]})

		if additional_dictionary != None:
			d.update(additional_dictionary)
		plots.append(d)

		# shape comparison
		d2 = copy.deepcopy(d)
		d2.update({
			'analysis_modules': ['NormalizeToFirstHisto', 'Ratio'],
			'filename': quantity+"_shapeComparison",
			'title': "Shape Comparison",
		})
		if additional_dictionary != None:
			d2.update(additional_dictionary)
		plots.append(d2)

	harryinterface.harry_interface(plots, args)

def basic_profile_comparisons(args=None, additional_dictionary=None):
	""" Plots Z mass as a function of pT """
	plots = []
	for xquantity, yquantity in zip(['zpt'], ['zmass']):
		d = {
			'x_expressions': [xquantity],
			'y_expressions': [yquantity],
			'analysis_modules': ['Ratio'],
			'tree_draw_options': 'prof',
			'cutlabel': True,
			'y_subplot_lims': [0.99, 1.01],
			'x_log': True,
			'y_lims': [90.19, 92.19],
			'x_bins': "30 40 50 60 75 95 125 180 300 1000",
		}
		if additional_dictionary != None:
			d.update(additional_dictionary)
		plots.append(d)

	harryinterface.harry_interface(plots, args)

def pf_comparisons(args=None, additional_dictionary=None):
	"""Absolute contribution of PF fractions vs Z pT."""
	plots = []

	for pf in ['ch', 'm', 'nh', 'p']:
		d = {
			'y_expressions': ["(jet1{0}f*jet1pt)".format(pf)],
			'x_expressions': ['zpt'],
			'x_bins': ['zpt'],
			'x_log': True,
			'cutlabel': True,
			'markers': ['.', 'd'],
			'tree_draw_options':  'prof',
			'x_lims': [30, 1000],
			'analysis_modules': ['Ratio'],
		}
		if additional_dictionary != None:
			d.update(additional_dictionary)
		plots.append(d)
	harryinterface.harry_interface(plots, args)


def pf_fractions(args=None, additional_dictionary=None):
	"""PF fractions and contributions to leading jet vs. ZpT, NPV, jet |eta|"""
	plots = []

	# for 'incoming' labels, add them to the PFfraction-labels
	if additional_dictionary is not None:
		if 'labels' in additional_dictionary:
			labels = additional_dictionary['labels']
			additional_dictionary.pop('labels')
		elif 'nicks' in additional_dictionary:
			labels = additional_dictionary['nicks']
			additional_dictionary.pop('nicks')
		else:
			labels = ['', '']
	else:
		labels = ['', '']
	if labels != ['', '']:
		labels = ["({0})".format(l) for l in labels]

	for absolute_contribution in [False, True]:
		for x_quantity, x_binning in zip(['zpt', 'abs(jet1eta)', 'npv'],
			['zpt', 'abseta', 'npv'],
		):
			d = {
				"labels": [
					"CH {0}".format(labels[0]),
					"CH {0}".format(labels[1]),
					r"$\\gamma$ {0}".format(labels[0]),
					r"$\\gamma$ {0}".format(labels[1]),
					"NH {0}".format(labels[0]),
					"NH {0}".format(labels[1]),
					r"$e$ {0}".format(labels[0]),
					r"$e$ {0}".format(labels[1]),
					r"$\\mu$ {0}".format(labels[0]),
					r"$\\mu$ {0}".format(labels[1]),
				],
				"nicks": [
					"CHad1",
					"CHad2",
					"g1",
					"g2",
					"NHad1",
					"NHad2",
					"e1",
					"e2",
					"m1",
					"m2",
				],
				"colors":[
					'blue',
					colors.histo_colors['blue'],
					'orange',
					colors.histo_colors['yellow'],
					'green',
					colors.histo_colors['green'],
					'brown',
					colors.histo_colors['brown'],
					'purple',
					colors.histo_colors['violet'],
					'blue',
					'orange',
					'green',
					'brown',
					'purple',
				],
				"markers": ["o", "fill"]*5 + ["o"]*5,
				"stacks": ["a", "b"]*5,
				"tree_draw_options": ["prof"],
				"legend_cols": 2,
				"x_expressions": [x_quantity],
				"x_bins": [x_binning],
				"y_expressions": [i for i in ["jet1chf", "jet1pf", "jet1nhf", "jet1ef", "jet1mf"] for _ in (0,1)],
				"y_label": "Leading Jet PF Energy Fraction",
				"y_lims": [0.0, 1.0],
				"analysis_modules": ["Ratio"],
				"ratio_numerator_nicks": [
					"CHad1",
					"g1",
					"NHad1",
					"e1",
					"m1",
				],
				"ratio_denominator_nicks": [
					"CHad2",
					"g2",
					"NHad2",
					"e2",
					"m2",
				],
				'y_subplot_lims' : [0, 2],
				'filename': "PFfractions_{}".format(x_quantity),
				'legend': "None",
			}
			if x_quantity == 'zpt':
				d["x_log"] = True
				d['x_ticks'] = [30, 50, 70, 100, 200, 400, 1000]
			elif x_quantity == 'abs(jet1eta)':
				d["zjetfolders"] = ["noetacuts"]
				d["save_legend"] = "PF_legend"
				# add HF fractions
				d["labels"] += [
					r"HFhad {0}".format(labels[0]),
					r"HFhad {0}".format(labels[1]),
					r"HFem {0}".format(labels[0]),
					r"HFem {0}".format(labels[1])]
				d["ratio_numerator_nicks"] += ["HFhad1", "HFem1"]
				d["ratio_denominator_nicks"] += ["HFhad2", "HFem2"]
				d["y_expressions"] += ["jet1hfhf", "jet1hfhf", "jet1hfemf", "jet1hfemf"]
				d["nicks"] += ["HFhad1","HFhad2", "HFem1", "HFem2"]
				d["colors"] = d["colors"][:10]+['black', 'grey', 'red', '#D35658']+d["colors"][10:]+['grey', 'red']
				d["markers"] = ["o", "fill"]*7 + ["o"]*7,
				d["stacks"] = ["a", "b"]*7,
			if absolute_contribution:
				d["y_expressions"] = ["{0}*jet1pt".format(i) for i in d["y_expressions"]]
				d.pop("y_lims")
				d["filename"] = "PFcontributions_{}".format(x_quantity)
				d["y_label"] = r"Leading Jet PF Energy / GeV"

			if additional_dictionary != None:
				d.update(additional_dictionary)
			plots.append(d)
	harryinterface.harry_interface(plots, args)


def full_comparison(args=None, d=None, data_quantities=True):
	""" Do all comparison plots"""
	response_comparisons(args, d)
	basic_comparisons(args, d, data_quantities)
	basic_profile_comparisons(args, d)
	pf_fractions(args, d)


def comparison_E1E2(args=None):
	""" Do response and basic comparison for E1 and E2 ntuples """
	d = {
		'files': [
			'ntuples/Data_8TeV_53X_E2_50ns_2015-04-21.root',
			'ntuples/Data_8TeV_53X_E1_50ns_2015-04-22.root', 
		],
		"folders": [
				"finalcuts_AK5PFTaggedJetsCHSL1L2L3/ntuple",
				"incut_AK5PFJetsCHSL1L2L3",
		],
		'nicks': [
			'Ex2',
			'Ex1',
		],
		'y_subplot_lims' : [0.95, 1.05],
		'y_subplot_label' : "Ex2/Ex1",
		'y_errors' : [True, True, False],
	}
	response_comparisons(args, additional_dictionary=d)
	basic_comparisons(args, additional_dictionary=d)
	basic_profile_comparisons(args, additional_dictionary=d)


def comparison_5374(args=None):
	d = {
		'files': [
			'ntuples/Data_8TeV_74X_E2_50ns_noHlt_2015-04-23.root',
			'ntuples/Data_8TeV_53X_E2_50ns_noHlt_2015-04-23.root',
		],
		"algorithms": ["AK5PFJetsCHS",],
		"corrections": ["L1L2L3Res",],
		'nicks': [
			'74',
			'53',
		],
		'weights': ['(run==208307||run==208339||run==208341||run==208351||run==208353)'],
		'y_subplot_label' : "74/53",
		'lumi': 0.309
	}
	full_comparison(args, d)


def comparison_datamc(args=None):
	"""full data mc comparisons for work/data.root and work/mc.root"""
	d = {
		'files': ['work/data.root', 'work/mc.root'],
		'labels': ['data', 'mc'],
		'corrections': ['L1L2L3Res', 'L1L2L3'],
	}
	pf_fractions(args, additional_dictionary=d)


def comparison_1215(args=None):
	"""comparison between 2012 (8TeV) and 2015 (13TeV) MC"""
	d = {
		'files': [
			'ntuples/MC_13TeV_72X_E2_25ns_algo_2015-05-21.root',
			'ntuples/MC_RD1_8TeV_53X_E2_50ns_algo_2015-05-21.root',
		],
		'labels': ['13 TeV', '8 TeV'],
		'corrections': ['L1L2L3'],
		'y_subplot_label' : "13/8",
	}
	full_comparison(args, d, data_quantities=False)


def comparison_53742(args=None):
	"""Comparison between 2012 rereco (22Jan) and 2015 742 rereco of 8TeV DoubleMu."""
	d = {
		'files': [
			'ntuples/Data_8TeV_742_E2_50ns_noHlt_2015-05-21.root',
			'ntuples/Data_8TeV_53X_E2_50ns_noHlt_2015-05-20.root',
		],
		'nicks': ['742','53'],
		'weights': ['(run==208307||run==208339||run==208341||run==208351||run==208353)'],
		'y_subplot_label' : "742/53",
		'lumis': [0.309],
	}
	full_comparison(args, d)


def comparison_53742_event_matched(args=None):
	"""Comparison between 2012 rereco (22Jan) and 2015 742 rereco of 8TeV DoubleMu."""
	d = {
		'files': [
			'output.root',
			'output.root',
		],
		'folders': [
			'common2',
			'common1',
		],
		'nicks': ['742','53'],
		'weights': ['(run==208307||run==208339||run==208341||run==208351||run==208353)'],
		'y_subplot_label': "742/53",
		'lumis': [0.309],
		'energies': [8],
		'y_errors': [True, True, False],
		'x_errors': False,
		'ratio_result_nicks': ['742vs53'],
	}
	full_comparison(args, d)


def comparison_740742(args=None):
	"""Comparison between 740 and 2015 742 rereco of 8TeV DoubleMu."""
	d = {
		'files': [
			'ntuples/Data_8TeV_742_E2_50ns_noHlt_2015-05-21.root',
			'ntuples/Data_8TeV_74X_E2_50ns_noHlt_2015-05-20.root',
		],
		'nicks': ['742','740'],
		#'weights': ['(run==208307||run==208339||run==208341||run==208351||run==208353)'],
		'y_subplot_label' : "742/740",
		'lumis': [0.309],
	}
	full_comparison(args, d)


def comparison_740742_event_matched(args=None):
	"""Comparison between event matched 740 and 2015 742 rereco of 8TeV DoubleMu. Takes output.root from eventmatching.py as input."""
	d = {
		'files': [
			'output.root',
			'output.root',
		],
		'folders': [
			'common1',
			'common2',
		],
		'nicks': ['742','740'],
		#'weights': ['(run==208307||run==208339||run==208341||run==208351||run==208353)'],
		'y_subplot_label' : "742/740",
		'lumis': [0.309],
	}
	full_comparison(args, d)


def comparison_53740742(args=None):
	"""Comparison between 53X, 740 and 742 rereco of 8TeV data."""
	d = {
		'files': [
			'output.root',
			'output.root',
			'output.root',
		],
		'folders': [
			'common3',
			'common2',
			'common1',
		],
		'y_errors' : [True, True, True, False, False],
		'markers': ['.', '.', 'fill'],
		'zorder': [30, 20, 10],
		'nicks': ['740', '742', '53'],
		'weights': ['(run==208307||run==208339||run==208341||run==208351||run==208353)'],
		'lumis': [0.309],
		'energies': [8],
		"ratio_numerator_nicks": ['742', '740'],
		"ratio_denominator_nicks": ['53', '53'],
		"x_errors": False,
		"colors": ['black','red', colors.histo_colors['blue'], 'red', 'black'],
		'y_subplot_label' : "74X/53",
	}
	basic_comparisons(args, d, True)
	d['markers'] = ['o', 'o', 'd']
	response_comparisons(args, d)
	basic_profile_comparisons(args, d)


if __name__ == '__main__':
	basic_comparisons()
