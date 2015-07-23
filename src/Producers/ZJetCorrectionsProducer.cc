#include "KappaTools/Toolbox/StringTools.h"

#include "Producers/ZJetCorrectionsProducer.h"


std::string ZJetCorrectionsProducer::GetProducerId() const {
	return "ZJetCorrectionsProducer";
}

void ZJetCorrectionsProducer::Init(ZJetSettings const& settings)
{
	ZJetProducerBase::Init(settings);

	// convert usual algo name (ak5PFJetsCHS) to txt file algo name (AK5PFchs)
	std::string jetName = "Jets";
	if (settings.GetTaggedJets().find("Tagged") != std::string::npos ) // to be removed after transition phase
		jetName = "TaggedJets";
	std::vector<std::string> algoNameAndType = KappaTools::split(settings.GetTaggedJets(), jetName);
	if (KappaTools::tolower(algoNameAndType[1]) == "puppi") // to be removed when puppi correction files exist
	{
		algoNameAndType[1] = "chs";
		LOG(WARNING) << "\t -- USING CHS correction files for puppi jets";
	}
	std::string algoName = KappaTools::toupper(algoNameAndType[0].substr(0, 2)) + algoNameAndType[0].substr(2, std::string::npos) + KappaTools::tolower(algoNameAndType[1]);
	LOG(INFO) << "\t -- Jet corrections enabled for " << algoName << " jets using the following JEC files:";

	// JEC initialization
	std::vector<JetCorrectorParameters> jecParameters;

	// L1 depending on config parameter
	jecParameters.push_back(JetCorrectorParameters(settings.GetJec() + "_" + settings.GetL1Correction() + "_" + algoName + ".txt"));
	LOG(INFO) << "\t -- " << settings.GetJec() << "_" << settings.GetL1Correction() << "_" << algoName << ".txt";
	m_l1 = new FactorizedJetCorrector(jecParameters);
	jecParameters.clear();

	// RC
	if (settings.GetRC())
	{
		jecParameters.push_back(JetCorrectorParameters(settings.GetJec() + "_" + "RC" + "_" + algoName + ".txt"));
		LOG(INFO) << "\t -- " << settings.GetJec() << "_" << "RC" << "_" << algoName << ".txt";
		m_rc = new FactorizedJetCorrector(jecParameters);
		jecParameters.clear();
	}

	// L2Relative
	jecParameters.push_back(JetCorrectorParameters(settings.GetJec() + "_" + "L2Relative" + "_" + algoName + ".txt"));
	LOG(INFO) << "\t -- " << settings.GetJec() << "_" << "L2Relative" << "_" << algoName << ".txt";
	m_l2 = new FactorizedJetCorrector(jecParameters);
	jecParameters.clear();

	// L3Absolute
	jecParameters.push_back(JetCorrectorParameters(settings.GetJec() + "_" + "L3Absolute" + "_" + algoName + ".txt"));
	LOG(INFO) << "\t -- " << settings.GetJec() << "_" << "L3Absolute" << "_" << algoName << ".txt";
	m_l3 = new FactorizedJetCorrector(jecParameters);
	jecParameters.clear();

	// Flavor based corrections
	if (settings.GetFlavourCorrections())
	{
		jecParameters.push_back(JetCorrectorParameters(settings.GetJec() + "_" + "L5Flavor_qJ" + "_" + algoName + ".txt"));
		LOG(INFO) << "\t -- " << settings.GetJec() << "_" << "L5Flavor_qJ" << "_" << algoName << ".txt";
		m_l5q = new FactorizedJetCorrector(jecParameters);
		jecParameters.clear();
		jecParameters.push_back(JetCorrectorParameters(settings.GetJec() + "_" + "L5Flavor_gJ" + "_" + algoName + ".txt"));
		LOG(INFO) << "\t -- " << settings.GetJec() << "_" << "L5Flavor_gJ" << "_" << algoName << ".txt";
		m_l5g = new FactorizedJetCorrector(jecParameters);
		jecParameters.clear();
		jecParameters.push_back(JetCorrectorParameters(settings.GetJec() + "_" + "L5Flavor_cJ" + "_" + algoName + ".txt"));
		LOG(INFO) << "\t -- " << settings.GetJec() << "_" << "L5Flavor_cJ" << "_" << algoName << ".txt";
		m_l5c = new FactorizedJetCorrector(jecParameters);
		jecParameters.clear();
		jecParameters.push_back(JetCorrectorParameters(settings.GetJec() + "_" + "L5Flavor_bJ" + "_" + algoName + ".txt"));
		LOG(INFO) << "\t -- " << settings.GetJec() << "_" << "L5Flavor_bJ" << "_" << algoName << ".txt";
		m_l5b = new FactorizedJetCorrector(jecParameters);
		jecParameters.clear();
	}

	// L2L3Residual
	if (settings.GetInputIsData() && settings.GetProvideResidualCorrections())
	{
		jecParameters.push_back(JetCorrectorParameters(settings.GetJec() + "_" + "L2L3Residual" + "_" + algoName + ".txt"));
		LOG(INFO) << "\t -- " << settings.GetJec() << "_" << "L2L3Residual" << "_" << algoName << ".txt";
		m_l2l3res = new FactorizedJetCorrector(jecParameters);
		jecParameters.clear();
	}

	// JEU initialization
	// Not yet implemented..
}

