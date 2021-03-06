import configtools

###
# base config
###

def getBaseConfig(tagged=True, **kwargs):
	cfg = {
		# Artus General Settings
		'ProcessNEvents': -1,
		'FirsEvent': 0,
		'Processors': [],
		'InputFiles': [],  # Overwritten by (data/mc).py, excalibur.py, json_modifier.py (if run in batch mode)
		'OutputPath': 'out', # Overwritten by excalibur.py
		# ZJetCorrectionsProducer Settings
		'Jec': '', # Path for JEC data, please set this later depending on input type
		'L1Correction': 'L1FastJet',
		'RC': True,  # Also provide random cone offset JEC, and use for type-I
		'FlavourCorrections': False,  # Calculate additional MC flavour corrections
		# ZProducer Settings
		'ZMassRange': 10.,	
		'GenZMassRange': 10.,
		#'VetoMultipleZs' : False,
		# TypeIMETProducer Settings
		'Met' : 'met', # metCHS will be selected automaticly if CHS jets are requested in TaggedJets
		'TypeIJetPtMin': 10.,
		'EnableMetPhiCorrection': False,
		'MetPhiCorrectionParameters': [], # Please set this later depending on input type
		# Valid Jet Selection
		'JetID' : 'loose',
		#'PuJetIDs' : ['2:puJetIDFullTight'],
		'JetMetadata' : 'jetMetadata',
		'TaggedJets' : 'ak4PFJetsCHS',
		# PU
		'PileupDensity' : 'pileupDensity',

		# Pipelines
		'Pipelines': {
			'default': {
				'CorrectionLevel': '', # Overwritten by expand function, set levels in data.py or mc.py
				                       # No correction at all equals 'None', not ''
				'Consumers': [
					'ZJetTreeConsumer',
					'cutflow_histogram',
				],
				'EventWeight': 'eventWeight',
				'Processors': [], # Overwritten/cleaned by expand function, set cuts in data.py or mc.py
				'Quantities': [
					# General quantities
					'npv', 'rho', 'weight', #'nputruth',
					'njets', 'njetsinv', 'njets30', # number of valid and invalid jets
					# Z quantities
					'zpt', 'zeta', 'zeta', 'zy', 'zphi', 'zmass', 'phistareta', 'zl1pt', 'zl2pt', 'zl1eta', 'zl2eta', 'zl1phi', 'zl2phi',
					# Leading jet
					'jet1pt', 'jet1eta', 'jet1y', 'jet1phi',
					'jet1chf', 'jet1nhf', 'jet1ef',
					'jet1mf', 'jet1hfhf', 'jet1hfemf', 'jet1pf',
					'jet1area',
					'jet1l1', 'jet1rc', 'jet1l2',
					'jet1ptraw', 'jet1ptl1', 
					#'jet1unc',  # Leading jet uncertainty
					# Second jet
					'jet2pt', 'jet2eta', 'jet2phi',
					# 3rd jet
					'jet3pt', 'jet3eta', 'jet3phi',
					# MET and related
					'mpf', 'rawmpf', 'met', 'metphi', 'rawmet', 'rawmetphi', 'sumet',
					'mettype1vecpt', 'mettype1pt',
				],
			},
		},
		
		# Wire Kappa objects
		'EventMetadata' : 'eventInfo',
		'LumiMetadata' : 'lumiInfo',
		'VertexSummary': 'goodOfflinePrimaryVerticesSummary',
	}
	if tagged:
		cfg['Pipelines']['default']['Quantities'] += ['jet1btag', 'jet1qgtag']#, 'jet1puidraw','jet1puidtight','jet1puidmedium', 'jet1puidloose', 'jet2puidraw', 'jet2puidtight','jet2puidmedium', 'jet2puidloose']
#	pujetids = []
#	for x in range(2,100):
#		pujetids.append(str(x)+':puJetIDFullMedium')	
#	cfg['PuJetIDs'] = pujetids
	return cfg

###
# config fragments for single categories (data/MC, year, channel)
###

# data/MC:

def data(cfg, **kwargs):
	cfg['InputIsData'] = True
	cfg['Pipelines']['default']['Quantities'] += ['run', 'event', 'lumi','leptonTriggerSFWeight']
	cfg['Processors'] = [
		'filter:JsonFilter',
	]+cfg['Processors']+[
		'producer:HltProducer',
		'filter:HltFilter',
		
	]
	cfg['ProvideL2L3ResidualCorrections'] = True
	cfg['Pipelines']['default']['Quantities'] += ['jet1ptl1l2l3', 'jet1res']


