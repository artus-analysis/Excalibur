#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Excalibur.Plotting.harryinterface as harryinterface


def flavour_fractions(args=None, additional_dictionary=None):
	""" Plots Flavour fraction (Physics definition) vs zpt, abs(jet1eta)"""
	plots = []

	for x_quantity, x_bins in zip(
			['zpt', 'abs(jet1eta)'],
			["30 40 50 60 75 95 125 180 300 1000", "0 0.783 1.305 1.93 2.5 2.964 3.139 5.191"]):

		d = {
			"filename": "flavorFractions_vs_" + x_quantity,
			"legend": "lower left",
			"labels": ["undef", "g", "b", "c", "uds"],
			"markers": ["fill" ],
			"stacks": ["a", "a", "a", "a", "a"],
			"tree_draw_options": ["prof"],
			"x_expressions": [x_quantity],
			"x_bins": x_bins,
			"y_label": "Flavour fraction (Physics definition)",
			"y_expressions": [
				"(matchedgenparton1flavour==-999)",
				"(abs(matchedgenparton1flavour)==21)",
				"(abs(matchedgenparton1flavour)==5)",
				"(abs(matchedgenparton1flavour)==4)",
				"(abs(matchedgenparton1flavour)>0 && abs(matchedgenparton1flavour)<4)"
			],
			"y_lims": [0.0, 1.0],
		}
		if x_quantity == 'zpt':
			d['x_ticks'] = [50, 100, 500, 1000]
			d['x_log'] = True
		elif x_quantity == 'abs(jet1eta)':
			d["zjetfolders"] = ["noetacuts"]

		d.update(additional_dictionary)
		plots.append(d)

	harryinterface.harry_interface(plots, args)

def flavour_jet1btag_vs_jet1qgtag(args=None, additional_dictionary=None):
	"""Plots Flavour jet1btag vs. jet1qgtag """
	plots = []

	d = {
		"filename": "flavorTaggingZones",
		"legend": "None",
		"x_expressions": "jet1btag",
		"x_bins": "100,0,1",
		"x_lims": [0.0, 1.0],
		"y_expressions": "jet1qgtag",
		"y_bins": "100,0,1",
		"y_lims": [0.0, 1.0],
		"colormap": "Blues",
		"z_log": True,
		"z_lims": [1, 500]
	}
	d.update(additional_dictionary)
	plots.append(d)

	harryinterface.harry_interface(plots, args)

def flavour(args=None):
	"""Plots all flavour plots"""
	d = {
		"files": [
			"ntuples/MC_RD1_8TeV_53X_E2_50ns_2015-05-20.root"
		],
		"algorithms": ["AK5PFJetsCHS",],
		"corrections": ["L1L2L3",]
	}

	flavour_fractions(args, d)
	flavour_jet1btag_vs_jet1qgtag(args, d)