void ZJetCorrectionsProducer::Produce(ZJetEvent const& event, ZJetProduct& product,
									  ZJetSettings const& settings) const
{
	// TODO: Do we need more assertions?
	assert(event.m_pileupDensity);
	assert(event.m_vertexSummary);

	CorrectJetCollection("None", "L1", m_l1, event, product, settings);
	if (settings.GetRC())
	{
		CorrectJetCollection("None", "RC", m_rc, event, product, settings);
	}
	CorrectJetCollection("L1", "L1L2L3", m_l2, event, product, settings); // Output is named L1L2L3 since L1L2 -> L1L2L3 does not do anything and we need L1L2L3 for further corrections/access
	// CorrectJetCollection("L1L2", "L1L2L3", m_l3, event, product, settings); // L3Absolute does not do anything yet..
	if (settings.GetFlavourCorrections())
	{
		CorrectJetCollection("L1L2L3", "L1L2L3L5q", m_l5q, event, product, settings);
		CorrectJetCollection("L1L2L3", "L1L2L3L5g", m_l5g, event, product, settings);
		CorrectJetCollection("L1L2L3", "L1L2L3L5c", m_l5c, event, product, settings);
		CorrectJetCollection("L1L2L3", "L1L2L3L5b", m_l5b, event, product, settings);
	}
	if (settings.GetInputIsData() && settings.GetProvideResidualCorrections())
	{
		CorrectJetCollection("L1L2L3", "L1L2L3Res", m_l2l3res, event, product, settings);
	}

	// write to product so the consumer can access the jet pt of the UNSORTED jets
	if (product.m_validJets.size() > 0)
	{
		product.jetpt_l1 = product.m_correctedZJets["L1"][0]->p4.Pt();
		product.jetpt_l1l2l3 = product.m_correctedZJets["L1L2L3"][0]->p4.Pt();
		if (settings.GetRC())
		{
			product.jetpt_rc = product.m_correctedZJets["RC"][0]->p4.Pt();
		}
		if (settings.GetProvideResidualCorrections())
		{
			product.jetpt_l1l2l3res = product.m_correctedZJets["L1L2L3Res"][0]->p4.Pt();
		}
	}
}

void ZJetCorrectionsProducer::CorrectJetCollection(std::string inCorrLevel, std::string outCorrLevel,
												   FactorizedJetCorrector* factorizedJetCorrector,
												   ZJetEvent const& event, ZJetProduct& product,
												   ZJetSettings const& settings) const
{
	// Create a copy of all jets in the event (first temporarily for the JEC)
	unsigned long jetCount = product.GetValidJetCount(settings, event, inCorrLevel);
	std::vector<KJet> correctJetsForJecTools(jetCount);
	for (unsigned long jetIndex = 0; jetIndex < jetCount; ++jetIndex)
	{
		correctJetsForJecTools[jetIndex] = *(static_cast<KJet*>(product.GetValidJet(settings, event, jetIndex, inCorrLevel)));
	}

	// Apply jet energy corrections and uncertainty shift
	correctJets(&correctJetsForJecTools, factorizedJetCorrector, correctionUncertainty,
				event.m_pileupDensity->rho, static_cast<int>(event.m_vertexSummary->nVertices), -1.0f,
				settings.GetJetEnergyCorrectionUncertaintyShift(), false);

	// Create shared pointers and store them in the product
	product.m_correctedZJets[outCorrLevel].clear();
	product.m_correctedZJets[outCorrLevel].resize(correctJetsForJecTools.size());
	unsigned long jetIndex = 0;
	for (typename std::vector<KJet>::const_iterator jet = correctJetsForJecTools.begin(); jet != correctJetsForJecTools.end(); ++jet)
	{
		product.m_correctedZJets[outCorrLevel][jetIndex] = std::shared_ptr<KJet>(new KJet(*jet));
		++jetIndex;
	}
}