def mc(cfg, **kwargs):
	cfg['InputIsData'] = False
	cfg['Processors'] += [
		'producer:RecoJetGenPartonMatchingProducer',
		'producer:RecoJetGenJetMatchingProducer',
		#'producer:GenParticleProducer',
		'producer:NeutrinoCounter',
	]
	cfg['GenParticles'] = 'genParticles'
	cfg['Pipelines']['default']['Quantities'] += [
		'run',
		'event',
		'lumi',
		'npu',
		'npumean',
		'njets10',
		'genjet1pt',
		'genjet1eta',
		'genjet1phi',
		'genjet2pt',
		'genjet2eta',
		'genjet2phi',
		'ngenjets',
		'ngenjets10',
		'ngenjets30',
		'matchedgenparton1pt',
		'matchedgenparton1flavour',
		'matchedgenparton2pt',
		'matchedgenjet1pt',
		'matchedgenjet1eta',
		'matchedgenjet2pt',
		'genzpt',
		'genzeta',
		'genzphi',
		'genzeta',
		'genzy',
		'genzmass',
		'genzfound',
		'validgenzfound',
		'genzlepton1pt',
		'genzlepton2pt',
		'genzlepton1eta',
		'genzlepton2eta',
		'genzlepton1phi',
		'genzlepton2phi',
		'genphistareta',
		'deltarzgenz',
		'ngenneutrinos',
		'x1',
		'x2',
		'qScale',
	]

	# RecoJetGenPartonMatchingProducer Settings
	cfg['DeltaRMatchingRecoJetGenParticle'] = 0.3
	cfg['JetMatchingAlgorithm'] = 'physics' # algorithmic or physics

	# RecoJetGenJetMatchingProducer Settings
	cfg['DeltaRMatchingRecoJetGenJet'] = 0.3

	# GenParticleProducer
	cfg['GenParticleTypes'] = ['genParticle']
	cfg['GenParticlePdgIds'] = [23] # Z
	cfg['GenParticleStatus'] = 2

	# MC sample reweighting
	cfg['Processors'] += [
		'producer:CrossSectionWeightProducer',
		'producer:ZJetNumberGeneratedEventsWeightProducer',
		'producer:EventWeightProducer',
	]
	cfg['Pipelines']['default']['Quantities'] += [
		'numberGeneratedEventsWeight',
		'crossSectionPerEventWeight',
	]
	cfg['EventWeight'] = 'weight'
	cfg['CrossSection'] = -1
	cfg['BaseWeight'] = 1000  # pb^-1 -> fb^-1

## year:

def _2012(cfg, **kwargs):
	cfg['Year'] = 2012
	cfg['Energy'] = 8
	cfg['TaggedJets'] = 'ak5PFJetsCHS'
	cfg['JetIDVersion'] = 2014
	cfg['MinZllJetDeltaRVeto'] = 0.3
	cfg['JetLeptonLowerDeltaRCut'] = 0.3

def _2015(cfg, **kwargs):
	cfg['Year'] = 2015
	cfg['Energy'] = 13
	cfg['TaggedJets'] = 'ak4PFJetsCHS'
	cfg['PileupDensity'] = 'pileupDensity'
	cfg['JetIDVersion'] = 2015
	cfg['TypeIJetPtMin'] = 15.
	cfg['MinZllJetDeltaRVeto'] = 0.3
	cfg['JetLeptonLowerDeltaRCut'] = 0.3 # JetID 2015 does not veto muon contribution - invalidate any jets that are likely muons; requires ZmmProducer and ValidZllJetsProducer to work
	# create empty containers to allow using references prematurely
	cfg["InputFiles"] = configtools.InputFiles()
	# data settings also used to derive values for mc
	cfg['Minbxsec'] = 69.0
	cfg['NPUFile'] = configtools.getPath() + '/data/pileup/pumean_data_13TeV.txt'
	if kwargs.get('bunchcrossing', "50ns") == "50ns":
		cfg['JsonFiles'] = configtools.RunJSON(configtools.getPath() + '/data/json/Cert_246908-251883_13TeV_PromptReco_Collisions15_JSON_v2.txt')
	elif kwargs.get('bunchcrossing', "50ns") == "25ns":
		cfg['JsonFiles'] = configtools.RunJSON('/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/Cert_246908-260627_13TeV_PromptReco_Collisions15_25ns_JSON_v2.txt')


def _2016(cfg, **kwargs):
	cfg['Year'] = 2016
	cfg['Energy'] = 13
	cfg['TaggedJets'] = 'ak4PFJetsCHS'
	cfg['PileupDensity'] = 'pileupDensity'
	cfg['JetIDVersion'] = 2015
	cfg['JetPtMin'] = 15.
	cfg['MinZllJetDeltaRVeto'] = 0.3
	cfg['JetLeptonLowerDeltaRCut'] = 0.3 # JetID 2015 does not veto muon contribution - invalidate any jets that are likely muons; requires ZmmProducer and ValidZllJetsProducer to work
	# create empty containers to allow using references prematurely
	cfg["InputFiles"] = configtools.InputFiles()
	# data settings also used to derive values for mc
	cfg['Minbxsec'] = 69.2
	cfg['NPUFile'] = configtools.getPath() + '/data/pileup/pumean_data_13TeV.txt'
	cfg['JsonFiles'] = configtools.RunJSON('/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/Cert_271036-284044_13TeV_PromptReco_Collisions16_JSON_NoL1T.txt')
	#cfg['JsonFiles'] = configtools.RunJSON('/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/Cert_271036-276811_13TeV_PromptReco_Collisions16_JSON.txt')


