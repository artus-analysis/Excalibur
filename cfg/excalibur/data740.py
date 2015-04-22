import ZJetConfigBase as base
import data

def config():
    cfg = data.config()
    cfg["InputFiles"] = base.setInputFiles(
        ekppath="/storage/a/dhaitz/skims/2015-04-21_DoubleMu_Run2012_740pre9ROOT6_8TeV/*.root",
        nafpath="/pnfs/desy.de/cms/tier2/store/user/dhaitz/2015-04-21_DoubleMu_Run2012_740pre9ROOT6_8TeV/*.root",
    )
    cfg['Processors'].remove("filter:HltFilter")
    return cfg
