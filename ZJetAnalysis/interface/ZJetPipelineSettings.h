/* Copyright (c) 2014 - All Rights Reserved
 *   Dominik Haitz <dhaitz@cern.ch>
 */

#pragma once

#include "Artus/KappaAnalysis/interface/KappaPipelineSettings.h"

class ZJetPipelineSettings: public KappaPipelineSettings {
public:
	IMPL_SETTING(std::string, JetAlgorithm)
	
	IMPL_SETTING(float, ZPtMin)
	
	IMPL_SETTING(float, JetPtMin)
	IMPL_SETTING(float, JetEtaMax)
};

class ZJetGlobalSettings: public KappaGlobalSettings {
public:

	IMPL_SETTING_DEFAULT(std::string, TaggerMetadata, "")

	IMPL_SETTING(bool, InputIsData)
	
	IMPL_SETTING(bool, MuonID2011)
	IMPL_SETTING(float, MuonEtaMax)
	IMPL_SETTING(float, MuonPtMin)

	IMPL_SETTING(float, ZMassMax)
	IMPL_SETTING(float, ZMassMin)
	
	IMPL_SETTING(bool, VetoPileupJets)
	
	IMPL_SETTING(float, ZPtMin)
	
	IMPL_SETTING(float, JetPtMin)
	IMPL_SETTING(float, JetEtaMax)

};