# channel:
def eemm(cfg, **kwargs):
	cfg['Muons'] = 'muons'
	cfg['Electrons'] = 'electrons'
	cfg['ElectronMetadata'] = 'electronMetadata'
	# The order of these producers is important!
	cfg['Processors'] = [
		'producer:ValidMuonsProducer',
		#'producer:ZJetValidElectronsProducer',
		'producer:ValidElectronsProducer',
		#'producer:ValidLeptonsProducer'
		'filter:MinNLeptonsCut',
		'filter:MaxNLeptonsCut',
		'producer:RecoZmmProducer',
		'filter:ZFilter',
		'producer:ValidTaggedJetsProducer',
		'producer:ValidZllJetsProducer',
		'filter:ValidJetsFilter',
		'producer:ZJetCorrectionsProducer',
		'producer:TypeIMETProducer',
		'producer:JetSorter',
	]
	cfg['Pipelines']['default']['Processors'] = [
		'filter:LeadingLeptonPtCut',
		'filter:LeadingJetPtCut',
		'filter:LeadingJetEtaCut',
		'filter:AlphaCut',
		'filter:ZPtCut',
		'filter:BackToBackCut',
	]
	cfg['Pipelines']['default']['Consumers'] += [
		'KappaMuonsConsumer',
	]

	# ValidMuonsProducer
	cfg['MuonID'] = 'tight'
	cfg['MuonIso'] = 'loose'
	cfg['MuonIsoType'] = 'pf'
	
	cfg['ElectronID'] = 'vbft95_tight'
	cfg['ElectronIsoType'] = 'none'
	cfg['ElectronIso'] = 'none'
	cfg['ElectronReco'] = 'none'
	

	cfg['Pipelines']['default']['Quantities'] += [
		'mupluspt', 'mupluseta', 'muplusphi', 'muplusiso',
		'muminuspt', 'muminuseta', 'muminusphi', 'muminusiso',
		'mu1pt', 'mu1eta', 'mu1phi',
		'mu1iso', 'mu1sumchpt', 'mu1sumnhet', 'mu1sumpet', 'mu1sumpupt',
		'mu2pt', 'mu2eta', 'mu2phi',
		'nmuons',
	]
	cfg['CutNLeptonsMin'] = 2
	cfg['CutNLeptonsMax'] = 3

	cfg['CutLeadingLeptonPtMin'] = 20.0
	cfg['CutMuonEtaMax'] = 2.3
	cfg['CutLeadingJetPtMin'] = 12.0
	cfg['CutLeadingJetEtaMax'] = 1.3
	cfg['CutZPtMin'] = 30.0
	cfg['CutBackToBack'] = 0.34
	cfg['CutAlphaMax'] = 0.2
  


def ee(cfg, **kwargs):
	cfg['Electrons'] = 'electrons'
	cfg['ElectronMetadata'] = 'electronMetadata'
	# The order of these producers is important!
	cfg['Processors'] = [
		# electrons
		'producer:ZJetValidElectronsProducer',
		'filter:MinElectronsCountFilter',
		'filter:MaxElectronsCountFilter',
		# Z
		'producer:ZeeProducer',
		'filter:ZFilter',
		# jets
		'producer:ValidTaggedJetsProducer',
		'producer:ValidZllJetsProducer',
		'filter:ValidJetsFilter',
		'producer:ZJetCorrectionsProducer',
		'producer:TypeIMETProducer',
		'producer:JetSorter',
	]
	cfg['ElectronID'] = 'vbft95_tight'
	cfg['ElectronIsoType'] = 'none'
	cfg['ElectronIso'] = 'none'
	cfg['ElectronReco'] = 'none'

	cfg['MinNElectrons'] = 2
	cfg['MaxNElectrons'] = 3

	cfg['CutElectronPtMin'] = 25.0
	cfg['CutElectronEtaMax'] = 2.4
	cfg['CutLeadingJetPtMin'] = 12.0
	cfg['CutLeadingJetEtaMax'] = 1.3
	cfg['CutZPtMin'] = 30.0
	cfg['CutBackToBack'] = 0.34
	cfg['CutAlphaMax'] = 0.2
	cfg['ZMassRange'] = 20

	cfg['Pipelines']['default']['Quantities'] += [
		'epluspt', 'epluseta', 'eplusphi', 'eplusiso',
		'eminuspt', 'eminuseta', 'eminusphi', 'eminusiso',
		'e1pt', 'e1eta', 'e1phi', 'e1looseid', 'e1mediumid', 'e1tightid', 'e1vetoid',
		'e1looseid95', 'e1mediumid95', 'e1tightid95',# 'e1mvanontrig', 'e1mvatrig',
		'e2pt', 'e2eta', 'e2phi', 'e2looseid', 'e2mediumid', 'e2tightid', 'e2vetoid',
		'e2looseid95', 'e2mediumid95', 'e2tightid95',# 'e2mvanontrig', 'e2mvatrig',
		'nelectrons',
	]
	cfg['Pipelines']['default']['Processors'] = [
		'filter:ElectronPtCut',
		'filter:ElectronEtaCut',
		'filter:LeadingJetPtCut',
		'filter:LeadingJetEtaCut',
		'filter:AlphaCut',
		'filter:ZPtCut',
		'filter:BackToBackCut',
	]
	cfg['Pipelines']['default']['Consumers'] += [
		'KappaElectronsConsumer',
	]

