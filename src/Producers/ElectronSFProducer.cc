#include "ElectronSFProducer.h"

#include <boost/algorithm/string.hpp>
#include "TH2.h"

/*
taken from https://twiki.cern.ch/twiki/bin/view/Main/EGammaScaleFactors2012

This producer contains some un-intuitive programming constructs, which are
necessary to account for the different formats of the ROOT files containing
the scale factors (different axes, binning in absolute eta)

needed tags:
- ElectronSFRootfilePath   Path for the root files
- ElectronSFVariation      Vary SF by error. Choices: up, down, None


maybe also relevant:
https://twiki.cern.ch/twiki/bin/viewauth/CMS/MultivariateElectronIdentification (SF files for MVA
ID)
https://twiki.cern.ch/twiki/bin/view/CMSPublic/DiLeptonAnalysis#Efficiencies_and_Scale_Factors
https://twiki.cern.ch/twiki/bin/viewauth/CMS/DileptonTriggerResults
http://lovedeep.web.cern.ch/lovedeep/WORK13/TnPRun2012ReReco_2013Oct28/effiPlots.html
*/

std::string ElectronSFProducer::GetProducerId() const { return "ElectronSFProducer"; }

void ElectronSFProducer::Init(ZJetSettings const& settings)
{
    // this is only the path, add filename according to ID
    m_sffile = settings.GetElectronSFRootfilePath() + "/Electron-";
    m_id = settings.GetElectronID();

    std::string histoname;  // histoname depending on id

    double error_multiplier = 0.;
    if (settings.GetElectronSFVariation() == "up") {
        LOG(WARNING) << "ElectronSFProducer: varying scale factor UP one sigma";
        error_multiplier = 1.;
    } else if (settings.GetElectronSFVariation() == "down") {
        LOG(WARNING) << "ElectronSFProducer: varying scale factor DOWN one sigma";
        error_multiplier = -1.;
    }

    // pt/eta axes are different for mva/cutbased
    // cutbased id has binning in absolute eta
    if (m_id == "mvanontrig") {
        histoname = "h_electronScaleFactor_IdIsoSip";
        m_etabins = &m_ybins;
        m_ptbins = &m_xbins;
        m_reversed_axes = true;
        m_absoluteeta = false;
        m_sffile = m_sffile += "NontrigMVAId";
    } else if (m_id == "mvatrig") {
        // TODO(dhaitz)
        LOG(FATAL) << "No scale factors for ID " << m_id << " available!";
    } else if ((m_id == "loose") || (m_id == "medium") || (m_id == "tight") || (m_id == "veto")) {
        histoname = ("sf" + boost::to_upper_copy(m_id));
        m_etabins = &m_xbins;
        m_ptbins = &m_ybins;
        m_reversed_axes = false;
        m_absoluteeta = true;
        m_sffile = m_sffile += "CutBasedID";
    } else if ((m_id == "vbft95_loose") || (m_id == "vbft95_medium") || (m_id == "vbft95_tight") ||
               (m_id == "vbft95_veto")) {
        histoname = (m_id);
        m_etabins = &m_ybins;
        m_ptbins = &m_xbins;
        m_reversed_axes = true;
        m_absoluteeta = true;
        if (settings.GetInputIsData())
            m_sffile = m_sffile += "Data";
        else
            m_sffile = m_sffile += "MC";
    } else {
        LOG(FATAL) << "No scale factors for ID " << m_id << " available!";
    }
    m_sffile = m_sffile += "ScaleFactors.root";

    // Get file
    LOG(INFO) << "Loading electron scale factors for ID " << m_id << ": File " << m_sffile
              << ", Histogram " << histoname;
    TFile file(m_sffile.c_str(), "READONLY");
    TH2F* sfhisto = (TH2F*)file.Get(histoname.c_str());

    // Get the pT and eta bin borders
    for (int iy = 0; iy <= sfhisto->GetNbinsY(); ++iy)
        m_ybins.emplace_back(2 * sfhisto->GetYaxis()->GetBinCenter(iy) -
                             sfhisto->GetYaxis()->GetBinLowEdge(iy));
    for (int ix = 0; ix <= sfhisto->GetNbinsX(); ++ix)
        m_xbins.emplace_back(2 * sfhisto->GetXaxis()->GetBinCenter(ix) -
                             sfhisto->GetXaxis()->GetBinLowEdge(ix));

    // Fill the m_sf array with the values from the root histo
    for (int iy = 1; iy <= sfhisto->GetNbinsY(); iy++) {
        for (int ix = 1; ix <= sfhisto->GetNbinsX(); ix++) {
            m_sf[ix - 1][iy - 1] = static_cast<float>(
                sfhisto->GetBinContent(ix, iy) + error_multiplier * sfhisto->GetBinError(ix, iy));
        }
    }
    delete sfhisto;
    file.Close();
}

void ElectronSFProducer::Produce(ZJetEvent const& event,
                                 ZJetProduct& product,
                                 ZJetSettings const& settings) const
{
    product.m_weights["electronSFWeight"] =
        GetScaleFactor(*product.m_zLeptons.first) * GetScaleFactor(*product.m_zLeptons.second);
}
