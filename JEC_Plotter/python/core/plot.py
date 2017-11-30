import Excalibur.Plotting.harryinterface as harryinterface

from copy import deepcopy

from Excalibur.JEC_Plotter.core.quantities import QUANTITIES

CHANNEL_SPEC = {
    'Zmm' : {
        'label': r"$\\mathrm{\\bf{Z \\rightarrow} \\mu \\mu}$"
    },
    'Zee' : {
        'label': r"$\\mathrm{\\bf{Z \\rightarrow} e e}$"
    }
}


class _Plot1D(object):
    _INFOBOX_TOPLEFT_XY = (0.05, 0.97)
    _INFOBOX_SPACING_Y = 0.05

    def __init__(self, basename, quantity, selection,
                 samples, cut_sets, correction_string,
                 normalize_to_first_histo=False,
                 show_ratio_to_first=False,
                 show_cut_info_text=True):
        self._nsamples = len(samples)

        self._basename = basename
        self._q = quantity
        self._samples = samples
        self._selection = selection
        self._cut_sets = cut_sets or [None]
        self._correction_string = correction_string
        self._normalize_to_first_histo = normalize_to_first_histo
        self._ratio = show_ratio_to_first

        _ncutsets = len(cut_sets)

        if _ncutsets == 1:
            cut_sets = [cut_sets[0]] * self._nsamples

        assert len(cut_sets) == self._nsamples

        self._basic_weights_string = self._selection.weights_string

        self._channel = self._samples[0]['channel']
        assert all([_sample['channel'] == self._channel for _sample in self._samples])

        _bin_spec = self._q.get_bin_spec_as_string()
        _output_folder = "_".join([self._basename,
                                   self._channel,
                                   self._correction_string,
                                   self._selection.name])
        _output_filename = '{0}'.format(self._q.name)
        self._basic_dict = {
            # data
            'zjetfolders': [self._selection.zjet_folder],
            #'weights': [self._basic_weights_string],
            'weights': [],

            # binning
            'x_expressions': [self._q.expression],
            'x_bins': _bin_spec,
            'x_label': self._q.label,

            # formatting
            'line_styles': '-',
            'x_lims': map(float, self._q.bin_spec[1:]) if _bin_spec is not None else None,
            'title': None,
            'y_log': self._q.log_scale,

            # web gallery options
            'www': _output_folder,
            'filename': _output_filename,

            # texts
            "texts": [
                CHANNEL_SPEC.get(self._channel, {}).get('label', ""),
                r"$\\bf{{{0}}}$".format(self._correction_string)
            ],
            "texts_size": [
                20,
                25,
            ],
            "texts_x": [
                0.1, #self._INFOBOX_TOPLEFT_XY[0],
                0.68,
            ],
            "texts_y": [
                1.08, #self._INFOBOX_TOPLEFT_XY[1],
                0.09,
            ],

            'analysis_modules': [],

            # -- filled in per sample/cut group
            'nicks': [],
            'files': [],
            'labels': [],
            'corrections': [],
            'colors': [],
            'markers': [],
            'step': [],
            'y_errors': []
        }

        if show_cut_info_text:
            # add cut labels as text
            for _i, _cl in enumerate(self._selection.texts):
                self._basic_dict['texts'].append(_cl)
                self._basic_dict['texts_size'].append(15)
                self._basic_dict['texts_x'].append(self._INFOBOX_TOPLEFT_XY[0])
                self._basic_dict['texts_y'].append(self._INFOBOX_TOPLEFT_XY[1] - 0.07 - (_i + 1) * self._INFOBOX_SPACING_Y)

    def get_dict(self):
        _d = deepcopy(self._basic_dict)

        for _i, (_sample, _cutset) in enumerate(zip(self._samples, self._cut_sets)):
            _d['nicks'].append("nick{}".format(_i))
            _d['files'].append(_sample['file'])
            _d['labels'].append("{source_type} ({source_label})".format(**_sample._dict))
            _d['corrections'].append(self._correction_string)
            _d['colors'].append(_sample['color'])
            _d['markers'].append(_sample._dict.get('marker', '_'))
            _d['step'].append(_sample._dict.get('step_flag', False))
            if _cutset is not None:
                _d['weights'].append(self._basic_weights_string + '&&' + _cutset.weights_string)
            else:
                _d['weights'].append(self._basic_weights_string)
            _d['y_errors'].append(True)

            # default to 'L1L2L3' for Monte Carlo
            if self._correction_string == 'L1L2L3Res' and _sample['source_type'] != 'Data':
                _d['corrections'][-1] = 'L1L2L3'

        if self._ratio:
            _d['analysis_modules'].append("Ratio")
            _num_nicks = ["nick{}".format(i) for i in range(self._nsamples)]
            _res_nicks = ["nick{}_over0".format(i) for i in range(self._nsamples)]
            _d.update({
                "ratio_numerator_nicks": _num_nicks,
                "ratio_denominator_nicks": ["nick0"],
                "ratio_result_nicks": _res_nicks,
                "ratio_denominator_no_errors": False,
                "subplot_fraction": 25,
                #"subplot_lines": [],
                "subplot_nicks": _res_nicks,  #["dummy"],  # HARRYPLOTTER!!
                "y_subplot_label": "Ratio",
                'y_subplot_lims': [0.85, 1.05],
                'y_errors': _d['y_errors']+[False]*len(_num_nicks),
            })

        if self._normalize_to_first_histo and len(_d['files']) > 1:
            _d['analysis_modules'].append("NormalizeToFirstHisto")

        return _d