def em(cfg, **kwargs):
	cfg['Electrons'] = 'correlectrons'
	cfg['Muons'] = 'muons'
	cfg['ElectronMetadata'] = 'electronMetadata'
	# The order of these producers is important!
	cfg['Processors'] = [
		# leptons
		'producer:ValidMuonsProducer',
		'filter:MinNMuonsCut',
		'producer:ValidElectronsProducer',
		'filter:MinElectronsCountFilter',
		# Z
		'producer:ZemProducer',
		'filter:ZFilter',
		# jets
		'producer:ValidTaggedJetsProducer',
		'producer:ValidZllJetsProducer',
		'filter:ValidJetsFilter',
		'producer:ZJetCorrectionsProducer',
		'producer:TypeIMETProducer',
		'producer:JetSorter',
	]
	cfg['ElectronID'] = 'mvanontrig'
	cfg['ElectronIsoType'] = 'pf'
	cfg['ElectronIso'] = 'mvanontrig'
	cfg['ElectronReco'] = 'none'

	# validMuonsProducer
	cfg['MuonID'] = 'tight'
	cfg['MuonIso'] = 'loose'
	cfg['MuonIsoType'] = 'pf'

	cfg['MinNElectrons'] = 1
	cfg['CutNMuonsMin'] = 1

	cfg['CutElectronPtMin'] = 25.0
	cfg['CutElectronEtaMax'] = 2.4
	cfg['CutMuonPtMin'] = 20.0
	cfg['CutMuonEtaMax'] = 2.3
	cfg['CutLeadingJetPtMin'] = 12.0
	cfg['CutLeadingJetEtaMax'] = 1.3
	cfg['CutZPtMin'] = 30.0
	cfg['CutBackToBack'] = 0.34
	cfg['CutAlphaMax'] = 0.2

	cfg['Pipelines']['default']['Quantities'] += [
		'e1pt', 'e1eta', 'e1phi', 'e1looseid', 'e1mediumid', 'e1tightid', 'e1vetoid',
		'e1looseid95', 'e1mediumid95', 'e1tightid95', 'e1mvanontrig', 'e1mvatrig',
		'nelectrons',
		'njets30',
		'mu1pt', 'mu1eta', 'mu1phi',
		'mu1iso', 'mu1sumchpt', 'mu1sumnhet', 'mu1sumpet', 'mu1sumpupt',
		'nmuons', 'ngenmuons', 'nvalidgenmuons'
	]

	cfg['Pipelines']['default']['Processors'] = [
		'filter:MuonPtCut',
		'filter:MuonEtaCut',
		'filter:ElectronPtCut',
		'filter:ElectronEtaCut',
		'filter:LeadingJetPtCut',
		'filter:LeadingJetEtaCut',
		'filter:AlphaCut',
		'filter:ZPtCut',
		'filter:BackToBackCut',
	]
	cfg['Pipelines']['default']['Consumers'] += [
		'KappaElectronsConsumer',
		'KappaMuonsConsumer',
	]


