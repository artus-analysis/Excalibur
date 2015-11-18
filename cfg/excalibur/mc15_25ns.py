import configtools


def config():
	cfg = configtools.getConfig('mc', 2015, 'mm', bunchcrossing='25ns')
	cfg["InputFiles"].set_input(
		ekppath="/storage/a/mfischer/skims/zjet/2015-10-30/Zmm_DYJetsToLL_M_50_aMCatNLO_Asympt25ns_13TeV/*.root",
		nafpath="/pnfs/desy.de/cms/tier2/store/user/mafische/skims/MF_Zll_run2/2015-10-30/Zmm_DYJetsToLL_M_50_aMCatNLO_Asympt25ns_13TeV/*.root",
	)
	cfg = configtools.expand(cfg, ['nocuts', 'zcuts', 'noalphanoetacuts', 'noalphacuts', 'noetacuts', 'finalcuts', 'betacuts'], ['None', 'L1', 'L1L2L3'])
	configtools.remove_quantities(cfg, ['jet1btag', 'jet1qgtag', 'jet1rc'])
	cfg['NumberGeneratedEvents'] = 299269
	cfg['CrossSection'] = 6025.2  # https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat13TeV
	return cfg
