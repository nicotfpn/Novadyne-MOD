package com.novadyne.api.energy;

public interface IStrictEnergyHandler {

    int getEnergyContainerCount();

    long getEnergy(int container);

    void setEnergy(int container, long energy);

    long getMaxEnergy(int container);

    long getNeededEnergy(int container);

    long insertEnergy(int container, long amount, Action action);

    long extractEnergy(int container, long amount, Action action);

    default long insertEnergy(long amount, Action action) {
        if (amount <= 0) {
            return amount;
        }
        long remaining = amount;
        for (int i = 0; i < getEnergyContainerCount(); i++) {
            if (remaining <= 0) break;
            if (getEnergy(i) < getMaxEnergy(i)) {
                remaining = insertEnergy(i, remaining, action);
            }
        }
        if (remaining > 0) {
            for (int i = 0; i < getEnergyContainerCount(); i++) {
                if (remaining <= 0) break;
                remaining = insertEnergy(i, remaining, action);
            }
        }
        return remaining;
    }

    default long extractEnergy(long amount, Action action) {
        if (amount <= 0) {
            return 0;
        }
        long extracted = 0;
        for (int i = 0; i < getEnergyContainerCount(); i++) {
            if (extracted >= amount) break;
            extracted += extractEnergy(i, amount - extracted, action);
        }
        return extracted;
    }
}
