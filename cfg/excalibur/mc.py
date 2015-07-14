import ZJetConfigBase as base


def config():
	cfg = base.getConfig('mc', 2012, 'mm')
	base.changeNamingScheme(cfg)
	cfg['JetMatchingAlgorithm'] = 'algorithmic'
	cfg["InputFiles"] = base.setInputFiles(
		ekppath="/storage/a/dhaitz/skims/2015-05-16_DYJetsToLL_M_50_madgraph_8TeV/*.root",
		nafpath="/pnfs/desy.de/cms/tier2/store/user/dhaitz/2015-05-16_DYJetsToLL_M_50_madgraph_8TeV/*.root",
	)
	cfg = base.expand(cfg, ['nocuts', 'zcuts', 'noalphanoetacuts', 'noalphacuts', 'noetacuts', 'finalcuts'], ['None', 'L1', 'L1L2L3'])

	return cfg
