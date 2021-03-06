/* Copyright (c) 2014 - All Rights Reserved
 *   Dominik Haitz <dhaitz@cern.ch>
 */

#pragma once

#include "Artus/Core/interface/ProducerBase.h"
#include "Artus/Core/interface/Pipeline.h"
#include "Artus/Core/interface/PipelineRunner.h"


#include "Excalibur/Compile/interface/ZJetSettings.h"
#include "Excalibur/Compile/interface/ZJetEvent.h"
#include "Excalibur/Compile/interface/ZJetProduct.h"

// all data types which are used for this analysis
struct ZJetTypes {
    typedef ZJetEvent event_type;
    typedef ZJetProduct product_type;
    typedef ZJetSettings setting_type;
};

// Pass the template parameters for the Producers
typedef ProducerBase<ZJetTypes> ZJetProducerBase;

// Pass the template parameters for the Consumer
typedef ConsumerBase<ZJetTypes> ZJetConsumerBase;

// Pass the template parameters for the Filter
typedef FilterBase<ZJetTypes> ZJetFilterBase;

// Pass the template parameters for the Pipeline
typedef Pipeline<ZJetTypes> ZJetPipeline;

// Setup our custom pipeline runner and initializer
typedef PipelineRunner<ZJetPipeline, ZJetTypes> ZJetPipelineRunner;
typedef PipelineInitilizerBase<ZJetTypes> ZJetPipelineInitializer;