class _Plot2D(_Plot1D):
    _INFOBOX_TOPLEFT_XY = (0.05, 0.97)
    _INFOBOX_SPACING_Y = 0.05
    def __init__(self, basename, quantity_pair, selection,
                 samples, cut_sets, correction_string,
                 normalize_to_first_histo=False,
                 show_ratio_to_first=False,
                 show_cut_info_text=True,
                 show_as_profile=False):

        super(_Plot2D, self).__init__(
            basename=basename, quantity=quantity_pair[0], selection=selection,
            samples=samples, cut_sets=cut_sets, correction_string=correction_string,
            normalize_to_first_histo=False, show_ratio_to_first=False
        )
        del self._q
        self._qx, self._qy = quantity_pair

        _bin_spec_x = self._qx.get_bin_spec_as_string()
        _bin_spec_y = self._qy.get_bin_spec_as_string()

        _output_folder = "_".join([self._basename,
                                   self._channel,
                                   self._correction_string,
                                   self._selection.name])
        _output_filename = '{0}_vs_{1}'.format(self._qy.name, self._qx.name)
        self._basic_dict = {
            # data
            'zjetfolders': [self._selection.zjet_folder],
            #'weights': [self._basic_weights_string],
            'weights': [],

            # binning
            'x_expressions': [self._qx.expression],
            'x_bins': _bin_spec_x,
            'x_label': self._qx.label,
            'y_expressions': [self._qy.expression],
            'y_bins': _bin_spec_y,
            'y_label': self._qy.label,

            # formatting
            'title': None,
            'line_styles': '-',
            'x_lims': map(float, self._qx.bin_spec[1:]) if _bin_spec_x is not None else None,
            'x_log': self._qx.log_scale,
            'y_lims': map(float, self._qy.bin_spec[1:]) if _bin_spec_y is not None else None,
            'y_log': self._qy.log_scale,


            # texts
            "texts": [
                CHANNEL_SPEC.get(self._channel, {}).get('label', ""),
                r"$\\bf{{{0}}}$".format(self._correction_string)
            ],
            "texts_size": [
                20,
                25,
            ],
            "texts_x": [
                0.1, #self._INFOBOX_TOPLEFT_XY[0],
                0.68,
            ],
            "texts_y": [
                1.08,  # self._INFOBOX_TOPLEFT_XY[1],
                0.09,
            ],
            # web gallery options
            'www': _output_folder,
            'filename': _output_filename,

            'analysis_modules': [],

            # -- filled in per sample/cut group
            'nicks': [],
            'files': [],
            'labels': [],
            'corrections': [],
            'colors': [],
            'markers': [],
            'step': [],
            'y_errors': []
        }

        self._profile = show_as_profile
        if show_as_profile:
            self._basic_dict['tree_draw_options'] = 'prof'

        if show_cut_info_text:
            # add cut labels as text
            for _i, _cl in enumerate(self._selection.texts):
                self._basic_dict['texts'].append(_cl)
                self._basic_dict['texts_size'].append(15)
                self._basic_dict['texts_x'].append(self._INFOBOX_TOPLEFT_XY[0])
                self._basic_dict['texts_y'].append(self._INFOBOX_TOPLEFT_XY[1] - 0.07 - (_i + 1) * self._INFOBOX_SPACING_Y)

    def get_dict(self):
        _d = super(_Plot2D, self).get_dict()
        # override markers for profile
        if self._profile:
            #_d['markers'] = ['.']
            _d['line_styles'] = ""
        return _d


