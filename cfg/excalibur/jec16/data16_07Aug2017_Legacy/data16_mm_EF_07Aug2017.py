import configtools
import os
import sys

# -- import common information
sys.path.append(os.path.dirname(__file__))
from common import JEC_BASE, JEC_VERSION, SE_PATH_PREFIXES

RUN='EF'
CH='mm'
JEC='{}{}_{}'.format(JEC_BASE, RUN, JEC_VERSION)


def config():
    cfg = configtools.getConfig('data', 2016, CH, JEC=JEC, IOV=RUN)
    cfg["InputFiles"].set_input(
        # bmspathE="{}/tberger/Skimming/ZJet_DoubleMuon_Run2016E-Legacy-07Aug2017-v1/*.root".format(SE_PATH_PREFIXES['srm_gridka_nrg']),
        # bmspathF="{}/tberger/Skimming/ZJet_DoubleMuon_Run2016F-Legacy-07Aug2017-v1/*.root".format(SE_PATH_PREFIXES['srm_gridka_nrg']),
        # ekppathE="{}/tberger/Skimming/ZJet_DoubleMuon_Run2016E-Legacy-07Aug2017-v1/*.root".format(SE_PATH_PREFIXES['srm_gridka_nrg']),
        # ekppathF="{}/tberger/Skimming/ZJet_DoubleMuon_Run2016F-Legacy-07Aug2017-v1/*.root".format(SE_PATH_PREFIXES['srm_gridka_nrg']),
        pathE="{}/tberger/Skimming/ZJet_DoubleMuon_Run2016E-Legacy-07Aug2017-v1/*.root".format(SE_PATH_PREFIXES['xrootd_gridka_nrg']),
        pathF="{}/tberger/Skimming/ZJet_DoubleMuon_Run2016F-Legacy-07Aug2017-v1/*.root".format(SE_PATH_PREFIXES['xrootd_gridka_nrg']),
    )
    cfg['JsonFiles'] =  [os.path.join(configtools.getPath(),'data/json/Cert_{}_13TeV_23Sep2016ReReco_Collisions16_JSON.txt'.format(RUN))]

    cfg['VertexSummary'] = 'offlinePrimaryVerticesSummary'  # above skims do not contain 'goodOfflinePrimaryVerticesSummary'
    cfg['ProvideL2ResidualCorrections'] = True
    cfg = configtools.expand(cfg, ['basiccuts', 'finalcuts'], ['None', 'L1', 'L1L2L3', 'L1L2Res', 'L1L2L3Res'])

    return cfg