def mm(cfg, **kwargs):
	cfg['Muons'] = 'muons'
	# The order of these producers is important!
	cfg['Processors'] = [
		'producer:MuonCorrectionsProducer',
		'producer:ValidMuonsProducer',
		'producer:RecoZmmProducer',
		
	]
	cfg['Pipelines']['default']['Processors'] = [
		'filter:ValidGenZCut',
		#'filter:MinNGenMuonsCut',
		#'filter:GenMuonPtCut',
		#'filter:GenMuonEtaCut',
		'filter:GenZPtCut',
		'filter:ValidZCut',
		'filter:MinNMuonsCut',
		'filter:MaxNMuonsCut',
		#'filter:LeadingLeptonPtCut',
		#'filter:MuonEtaCut',
		'filter:ZPtCut',
		#'filter:LeadingJetPtCut',
		#'filter:LeadingJetEtaCut',
		#'filter:AlphaCut',
		#'filter:BackToBackCut',
		#'filter:GenMuPlusCut',
		#'filter:MuPlusCut',
	]
	cfg['Pipelines']['default']['Consumers'] += [
		'KappaMuonsConsumer',
	]

	# validMuonsProducer
	cfg['MuonID'] = 'tight'
	cfg['MuonIso'] = 'loose'
	cfg['MuonIsoType'] = 'pf'
	#cfg['UseHighPtID'] = True
	
	cfg['Pipelines']['default']['Quantities'] += [
		'mupluspt', 'mupluseta', 'muplusphi', 'muplusiso',
		'muminuspt', 'muminuseta', 'muminusphi', 'muminusiso',
		'mu1pt', 'mu1eta', 'mu1phi',
		'mu1iso', 'mu1sumchpt', 'mu1sumnhet', 'mu1sumpet', 'mu1sumpupt',
		'mu2pt', 'mu2eta', 'mu2phi',
		'nmuons', 'leptonSFWeight', 'validz'
	]
	cfg['CutNMuonsMin'] = 2
	cfg['CutNMuonsMax'] = 3
	cfg['MuonLowerPtCuts'] = ['27']
	cfg['MuonUpperAbsEtaCuts'] = ['2.3']
	cfg['GenMuonLowerPtCuts'] = ['27']
	cfg['GenMuonUpperAbsEtaCuts'] = ['2.3']
	cfg['CutZPtMin'] = 40.0

#Efficiency calculation
	
	cfg["InvalidateNonMatchingMuons"] = False
	cfg["TriggerObjects"] = "triggerObjects"
	cfg["TriggerInfos"] = "triggerObjectMetadata"
###
# config fragments for combinations of two categories (data/MC+year, year+channel, ...)
###

def data_2012(cfg, **kwargs):
	cfg['Jec'] = configtools.getPath() + '/data/jec/Winter14_V8/Winter14_V8_DATA'
	cfg['JsonFiles'] = [configtools.getPath() + '/data/json/Cert_190456-208686_8TeV_22Jan2013ReReco_Collisions12_JSON.txt']
	cfg['Lumi'] = 19.712
	cfg['MetPhiCorrectionParameters'] = [0.2661, 0.3217, -0.2251, -0.1747]

	cfg['Processors'] += ['producer:NPUProducer']
	cfg['Minbxsec'] = 68.5
	cfg['NPUFile'] = configtools.getPath() + '/data/pileup/pumean_pixelcorr_data2012.txt'
	cfg['Pipelines']['default']['Quantities'] += ['npumean']


def data_2015(cfg, **kwargs):
	cfg['Processors'] += ['producer:NPUProducer']
	cfg['Pipelines']['default']['Quantities'] += ['npumean']
	cfg['CutAlphaMax'] = 0.3
	if kwargs.get('bunchcrossing', "50ns") == "50ns":
		cfg['Jec'] = configtools.getPath() + '/data/jec/Summer15_50nsV5_DATA/Summer15_50nsV5_DATA'
		cfg['Lumi'] = 0.04003
	elif kwargs.get('bunchcrossing', "50ns") == "25ns":
		cfg['Jec'] = configtools.get_jec("Fall15_25nsV2_DATA")
		#cfg['Lumi'] = configtools.Lumi(json_source=cfg['JsonFiles'],normtag='/afs/cern.ch/user/c/cmsbril/public/normtag_json/OfflineNormtagV1.json')
	else:
		raise ValueError("No support for 'bunchcrossing' %r" % kwargs['bunchcrossing'])

def data_2016(cfg, **kwargs):
	#cfg['Processors'] += ['producer:NPUProducer']
	#cfg['Pipelines']['default']['Quantities'] += ['npumean']
	cfg['CutAlphaMax'] = 0.3
	#cfg['Lumi'] = configtools.Lumi(json_source=cfg['JsonFiles'], normtag='')

def mc_2012(cfg, **kwargs):
	cfg['GenJets'] = 'AK5GenJetsNoNu'
	cfg['Jec'] = configtools.getPath() + '/data/jec/Winter14_V8/Winter14_V8_MC'
	cfg['MetPhiCorrectionParameters'] = [0.1166, 0.0200, 0.2764, -0.1280]
	# insert PU weight producer before EventWeightProducer:
	cfg['Processors'].insert(cfg['Processors'].index('producer:EventWeightProducer'), 'producer:PUWeightProducer')
	# 2012 PU weight file determined with: puWeightCalc.py data/json/Cert_190456-208686_8TeV_22Jan2013ReReco_Collisions12_JSON.txt /storage/a/dhaitz/skims/2015-05-16_DYJetsToLL_M_50_madgraph_8TeV/*.root  --inputLumiJSON /afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions12/8TeV/PileUp/pileup_latest.txt  --minBiasXsec 69 --weight-limits 0 10   --output $EXCALIBURPATH/data/pileup/weights_190456-208686_8TeV_22Jan2013ReReco_madgraphPU-RD.root
	cfg['Pipelines']['default']['Quantities'] += ['puWeight']

