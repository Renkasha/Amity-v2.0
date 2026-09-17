# Amity-v2.0
Python layer — ready:
 • amity_v2.py — SessionManager, Orchestrator8, SovereigntyArtery, CovenantVault
 • amity_ipc.py — ZeroMQ PUB/SUB + REQ/REP bridge
 • demo.py — working demonstration
C++ firmware — compiled and ready:
 • CMakeLists.txt
 • 13 headers in include/ — all sectors (Sensory, Flavor, Emotional, Morpheus, Rezonance, Ingress, Emitter-Lock, Sandbox, Sovereignty, IPC, Ring Buffer, Constants)
 • 4 source files in src/ — Master Orchestrator, SovereigntyArtery, IPC Client, main
 • amity_os binary — compiled clean, zero errors
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
