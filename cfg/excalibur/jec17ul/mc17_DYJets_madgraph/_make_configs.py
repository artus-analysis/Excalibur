"""
Quick and dirty script to generate config files for all channels, JEC versions, etc,
which can then be edited manually. Note: existing configs with matching names will
be overwritten!
"""

INPUT_TEMPLATE = '"{{}}/{userpath}/ZJet_DYJetsToLL_Summer19-madgraphMLM_realistic_v6-v3/*.root".format(SE_PATH_PREFIXES["xrootd_gridka_nrg"])'

TEMPLATE = """
import configtools
import os
import sys

# -- import common information
sys.path.append(os.path.dirname(__file__))
from common import JEC_BASE, JEC_VERSION, JER, SE_PATH_PREFIXES

RUN='{run}'
CH='{ch}'
JEC='{{}}_{{}}_{jecv_suffix}'.format(JEC_BASE, JEC_VERSION)


def config():
    cfg = configtools.getConfig('mc', 2017, CH, JEC=JEC, JER=JER)
    cfg["InputFiles"].set_input(
        path={input_path},
    )
    cfg['JsonFiles'] = [os.path.join(configtools.getPath(), 'data/json/Cert_294927-306462_13TeV_PromptReco_Collisions17_JSON.txt')]

    cfg = configtools.expand(cfg, ['nocuts','basiccuts','finalcuts'], ['None', 'L1', 'L1L2L3'])
    cfg['PileupWeightFile'] = os.path.join(configtools.getPath() , 'data/pileup/mc_weights/mc17_DYJets_madgraph/PUWeights_BCDEF_17Nov2017_DY1JetsToLL_Fall17-madgraphMLM_realistic_v10-v1.root')
    cfg['NumberGeneratedEvents'] = 101077576
    cfg['GeneratorWeight'] = 1.0
    cfg['CrossSection'] = 6077.22  # from XSDB: https://cms-gen-dev.cern.ch/xsdb/?searchQuery=DAS=DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8

    cfg['VertexSummary'] = 'offlinePrimaryVerticesSummary'

    cfg['ApplyElectronVID'] = True
    cfg['ElectronVIDName'] = "Fall17-94X-V2"
    cfg['ElectronVIDType'] = "cutbased"
    cfg['ElectronVIDWorkingPoint'] = "tight"

    return cfg
"""

def make():
    for jecv_suffix in ('SimpleL1', 'ComplexL1'):
      for ch in ("mm", "ee"):
          _cfg = TEMPLATE.format(
            run='BCDEF',
            jecv_suffix=jecv_suffix,
            ch=ch,
            input_path=INPUT_TEMPLATE.format(
              userpath='mhorzela/Skimming',
            ),
          )
          _fname = "mc17_{ch}_DYJets_Madgraph_JEC{jecv_suffix}.py".format(
            jecv_suffix=jecv_suffix,
            ch=ch,            
          )
          with open(_fname, 'w') as _f:
            _f.write(_cfg)

if __name__ == '__main__':    
    make()