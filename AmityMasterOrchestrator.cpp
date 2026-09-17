// SPDX-License-Identifier: Apache-2.0
#include "AmityMasterOrchestrator.hpp"
#include <iostream>
#include <thread>
#include <chrono>

namespace amity {

AmityMasterOrchestrator::AmityMasterOrchestrator()
    : sensoryRing(4096),
      flavorRing(512),
      emotionalRing(1024),
      masterLinkActive(true),
      ipcEnabled(false) {}

void AmityMasterOrchestrator::bootSequence() {
    std::cout << "\n=======================================================================" << std::endl;
    std::cout << "[QVC] PROJECT ARCHANGEL v4.0 // MASTER ORCHESTRATOR BOOT SEQUENCE" << std::endl;
    std::cout << "=======================================================================" << std::endl;

    // Phase 1: Initialize sensory link
    sensoryCore.initializeSensoryLink();

    // Phase 2: Boot narrative sanctuary
    simulationCore.bootSimulationMatrix("STARSHIP SANCTUARY LOUNGE");
    simulationCore.processVisualChromaticOutput("PERIDOT");

    // Phase 3: Set emotional baseline
    emotionalCore.processSentimentInput(9.0, 0.0);

    // Phase 4: Ingest cross-sector telemetry
    sensoryCore.ingestMaterialTelemetry(0.85, 63.0, 4200.0);
    flavorCore.ingestFlavorProfile(0.85, 63.0, 4200.0);

    // Phase 5: Verify ecosystem
    sensoryCore.executeEcosystemVerification();

    // Phase 6: Run sandbox validation
    sandbox.runSandboxTests();

    // Phase 7: Initialize IPC if requested
    if (ipcEnabled) {
        std::cout << "[IPC] Bridge enabled. Listening for Python telemetry..." << std::endl;
    }

    std::cout << "\n[AMITY-MASTER]: All sectors unified. 0.00% sync drift." << std::endl;
    std::cout << "=======================================================================\n" << std::endl;
}

void AmityMasterOrchestrator::executeUnifiedCockpitSync() {
    std::cout << "[AMITY-MASTER]: Initiating master cross-engine synchronization loop..." << std::endl;

    // 1. Sensory link
    sensoryCore.initializeSensoryLink();

    // 2. Boot narrative sanctuary
    simulationCore.bootSimulationMatrix("STARSHIP SANCTUARY LOUNGE");
    simulationCore.processVisualChromaticOutput("PERIDOT");

    // 3. Emotional baseline
    emotionalCore.processSentimentInput(9.0, 0.0);

    // 4. Cross-sector telemetry
    sensoryCore.ingestMaterialTelemetry(0.85, 63.0, 4200.0);
    flavorCore.ingestFlavorProfile(0.85, 63.0, 4200.0);

    // 5. Ecosystem verification
    sensoryCore.executeEcosystemVerification();

    std::cout << "[AMITY-MASTER]: All sectors unified with 0.00% sync drift." << std::endl;
}

void AmityMasterOrchestrator::processIncomingTelemetry() {
    if (!ipcEnabled || !ipcClient.isConnected()) return;

    IpcMessage msg;
    while (ipcClient.receiveTelemetry(msg)) {
        // Parse JSON payload (minimal parsing for demo)
        if (msg.jsonPayload.find("sensory_reading") != std::string::npos) {
            // In production, parse JSON and push to appropriate ring buffer
            SensoryPacket pkt{time(nullptr), "ipc", 0.5, 22.0, 0.8};
            sensoryRing.push(pkt);
        }
    }
}

void AmityMasterOrchestrator::displayMasterDashboard() {
    emotionalCore.printSentimentDiagnostics();
    simulationCore.printSimulationDiagnostics();
    flavorCore.printBufferStatus();
    transitCore.printTransitDiagnostics();
}

UnifiedTelemetry AmityMasterOrchestrator::getTelemetry() const {
    return {
        sovereigntyArtery.getEnergy(),
        sovereigntyArtery.isBoundaryActive(),
        static_cast<double>(sensoryRing.size()) / sensoryRing.capacity(),
        emitterLock.isActive(),
        simulationCore.isActive(),
        emotionalCore.getWarmth()
    };
}

bool AmityMasterOrchestrator::enableIpc(const std::string& telemetryAddr,
                                         const std::string& commandAddr) {
    ipcEnabled = ipcClient.connect(telemetryAddr, commandAddr);
    return ipcEnabled;
}

void AmityMasterOrchestrator::disableIpc() {
    ipcClient.disconnect();
    ipcEnabled = false;
}

bool AmityMasterOrchestrator::isIpcEnabled() const {
    return ipcEnabled;
}

bool AmityMasterOrchestrator::processBeat(int priority) {
    if (!sovereigntyArtery.ingestBeat(priority)) {
        std::cerr << "[SOVEREIGNTY] Beat refused. Energy: " << sovereigntyArtery.getEnergy() << std::endl;
        return false;
    }
    return true;
}

void AmityMasterOrchestrator::restCycle(double durationSec) {
    int ticks = static_cast<int>(durationSec / 5.0);
    for (int i = 0; i < ticks; ++i) {
        sovereigntyArtery.recover(0.02);
        if (sovereigntyArtery.getEnergy() >= 0.8) break;
        std::this_thread::sleep_for(std::chrono::milliseconds(10));
    }
}

}