def mc_2015(cfg, **kwargs):
	#cfg['PileupWeightFile'] = configtools.PUWeights(cfg['JsonFiles'], cfg['InputFiles'], pileup_json="/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/PileUp/pileup_latest.txt", min_bias_xsec=cfg['Minbxsec'], weight_limits=(0, 4))
	cfg['CutAlphaMax'] = 0.3
	cfg['GenJets'] = 'ak4GenJetsNoNu'
	cfg['GenParticleStatus'] = 22  # see also http://www.phy.pku.edu.cn/~qhcao/resources/CTEQ/MCTutorial/Day1.pdf
	# insert Generator producer before EventWeightProducer:
	cfg['Processors'].insert(cfg['Processors'].index('producer:EventWeightProducer'), 'producer:GeneratorWeightProducer')
	cfg['Pipelines']['default']['Quantities'] += ['generatorWeight']
	#cfg['Processors'].insert(cfg['Processors'].index('producer:EventWeightProducer'), 'producer:PUWeightProducer')
	#cfg['Pipelines']['default']['Quantities'] += ['puWeight']
	if kwargs.get('bunchcrossing', "50ns") == "50ns":
		cfg['Jec'] = configtools.getPath() + '/data/jec/Summer15_50nsV5_MC/Summer15_50nsV5_MC'
	elif kwargs['bunchcrossing'] == "25ns":
		# use WIP corrections until full tarballs are available again -- MF@20160215
		#cfg['Jec'] = configtools.getPath() + '/data/jec/Fall15_25nsV2_MC/Fall15_25nsV2_MC'
		cfg['Jec'] = configtools.getPath() + '/data/jec/Fall15_25nsV2_MC/Fall15_25nsV2_MC'
		#cfg['Jec'] = configtools.getPath() + '/data/jec/Fall15_25nsV1_MC/Fall15_25nsV1_MC'
		# cfg['Jec'] = configtools.get_jec("Fall15_25nsV1_MC")-
	else:
		raise ValueError("No support for 'bunchcrossing' %r" % kwargs['bunchcrossing'])

def mc_2016(cfg, **kwargs):
	cfg['DeltaRRadiationJet'] = 1
	cfg['CutAlphaMax'] = 0.3
	cfg['CutBetaMax'] = 0.1
	cfg['GenJets'] = 'ak4GenJetsNoNu'
	cfg['UseKLVGenJets'] = True
	cfg['GenParticleStatus'] = 22  # see also http://www.phy.pku.edu.cn/~qhcao/resources/CTEQ/MCTutorial/Day1.pdf
	# insert Generator producer before EventWeightProducer:
	cfg['Processors'].insert(cfg['Processors'].index('producer:EventWeightProducer'), 'producer:GeneratorWeightProducer')
	cfg['Pipelines']['default']['Quantities'] += ['generatorWeight']
	# use WIP corrections until full tarballs are available again -- MF@20160215

def mcee(cfg, **kwargs):
	cfg['Pipelines']['default']['Quantities'] += [
		'ngenelectrons',
		'geneminusphi',
		'genParticleMatchDeltaR',
	]
	# reco-gen electron matching producer
	cfg['Processors'] += ['producer:RecoElectronGenParticleMatchingProducer']
	cfg['RecoElectronMatchingGenParticleStatus'] = 3
	cfg['DeltaRMatchingRecoElectronGenParticle'] = 0.3
	cfg["RecoElectronMatchingGenParticlePdgIds"] = [11, -11]
	cfg["InvalidateNonGenParticleMatchingRecoElectrons"] = False
	cfg['GenParticleTypes'] += ['genElectron']
	cfg['GenElectronStatus'] = 3
	# KappaCollectionsConsumer: dont add taus or taujets:
	cfg['BranchGenMatchedElectrons'] = True
	cfg['AddGenMatchedTaus'] = False
	cfg['AddGenMatchedTauJets'] = False

