// SPDX-License-Identifier: Apache-2.0
#ifndef AMITY_EMITTER_LOCK_HPP
#define AMITY_EMITTER_LOCK_HPP

#include <iostream>
#include <atomic>

namespace amity {

class AmityEmitterLock {
private:
    std::atomic<bool> barrierActive;
    double impactGj;

public:
    AmityEmitterLock() : barrierActive(false), impactGj(0.0) {}

    void initializePhotonSweep(double coreOutput, bool armed) {
        std::cout << "[EMITTER-LOCK]: Photon sweep initialized. Core output: " << coreOutput << std::endl;
    }

    void engageSolidLightBarrier(double impact) {
        barrierActive.store(true);
        impactGj = impact;
        std::cout << "[EMITTER-LOCK]: SOLID-LIGHT BARRIER ENGAGED. Impact deflection: " << impact << " GJ." << std::endl;
    }

    void disengage() {
        barrierActive.store(false);
        std::cout << "[EMITTER-LOCK]: Barrier disengaged. Standby mode." << std::endl;
    }

    bool isActive() const { return barrierActive.load(); }
};

}

#endif