class PlotHistograms1D(object):

    def __init__(self, samples, quantities, selection_cuts,
                 additional_cuts=None,
                 basename='hist_1d', corrections='L1L2L3Res',
                 normalize_to_first=False,
                 show_ratio_to_first=False,
                 show_cut_info_text=True):
        self._plots = []
        self._basename = basename

        for _qn in quantities:

            _q = QUANTITIES.get(_qn, None)
            if _q is None:
                print "UNKONWN quantity '%s': skipping..." % (_qn,)
                continue

            for _selection_cut in selection_cuts:

                _plot = _Plot1D(basename=self._basename,
                        quantity=_q,
                        selection=_selection_cut,
                        samples=samples,
                        cut_sets=additional_cuts,
                        correction_string=corrections,
                        normalize_to_first_histo=normalize_to_first,
                        show_ratio_to_first=show_ratio_to_first,
                        show_cut_info_text=show_cut_info_text)

                self._plots.append(_plot)

    def make_plots(self, args=None):
        _plot_dicts = [_p.get_dict() for _p in self._plots]
        harryinterface.harry_interface(_plot_dicts, args)

class PlotHistograms2D(PlotHistograms1D):

    def __init__(self, samples, quantity_pairs, selection_cuts,
                 additional_cuts=None,
                 basename='hist_2d', corrections='L1L2L3Res',
                 show_cut_info_text=True,
                 show_as_profile=False):

        self._plots = []
        self._basename = basename

        for _qxn, _qyn in quantity_pairs:

            _qx = QUANTITIES.get(_qxn, None)
            if _qx is None:
                print "UNKONWN 'x' quantity '%s': skipping..." % (_qxn,)
                continue

            _qy = QUANTITIES.get(_qyn, None)
            if _qy is None:
                print "UNKONWN 'y' quantity '%s': skipping..." % (_qyn,)
                continue

            for _selection_cut in selection_cuts:

                _plot = _Plot2D(basename=self._basename,
                        quantity_pair=(_qx, _qy),
                        selection=_selection_cut,
                        samples=samples,
                        cut_sets=additional_cuts,
                        correction_string=corrections,
                        normalize_to_first_histo=False,
                        show_ratio_to_first=False,
                        show_cut_info_text=show_cut_info_text,
                        show_as_profile=show_as_profile)

                self._plots.append(_plot)