def mcmm(cfg, **kwargs):
	cfg['Pipelines']['default']['Quantities'] += [
		'matchedgenmuon1pt',
		'matchedgenmuon2pt',
		'ngenmuons',
		'genmupluspt',
		'genmupluseta',
		'genmuplusphi',
		'genmuminuspt',
		'genmuminuseta',
		'genmuminusphi',
		'leptonTriggerSFWeight',
		'genmu1pt',
		'genmu2pt',
		'genmu1eta',
		'genmu2eta',
		'genmu1phi',
		'genmu2phi',
	]
	cfg['Processors'] += [
			'producer:ZJetGenMuonProducer', 
			'producer:GenZmmProducer', #Use this for Status 1 muons
			#'producer:ValidGenZmmProducer', #Use this for original muons
		      	'producer:RecoMuonGenParticleMatchingProducer',
			]
	cfg['RecoMuonMatchingGenParticleStatus'] = 1
	cfg['DeltaRMatchingRecoMuonGenParticle'] = 0.5 # TODO: check if lower cut is more reasonable
	#cfg['Processors'].insert(cfg['Processors'].index('producer:EventWeightProducer'), 'producer:HltProducer')
	#cfg['Processors'].insert(cfg['Processors'].index('producer:EventWeightProducer'), 'filter:HltFilter')
	#cfg['Processors'].insert(cfg['Processors'].index('producer:EventWeightProducer'), 'producer:MuonTriggerMatchingProducer')
	cfg['Processors']+= 'producer:LeptonSFProducer',
	#cfg['Pipelines']['default']['Processors']+= 'producer:LeptonTriggerSFProducer',
	cfg['GenParticleTypes'] += ['genMuon', 'genTau']
	cfg['GenMuonStatus'] = 1
	cfg['TriggerSFRuns'] = []

	# for KappaMuonsConsumer
	cfg['BranchGenMatchedMuons'] = True
	cfg['AddGenMatchedTaus'] = False
	cfg['AddGenMatchedTauJets'] = False

def _2012mm(cfg, **kwargs):
	pass

def _2012ee(cfg, **kwargs):
	cfg['ZMassRange'] = 10
	cfg['Electrons']='correlectrons'
	cfg['HltPaths'] = ['HLT_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL']
	cfg['ExcludeECALGap'] = True

def _2015mm(cfg, **kwargs):
	#cfg['MuonID'] = 'tight'
	cfg['HltPaths'] = ['HLT_IsoMu20', 'HLT_IsoTkMu20']
	cfg['EventWeight'] = 'weight'
	cfg['MuonRochesterCorrectionsFile'] = configtools.getPath()+'/../Artus/KappaAnalysis/data/rochcorr/RoccoR_13tev_2015.txt'
	cfg['MuonEnergyCorrection'] = 'rochcorr2015'
	cfg['ValidMuonsInput'] = "corrected"
	cfg["MuonTriggerFilterNames"] = ["HLT_IsoMu20_v2:hltL3crIsoL1sMu16L1f0L2f10QL3f20QL3trkIsoFiltered0p09", "HLT_IsoTkMu20_v3:hltL3fL1sMu16L1f0Tkf20QL3trkIsoFiltered0p09", "HLT_IsoMu20_eta2p1_LooseIsoPFTau20_v1:hltOverlapFilterSingleIsoMu20LooseIsoPFTau20", "HLT_IsoTkMu20_eta2p1_v2:hltL3fL1sMu16Eta2p1L1f0Tkf20QL3trkIsoFiltered0p09","HLT_IsoMu20_v3:hltL3fL1sMu16L1f0L2f10QL3Filtered20QL3pfhcalIsoRhoFilteredHB0p21HE0p22","HLT_IsoTkMu20_v4:hltL3crIsoL1sMu16L1f0L2f10QL3f20QL3trkIsoFiltered0p09"]

def _2016mm(cfg, **kwargs):
	#cfg['MuonID'] = 'tight'
	cfg['HltPaths'] = ['HLT_IsoMu22', 'HLT_IsoTkMu22']
	cfg['EventWeight'] = 'weight'
	cfg['MuonRochesterCorrectionsFile'] = configtools.getPath()+'/../Artus/KappaAnalysis/data/rochcorr2016'
	cfg['MuonEnergyCorrection'] = 'rochcorr2016'
	cfg['ValidMuonsInput'] = "corrected"
	cfg["MuonTriggerFilterNames"] = ["HLT_IsoMu22_v2:hltL3crIsoL1sMu20L1f0L2f10QL3f22QL3trkIsoFiltered0p09","HLT_IsoTkMu22_v2:hltL3fL1sMu20L1f0Tkf22QL3trkIsoFiltered0p09", "HLT_IsoTkMu22_v3: hltL3fL1sMu20L1f0Tkf22QL3trkIsoFiltered0p09", "HLT_IsoMu22_v3:hltL3crIsoL1sMu20L1f0L2f10QL3f22QL3trkIsoFiltered0p09","HLT_IsoTkMu22_v4:hltL3fL1sMu20L1f0Tkf22QL3trkIsoFiltered0p09"]
	#cfg["MuonTriggerFilterNames"] = ['HLT_IsoMu24_v2:hltL3crIsoL1sMu22L1f0L2f10QL3f24QL3trkIsoFiltered0p09','HLT_IsoTkMu24_v3:hltL3fL1sMu22L1f0Tkf24QL3trkIsoFiltered0p09']
 

