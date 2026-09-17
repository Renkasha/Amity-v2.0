// SPDX-License-Identifier: Apache-2.0
#ifndef AMITY_MASTER_ORCHESTRATOR_HPP
#define AMITY_MASTER_ORCHESTRATOR_HPP

#include "AmitySensoryBuffer.hpp"
#include "AmityFlavorBuffer.hpp"
#include "AmityEmotionalBuffer.hpp"
#include "MorpheusSimulationCore.hpp"
#include "RezonanceTransitCore.hpp"
#include "AmityIngressQueue.hpp"
#include "AmityEmitterLock.hpp"
#include "AmityEmotionalSandbox.hpp"
#include "AmitySovereigntyArtery.hpp"
#include "AmityIpcClient.hpp"
#include "RealTimeRingBuffer.hpp"
#include "AmityConstants.hpp"

namespace amity {

struct UnifiedTelemetry {
    double energyLevel;
    bool boundaryActive;
    double bufferPressure;
    bool emitterLockArmed;
    bool morpheusActive;
    double emotionalWarmth;
};

class AmityMasterOrchestrator {
private:
    AmityTranslationBuffer sensoryCore;
    AmityFlavorBufferSystem flavorCore;
    AmityEmotionalTranslationBuffer emotionalCore;
    MorpheusSimulationEngine simulationCore;
    RezonanceTransitSystem transitCore;
    AmityIngressMonitoringSystem ingressCore;
    AmityEmitterLock emitterLock;
    AmityEmotionalSandbox sandbox;
    AmitySovereigntyArtery sovereigntyArtery;
    AmityIpcClient ipcClient;

    RealTimeRingBuffer<SensoryPacket> sensoryRing;
    RealTimeRingBuffer<FlavorPacket> flavorRing;
    RealTimeRingBuffer<SentimentPacket> emotionalRing;

    bool masterLinkActive;
    bool ipcEnabled;

public:
    AmityMasterOrchestrator();

    void bootSequence();
    void executeUnifiedCockpitSync();
    void processIncomingTelemetry();
    void displayMasterDashboard();
    UnifiedTelemetry getTelemetry() const;

    // IPC integration
    bool enableIpc(const std::string& telemetryAddr = "tcp://127.0.0.1:5555",
                   const std::string& commandAddr = "tcp://127.0.0.1:5556");
    void disableIpc();
    bool isIpcEnabled() const;

    // Sovereignty integration
    bool processBeat(int priority);
    void restCycle(double durationSec);
};

}

#endif