# class PlotHistograms1DCompareCuts:
#     _INFOBOX_TOPLEFT_XY = (0.05, 0.46)
#     _INFOBOX_SPACING_Y = 0.05
#
#     def __init__(self, basename, quantities, sample, subplot_cuts,
#                  sample_variant="eventBased",
#                  selection_cuts=[SELECTIONS['finalcuts']], corrections='L1L2L3'):
#         self._plots = []
#         self._basename = basename
#         _corrections = corrections
#
#         for _q in quantities:
#             _labels = []
#             _subplot_additional_weights = []
#             _colors = []
#             _markers = []
#             _step_flags = []
#             _stacks = []
#             if _q not in QUANTITIES:
#                 print "UNKONWN quantity '%s': skipping..." % (_q,)
#                 continue
#             _qd = QUANTITIES[_q]
#
#             try:
#                 sample_dict = Sample(sample, variant=sample_variant)._dict
#             except IOError as e:
#                 print "Error reading file for sample '%s': skipping..." % (_sample,)
#                 continue
#
#             # don't plot quantities for channels for which they are not available
#             if "channels" in _qd and sample_dict['channel'] not in _qd["channels"]:
#                 print "Quantity '{}' unavailable for channel '{}': skipping...".format(_q, sample_dict['channel'])
#                 continue
#
#             # don't plot quantities for source types for which they are not available
#             if "source_types" in _qd and sample_dict['source_type'] not in _qd["source_types"]:
#                 print "Quantity '{}' unavailable for source type '{}': skipping...".format(_q,
#                                                                                            sample_dict['source_type'])
#                 continue
#
#             # sample_dict = SAMPLE_SPEC[_sample]
#             for _scut in subplot_cuts:
#                 if _scut not in GENMATCHING_CUT_SPEC:
#                     print "UNKONWN subplot cut '%s': skipping..." % (_scut,)
#                     continue
#                 scut_dict = GENMATCHING_CUT_SPEC[_scut]
#
#                 _labels.append("{0} ({label})".format(sample_dict['source_type'], **scut_dict))
#                 _subplot_additional_weights.append("&&".join(scut_dict['cuts']))
#                 _colors.append(scut_dict.get('color', None))
#                 _markers.append(scut_dict.get('marker', '_'))
#                 _step_flags.append(scut_dict.get('step_flag', False))
#                 _stacks.append(scut_dict.get('stack', None))
#
#             if all([c is None for c in _colors]):
#                 _colors = None
#             print _colors
#
#             for _sel_cutset in selection_cuts:
#                 selection_dict = _sel_cutset.plot_dict
#                 _output_folder = "_".join([self._basename,
#                                            sample_dict['channel'],
#                                            _corrections, sample_variant,
#                                            _sel_cutset.name])
#                 _output_filename = '{0}'.format(_q)
#
#                 _d = {
#                     # get data
#                     'files': sample_dict['file'],
#                     'zjetfolders': selection_dict['zjetfolders'],
#                     'corrections': [_corrections],
#                     'weights': [_sel_cutset.weights_string + "&&" + _sw for _sw in _subplot_additional_weights],
#
#                     # binning
#                     'x_expressions': [_qd.get("expression", _q)],
#                     'x_bins': ",".join(_qd.get("bins")) if "bins" in _qd else None,
#                     'x_label': _qd.get("label", None),
#
#                     # formatting
#                     "canvas_width": 600,
#                     "canvas_height": 480,
#                     "markers": _markers,
#                     'step': _step_flags,
#                     'line_styles': '-',
#                     'colors': _colors,
#                     'x_lims': map(float, _qd['bins'][1:]) if "bins" in _qd else None,
#                     'filename': _output_filename,
#                     'title': None,
#                     'labels': _labels,
#                     'y_log': _qd.get('log_scale', False),
#                     "stacks": _stacks,
#
#                     # texts
#                     "texts": [
#                         CHANNEL_SPEC.get(sample_dict['channel'], {}).get('label', ""),
#                         r"$\\bf{{{0}}}$".format(_corrections)
#                     ],
#                     "texts_size": [
#                         20,
#                         25,
#                     ],
#                     "texts_x": [
#                         self._INFOBOX_TOPLEFT_XY[0],
#                         0.68,
#                     ],
#                     "texts_y": [
#                         self._INFOBOX_TOPLEFT_XY[1],
#                         0.09,
#                     ],
#
#                     # web gallery options
#                     'www': _output_folder,
#                 }
#
#                 # add variant label as text
#                 _d['texts'].append(sample_dict['variant_label'])
#                 _d['texts_size'].append(15)
#                 _d['texts_x'].append(self._INFOBOX_TOPLEFT_XY[0])
#                 _d['texts_y'].append(self._INFOBOX_TOPLEFT_XY[1] - 0.07)
#
#                 # add cut labels as text
#                 for _i, _cl in enumerate(selection_dict['texts']):
#                     _d['texts'].append(_cl)
#                     _d['texts_size'].append(15)
#                     _d['texts_x'].append(self._INFOBOX_TOPLEFT_XY[0])
#                     _d['texts_y'].append(self._INFOBOX_TOPLEFT_XY[1] - 0.07 - (_i + 1) * self._INFOBOX_SPACING_Y)
#
#                 if DEBUG_MODE:
#                     _d['log_level'] = 'debug'
#
#                 self._plots.append(_d)
#
#     def make_plots(self, args=None):
#         harryinterface.harry_interface(self._plots, args)
#
#
# class PlotHistograms1DCompareCutsRatio(PlotHistograms1DCompareCuts):
#     def __init__(self, basename, quantities, sample, numerator_cuts, denominator_cut,
#                  sample_variant="eventBased",
#                  selection_cuts=[SELECTIONS['finalcuts']], corrections='L1L2L3',
#                  title=None, y_label=None):
#         self._plots = []
#         self._basename = basename
#         _corrections = corrections
#         self._force_z_log = False
#
#         # subplot_cuts = [numerator_cuts, denominator_cuts]
#         z_log = False
#
#         for _qx in quantities:
#             _labels = []
#             _subplot_additional_weights = []
#             _colors = []
#             _markers = []
#             _step_flags = []
#             _nicks = []
#             _num_nicks = []
#             _ratio_result_nicks = []
#             _colormap = None
#             if _qx not in QUANTITIES:
#                 print "UNKONWN 'x' quantity '%s': skipping..." % (_qx,)
#                 continue
#             _qxd = QUANTITIES[_qx]
#
#             try:
#                 sample_dict = Sample(sample, variant=sample_variant)._dict
#             except IOError as e:
#                 print "Error reading file for sample '%s': skipping..." % (_sample,)
#                 continue
#
#             # don't plot quantities for channels for which they are not available
#             if ("channels" in _qxd and sample_dict['channel'] not in _qxd["channels"]):
#                 print "Quantity '{}' unavailable for channel '{}': skipping...".format(_qx, sample_dict['channel'])
#                 continue
#
#             # don't plot quantities for source types for which they are not available
#             if "source_types" in _qxd and sample_dict['source_type'] not in _qxd["source_types"]:
#                 print "Quantity '{}' unavailable for source type '{}': skipping...".format(_qx,
#                                                                                            sample_dict['source_type'])
#                 continue
#
#             # add denom nick
#             if denominator_cut not in GENMATCHING_CUT_SPEC:
#                 print "UNKONWN subplot cut '%s': skipping..." % (denominator_cut,)
#                 continue
#             denom_scut_dict = GENMATCHING_CUT_SPEC[denominator_cut]
#             _nicks.append("nick_denom")
#             _subplot_additional_weights.append("&&".join(denom_scut_dict['cuts']))
#
#             # sample_dict = SAMPLE_SPEC[_sample]
#             for _i, _scut in enumerate(numerator_cuts):
#                 if _scut not in GENMATCHING_CUT_SPEC:
#                     print "UNKONWN subplot cut '%s': skipping..." % (_scut,)
#                     continue
#                 scut_dict = GENMATCHING_CUT_SPEC[_scut]
#
#                 _nicks.append("nick{}_num".format(_i))
#                 _ratio_result_nicks.append("ratio{}".format(_i))
#                 _num_nicks.append("nick{}_num".format(_i))
#                 _subplot_additional_weights.append("&&".join(scut_dict['cuts']))
#
#                 _labels.append("{0} ({label})".format(sample_dict['source_type'], **scut_dict))
#                 _colors.append(scut_dict.get('color', None))
#                 _markers.append(scut_dict.get('marker', '_'))
#                 _step_flags.append(scut_dict.get('step_flag', False))
#                 if _colormap is None:
#                     _colormap = scut_dict.get('colormap', _colormap)
#
#             if all([c is None for c in _colors]):
#                 _colors = None
#
#             for _sel_cutset in selection_cuts:
#                 selection_dict = _sel_cutset.plot_dict
#                 _output_folder = "_".join([self._basename,
#                                            sample_dict['channel'],
#                                            _corrections, sample_variant,
#                                            _sel_cutset.name])
#                 _output_filename = '{0}'.format(_qx)
#                 if self._force_z_log:
#                     _output_filename += '_log'
#
#                 _d = {
#                     # get data
#                     'files': sample_dict['file'],
#                     'zjetfolders': selection_dict['zjetfolders'],
#                     'corrections': [_corrections],
#                     'weights': [_sel_cutset.weights_string + "&&" + _sw for _sw in _subplot_additional_weights],
#
#                     # binning
#                     'x_expressions': [_qxd.get("expression", _qx)],
#                     'x_bins': ",".join(_qxd.get("bins")) if "bins" in _qxd else None,
#                     'x_label': _qxd.get("label", None),
#
#                     # formatting
#                     "canvas_width": 640,
#                     "canvas_height": 480,
#                     "markers": _markers,
#                     'step': _step_flags,
#                     'line_styles': '-',
#                     'x_lims': map(float, _qxd['bins'][1:]) if "bins" in _qxd else None,
#                     'y_tick_labels': None,  # suppress tick marks in main plot
#                     'colors': _colors if _colormap is None else None,
#                     'colormap': _colormap if _colormap is not None else "afmhot",
#                     # 'alpha': 0.3,
#                     'filename': _output_filename,
#                     'title': title or "",
#                     'labels': _labels,
#                     'stacks': [
#                         "fractions"
#                     ],
#                     # 'z_log': self._force_z_log or _qyd.get('log_scale', False) or _qxd.get('log_scale', False),
#                     'nicks': _nicks,
#                     'nicks_blacklist': _num_nicks + ["nick_denom"],
#                     'nicks_whitelist': ["ratio"],
#
#                     # ratio
#                     "analysis_modules": ["Ratio"],
#                     "ratio_numerator_nicks": _num_nicks,
#                     "ratio_denominator_nicks": ["nick_denom"],
#                     "ratio_result_nicks": _ratio_result_nicks,
#                     "ratio_denominator_no_errors": "false",
#                     "subplot_fraction": 0,
#                     "subplot_lines": [],
#                     "subplot_nicks": ["dummy"],  # HARRYPLOTTER!!
#                     "y_subplot_label": "",
#                     "y_subplot_label": y_label or "Ratio",
#                     "y_label": y_label or "Ratio",
#                     'y_subplot_lims': [0., 1.],
#                     'y_lims': [0., 1.25],
#                     'y_errors': False,
#
#                     # texts
#                     "texts": [
#                         # CHANNEL_SPEC.get(sample_dict['channel'], {}).get('label', ""),
#                         r"$\\bf{{{0}}}$".format(_corrections)
#                     ],
#                     "texts_size": [
#                         # 20,
#                         25,
#                     ],
#                     "texts_x": [
#                         # self._INFOBOX_TOPLEFT_XY[0],
#                         0.68,
#                     ],
#                     "texts_y": [
#                         # self._INFOBOX_TOPLEFT_XY[1],
#                         0.09,
#                     ],
#
#                     # web gallery options
#                     'www': _output_folder,
#                 }
#
#                 # add variant label as text
#                 _d['texts'].append(sample_dict['variant_label'])
#                 _d['texts_size'].append(15)
#                 _d['texts_x'].append(self._INFOBOX_TOPLEFT_XY[0])
#                 _d['texts_y'].append(self._INFOBOX_TOPLEFT_XY[1] - 0.07)
#
#                 # add variant label as text
#                 _d['texts'].append(CHANNEL_SPEC.get(sample_dict['channel'], {}).get('label', ""))
#                 _d['texts_size'].append(20)
#                 _d['texts_x'].append(self._INFOBOX_TOPLEFT_XY[0])
#                 _d['texts_y'].append(1.07)
#
#                 # add cut labels as text
#                 for _i, _cl in enumerate(selection_dict['texts']):
#                     _d['texts'].append(_cl)
#                     _d['texts_size'].append(15)
#                     _d['texts_x'].append(self._INFOBOX_TOPLEFT_XY[0])
#                     _d['texts_y'].append(self._INFOBOX_TOPLEFT_XY[1] - 0.07 - (_i + 1) * self._INFOBOX_SPACING_Y)
#
#                 if DEBUG_MODE:
#                     _d['log_level'] = 'debug'
#
#                 with open("dump.json", 'w') as f:
#                     json.dump(_d, f, indent=4)
#                 self._plots.append(_d)
#
#     def make_plots(self, args=None):
#         harryinterface.harry_interface(self._plots, args)
#
#
# if __name__ == "__main__":
#     _qs = [
#         # 'jet1pt_extended_log',  'jet2pt_extended_log',  'jet3pt_extended_log',
#         # 'jet1pt',  'jet2pt',  'jet3pt',
#         # 'jet1eta', 'jet2eta', 'jet3eta',
#         # 'jet1eta_extended', 'jet2eta_extended', 'jet3eta_extended',
#         # 'metphi', 'met',
#         # 'alpha', 'ptbalance', 'mpf',
#         # 'jet1pt', 'jet2pt', 'jet3pt',
#         # 'zpt',
#         # 'jet1eta', 'jet2eta', 'jet3eta',
#         # 'zeta',
#         'jet1phi', 'jet2phi', 'jet3phi',
#     ]
#     _samples = [
#         'data16_mm_BCD_DoMuLegacy.root',
#         # 'data16_mm_BCD_DoMuLegacy_etaphiclean.root',
#         # 'mc16_mm_BCDEFGH_DYJets_Madgraph.root',
#     ]
#     _selections = [
#         SELECTIONS['finalcuts'],
#         SELECTIONS['finalcuts'] + CUT_GROUPS['user']['adhocEtaPhiBCD'],
#     ]
#
#     ph_legacy = PlotHistograms1D(quantities=_qs,
#                                  samples=_samples,
#                                  selection_cuts=_selections,
#                                  normalized=False,
#                                  sample_variant="Summer16_07Aug2017_V1")
#     ph_legacy.make_plots()
#
#     exit(43)
#
#     # ph_legacy_compareEtaPhiCuts = PlotHistograms1D(
#     #    quantities=_qs,
#     #    samples=_samples,
#     #    cuts=_selections,
#     #    normalized=False,
#     #    sample_variant="Summer16_07Aug2017_V1"
#     # )
#     # ph_legacy_compareEtaPhiCuts.make_plots()
#
#     # ph_remini = PlotHistograms1D(quantities=_qs,
#     #                             samples=_samples,
#     #                             cuts=_selections,
#     #                             normalized=False,
#     #                             sample_variant="Summer16_03Feb2017BCD_V3")
#     # ph_remini.make_plots()
#
#     _qs = ['jet2phi']
#     _sample = 'data16_mm_BCD_DoMuLegacy.root'
#     _subplot_cut_formats = [
#         'genMatch_deltaR{dr}_pT{dptpt}_bar',
#         'genMatch_DeltaR{dr}_nopT{dptpt}_bar',
#         'genMatch_noDeltaR{dr}_bar',
#     ]
#
#     _txt_dr = "{:02d}".format(int(10 * 0.3))
#     _txt_dptpt = "{:02d}".format(int(10 * 0.3))
#     _subplot_cuts = [_fmt.format(dr=_txt_dr, dptpt=_txt_dptpt) for _fmt
#                      in _subplot_cut_formats]
#
#     ph_legacy_compareEtaPhiCuts = PlotHistograms1DCompareCuts(
#         basename="compareEtaPhi_1D",
#         quantities=_qs,
#         sample=_sample,
#         sample_variant="eventBased",
#         subplot_cuts=_subplot_cuts,
#         selection_cuts=_selections
#     )
#     ph_legacy_compareEtaPhiCuts.make_plots()

