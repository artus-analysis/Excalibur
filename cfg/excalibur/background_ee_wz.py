import configtools
import mc_ee

def config():
	cfg = mc_ee.config()
	cfg["InputFiles"] = configtools.setInputFiles(
		ekppath="/storage/a/dhaitz/skims/2015-07-22_ee-backgrounds_Run2012/kappa_WZ*.root",
		nafpath="/pnfs/desy.de/cms/tier2/store/user/dhaitz/2015-07-22_ee-backgrounds_Run2012/kappa_WZ*.root",
	)
	cfg['TaggedJets'] = 'ak5PFJetsCHS'

	cfg['CrossSection'] = 33.21
	cfg['NumberGeneratedEvents'] = 10000283

	return cfg
