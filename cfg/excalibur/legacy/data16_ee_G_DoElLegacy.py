import configtools
import os

RUN='G'
CH='ee'
JEC='Summer16_03Feb2017'+RUN+'_V3'

def config():
	cfg = configtools.getConfig('data', 2016, CH, bunchcrossing='25ns')
	cfg["InputFiles"].set_input(
		#ekppath="/storage/jbod/tberger/testfiles/skimming_output/data/ZJet_DoubleElectron_Run2016G-Legacy-07Aug2017-v1_testfile.root",
		ekppathF="srm://cmssrm-kit.gridka.de:8443/srm/managerv2?SFN=/pnfs/gridka.de/cms/disk-only/store/user/tberger/Skimming/ZJet_DoubleElectron_Run2016F-Legacy-07Aug2017-v1/*.root",
		ekppathG="srm://cmssrm-kit.gridka.de:8443/srm/managerv2?SFN=/pnfs/gridka.de/cms/disk-only/store/user/tberger/Skimming/ZJet_DoubleElectron_Run2016G-Legacy-07Aug2017-v1/*.root",
		)
	cfg['JsonFiles'] =  [os.path.join(configtools.getPath(),'data/json/Cert_'+RUN+'_13TeV_23Sep2016ReReco_Collisions16_JSON.txt')]
	cfg['Jec'] = os.path.join(configtools.getPath(),'../JECDatabase/textFiles/'+JEC+'_DATA/'+JEC+'_DATA')
	cfg['VertexSummary'] = 'offlinePrimaryVerticesSummary'
	cfg = configtools.expand(cfg, ['nocuts','noalphanoetacuts','noetaphicleaning','basiccuts','finalcuts'], ['None', 'L1', 'L1L2L3', 'L1L2Res', 'L1L2L3Res'])
	configtools.remove_quantities(cfg, ['jet1qgtag'])
	return cfg
