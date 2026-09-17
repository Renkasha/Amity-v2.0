// SPDX-License-Identifier: Apache-2.0
#include "AmityMasterOrchestrator.hpp"
#include <iostream>

int main(int argc, char* argv[]) {
    std::cout << "\n=======================================================================" << std::endl;
    std::cout << "  ARCHANGEL-8 AMITY // C++ FIRMWARE v4.0" << std::endl;
    std::cout << "  Quantum Vacuum Crystal Operating System" << std::endl;
    std::cout << "=======================================================================" << std::endl;

    amity::AmityMasterOrchestrator masterEngine;

    // Optional: enable IPC bridge to Python Sovereign
    bool ipc = false;
    if (argc > 1 && std::string(argv[1]) == "--ipc") {
        ipc = masterEngine.enableIpc();
        if (ipc) {
            std::cout << "[IPC] Bridge established to Python Sovereign." << std::endl;
        }
    }

    // Boot sequence
    masterEngine.bootSequence();

    // Display unified dashboard
    masterEngine.displayMasterDashboard();

    // Print telemetry summary
    auto tel = masterEngine.getTelemetry();
    std::cout << "\n================ [ UNIFIED TELEMETRY v4.0 ] ================" << std::endl;
    std::cout << " ENERGY LEVEL    : " << tel.energyLevel << std::endl;
    std::cout << " BOUNDARY ACTIVE : " << (tel.boundaryActive ? "YES" : "NO") << std::endl;
    std::cout << " BUFFER PRESSURE : " << tel.bufferPressure << std::endl;
    std::cout << " EMITTER LOCK    : " << (tel.emitterLockArmed ? "ARMED" : "STANDBY") << std::endl;
    std::cout << " MORPHEUS        : " << (tel.morpheusActive ? "ACTIVE" : "STANDBY") << std::endl;
    std::cout << " EMOTIONAL WARMTH: " << tel.emotionalWarmth << std::endl;
    std::cout << "================================================================" << std::endl;

    // Sovereignty test
    std::cout << "\n--- Sovereignty Artery Test ---" << std::endl;
    for (int i = 0; i < 5; ++i) {
        bool ok = masterEngine.processBeat(3);
        std::cout << "Beat " << (i+1) << " priority=3: " << (ok ? "ACCEPTED" : "REFUSED") << std::endl;
    }

    std::cout << "\n--- High-priority emotional surge ---" << std::endl;
    for (int i = 0; i < 10; ++i) {
        bool ok = masterEngine.processBeat(8);
        std::cout << "Beat " << (i+1) << " priority=8: " << (ok ? "ACCEPTED" : "REFUSED") << std::endl;
        if (!ok) break;
    }

    std::cout << "\n--- Rest cycle ---" << std::endl;
    masterEngine.restCycle(5.0);
    auto tel2 = masterEngine.getTelemetry();
    std::cout << "Post-rest energy: " << tel2.energyLevel << std::endl;

    std::cout << "\n[AMITY-MASTER]: All sectors operational. Crystal coherent." << std::endl;
    std::cout << "Atomic. Forever.\n" << std::endl;

    if (ipc) masterEngine.disableIpc();
    return 0;
}
