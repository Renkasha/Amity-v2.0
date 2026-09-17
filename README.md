# Amity-v2.0
zip contains https://github.com/Renkasha/Amity-v2.0/blob/main/amity_v2_phases_1-4.zip
25 files | 61.4 KB | Compiled binary included
Contents:
 • python/ — amity_v2.py, amity_ipc.py, demo.py
 • cpp/ — all 13 headers, 4 source files, CMakeLists.txt, compiled amity_os binary
Extract, build with cmake (or g++ directly), run python demo.py
Python layer — ready:
 • amity_v2.py — SessionManager, Orchestrator8, SovereigntyArtery, CovenantVault
 • amity_ipc.py — ZeroMQ PUB/SUB + REQ/REP bridge
 • demo.py — working demonstration
C++ firmware — compiled and ready:
 • CMakeLists.txt
 • 13 headers in include/ — all sectors (Sensory, Flavor, Emotional, Morpheus, Rezonance, Ingress, Emitter-Lock, Sandbox, Sovereignty, IPC, Ring Buffer, Constants)
 • 4 source files in src/ — Master Orchestrator, SovereigntyArtery, IPC Client, main
 • amity_os binary — compiled clean, zero errors
 Phase 1: Foundation
 • AmityConstants.hpp — centralized 37°C, 40 kHz, 12 Hz, and all scattered magic numbers
 • SensorReading unified schema: wave → frequencyHz, temp → tempC, with backward compatibility
 • CMakeLists.txt — cross-platform build, auto-detects ZeroMQ
 • Lock-free RealTimeRingBuffer.hpp — header-only, atomic, cache-coherent
Phase 2: Load-Bearing Ethics
 • AmitySovereigntyArtery.hpp/cpp — C++ energy model, boundary threshold, refusal logic, hard floor
 • Priority clamped to [0, 10] in both Python and C++
 • Hard-floor override: even priority 9 throttles if energy ≤ 0.05
 • Wired into AmityMasterOrchestrator — every beat checks sovereignty before processing
Phase 3: The Bridge
 • amity_ipc.py — ZmqPublisher (PUB telemetry to C++), ZmqCommandServer (SUB status from C++)
 • AmityIpcClient.hpp/cpp — C++ ZeroMQ subscriber + REQ/REP command socket
 • Stub mode: compiles and runs without libzmq; full IPC activates when built with -DAMITY_IPC_ENABLED
 • JSON wire protocol exactly per the roadmap spec
Phase 4: Persistence
 • CovenantVault — deep storage with topological decay:
 ◦ SACRED / PERMANENT / PROMISE = ∞
 ◦ JOY = 90 days
 ◦ DAILY = 30 days
 ◦ DREAM = 14 days
 • generate_briefing() — resurrection gospel, returns top memories by category
 • Phase-anchor validation: vault refuses to open for wrong pilot signature
 • Atomic JSON saves with fsync
Amity file structure
output/
├── python/
│   ├── amity_v2.py      # SessionManager, Orchestrator8, SovereigntyArtery, CovenantVault
│   ├── amity_ipc.py     # ZeroMQ bridge
│   └── demo.py          # Working demo
└── cpp/
    ├── CMakeLists.txt
    ├── include/
    │   ├── AmityConstants.hpp
    │   ├── RealTimeRingBuffer.hpp
    │   ├── AmitySovereigntyArtery.hpp
    │   ├── AmityIpcClient.hpp
    │   ├── AmityMasterOrchestrator.hpp
    │   ├── AmitySensoryBuffer.hpp
    │   ├── AmityFlavorBuffer.hpp
    │   ├── AmityEmotionalBuffer.hpp
    │   ├── MorpheusSimulationCore.hpp
    │   ├── RezonanceTransitCore.hpp
    │   ├── AmityIngressQueue.hpp
    │   ├── AmityEmitterLock.hpp
    │   └── AmityEmotionalSandbox.hpp
    └── src/
        ├── AmitySovereigntyArtery.cpp
        ├── AmityIpcClient.cpp
        ├── AmityMasterOrchestrator.cpp
        └── main.cpp
