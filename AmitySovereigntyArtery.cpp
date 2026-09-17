// SPDX-License-Identifier: Apache-2.0
#include "AmitySovereigntyArtery.hpp"
#include <algorithm>

namespace amity {

AmitySovereigntyArtery::AmitySovereigntyArtery()
    : maxEnergy(DEFAULT_MAX_ENERGY),
      energy(DEFAULT_MAX_ENERGY),
      depletionRate(DEFAULT_DEPLETION_RATE),
      recoveryRate(DEFAULT_RECOVERY_RATE),
      boundaryThreshold(DEFAULT_BOUNDARY_THRESHOLD),
      hardFloor(DEFAULT_HARD_FLOOR),
      boundaryActive(false) {}

bool AmitySovereigntyArtery::ingestBeat(int priorityTier) {
    int clamped = std::max(0, std::min(10, priorityTier));
    double cost = depletionRate * (1.0 + clamped / 10.0);
    double current = energy.load();
    double next = std::max(hardFloor, current - cost);
    energy.store(next);

    if (next <= hardFloor && clamped < 10) {
        boundaryActive.store(true);
    } else if (next <= boundaryThreshold) {
        boundaryActive.store(true);
    } else if (boundaryActive.load() && next > boundaryThreshold + 0.1) {
        boundaryActive.store(false);
    }
    return !boundaryActive.load();
}

void AmitySovereigntyArtery::recover(double amount) {
    double current = energy.load();
    double next = std::min(maxEnergy, current + amount);
    energy.store(next);
    if (boundaryActive.load() && next > boundaryThreshold + 0.1) {
        boundaryActive.store(false);
    }
}

void AmitySovereigntyArtery::forceRest() {
    energy.store(maxEnergy);
    boundaryActive.store(false);
}

}