###
# config fragments for combinations of three categories (data/MC+year+channel)
###

def mc_2012ee(cfg, **kwargs):
	cfg['Processors'] += ['producer:HltProducer']
	cfg['Pipelines']['default']['Quantities'] += ['hlt']

def data_2015mm(cfg, **kwargs):
	cfg['Processors'] += ['producer:MuonTriggerMatchingProducer', 'producer:LeptonSFProducer','producer:LeptonTriggerSFProducer']
	cfg['MuonPtVariationFactor'] = 1.00
	cfg['LeptonSFRootfile'] = configtools.getPath()+"/data/scalefactors/2015/SFData.root"
	cfg['LeptonTriggerSFRootfile'] = configtools.getPath()+"/data/scalefactors/2015/SFTriggerData.root"
	#cfg['LeptonTriggerSFVariation'] = "up"

def data_2016mm(cfg, **kwargs):
	cfg['Pipelines']['default']['Processors'] += ['producer:MuonTriggerMatchingProducer','producer:LeptonSFProducer','producer:LeptonTriggerSFProducer']
	cfg['MuonPtVariationFactor'] = 1.00
	cfg['LeptonSFRootfile'] = configtools.getPath()+"/data/scalefactors/2016/SFData_ICHEP.root"
	cfg['LeptonTriggerSFRootfile'] = configtools.getPath()+"/data/scalefactors/2016/SFTriggerData.root"
	cfg['TriggerSFRuns'] = [274094,276097]

def data_2012em(cfg, **kwargs):
	cfg['HltPaths'] = ['HLT_Mu17_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL', 'HLT_Mu8_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL']

def data_2015ee(cfg, **kwargs):
	cfg['HltPaths']= ['HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ', 'HLT_Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_DZ', 'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL', 'HLT_Ele17_Ele12_CaloIdL_TrackIdL_IsoVL']
	cfg['Electrons']= 'electrons'
def mc_2012mm(cfg, **kwargs):
	pass
	# muon corrections - not active at the moment
	#cfg['Processors'].insert(cfg['Processors'].index('producer:ValidMuonsProducer')+1, 'producer:MuonCorrector')
	#cfg["MuonSmearing"] = True
	#cfg["MuonRadiationCorrection"] = False
	#cfg["MuonCorrectionParameters"] = configtools.getPath() + "/data/muoncorrection/MuScleFit_2012_MC_53X_smearReReco.txt"

def data_2012mm(cfg, **kwargs):
	cfg['HltPaths'] = ['HLT_Mu17_Mu8']
	# muon corrections - not active at the moment
	#cfg['Processors'].insert(cfg['Processors'].index('producer:ValidMuonsProducer')+1, 'producer:MuonCorrector')
	#cfg["MuonRadiationCorrection"] = False
	#cfg["MuonSmearing"] = False
	#cfg["MuonCorrectionParameters"] = configtools.getPath() + "/data/muoncorrection/MuScleFit_2012ABC_DATA_ReReco_53X.txt"

	#cfg["MuonCorrectionParametersRunD"] = configtools.getPath() + "/data/muoncorrection/MuScleFit_2012D_DATA_ReReco_53X.txt"

def mc_2015ee(cfg, **kwargs):
	# not sure about the status codes in aMCatNLO/MG5. theres usually an e+/e-
	# pair with status 1 in each event, so take this number for now
	# see also http://www.phy.pku.edu.cn/~qhcao/resources/CTEQ/MCTutorial/Day1.pdf
	cfg['RecoElectronMatchingGenParticleStatus'] = 1
	cfg[''] = 1

def mc_2015mm(cfg, **kwargs):
	cfg['LeptonSFRootfile'] = configtools.getPath()+"/data/scalefactors/2015/SFMC.root"
	cfg['LeptonTriggerSFRootfile'] = configtools.getPath()+"/data/scalefactors/2015/SFTriggerMC.root"

def mc_2016mm(cfg, **kwargs):
	cfg['LeptonSFRootfile'] = configtools.getPath()+"/data/scalefactors/2016/SFMC_ICHEP.root"
	cfg['LeptonTriggerSFRootfile'] = configtools.getPath()+"/data/scalefactors/2016/SFTriggerMC.root"

def data_2016ee(cfg, **kwargs):
	cfg['HltPaths']= ['HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ', 'HLT_Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_DZ', 'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL', 'HLT_Ele17_Ele12_CaloIdL_TrackIdL_IsoVL']
	cfg['Electrons']= 'electrons'

def mc_2016ee(cfg, **kwargs):
	# not sure about the status codes in aMCatNLO/MG5. theres usually an e+/e-
	# pair with status 1 in each event, so take this number for now
	# see also http://www.phy.pku.edu.cn/~qhcao/resources/CTEQ/MCTutorial/Day1.pdf
	cfg['RecoElectronMatchingGenParticleStatus'] = 1
	cfg[''] = 1

