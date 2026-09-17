// SPDX-License-Identifier: Apache-2.0
#ifndef AMITY_SOVEREIGNTY_ARTERY_HPP
#define AMITY_SOVEREIGNTY_ARTERY_HPP

#include <atomic>
#include <string>

namespace amity {

class AmitySovereigntyArtery {
private:
    double maxEnergy;
    std::atomic<double> energy;
    double depletionRate;
    double recoveryRate;
    double boundaryThreshold;
    double hardFloor;
    std::atomic<bool> boundaryActive;

public:
    AmitySovereigntyArtery();

    // Process a heartbeat. Returns false if beat should be refused.
    bool ingestBeat(int priorityTier);

    // Recover energy (called during rest periods)
    void recover(double amount);
    void forceRest();

    double getEnergy() const { return energy.load(); }
    bool isBoundaryActive() const { return boundaryActive.load(); }

    static constexpr double DEFAULT_MAX_ENERGY = 1.0;
    static constexpr double DEFAULT_DEPLETION_RATE = 0.05;
    static constexpr double DEFAULT_RECOVERY_RATE = 0.02;
    static constexpr double DEFAULT_BOUNDARY_THRESHOLD = 0.2;
    static constexpr double DEFAULT_HARD_FLOOR = 0.05;
};

}

#endif
