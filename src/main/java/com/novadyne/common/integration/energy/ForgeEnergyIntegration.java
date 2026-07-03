package com.novadyne.common.integration.energy;

import com.novadyne.api.energy.Action;
import com.novadyne.api.energy.IStrictEnergyHandler;
import net.neoforged.neoforge.energy.IEnergyStorage;

@SuppressWarnings("removal")

public class ForgeEnergyIntegration implements IEnergyStorage {

    private final IStrictEnergyHandler handler;

    public ForgeEnergyIntegration(IStrictEnergyHandler handler) {
        this.handler = handler;
    }

    @Override
    public int receiveEnergy(int toReceive, boolean simulate) {
        if (!canReceive() || toReceive <= 0) {
            return 0;
        }
        long inserted = toReceive - handler.insertEnergy(toReceive, Action.fromSimulate(simulate));
        return (int) Math.min(inserted, Integer.MAX_VALUE);
    }

    @Override
    public int extractEnergy(int toExtract, boolean simulate) {
        if (!canExtract() || toExtract <= 0) {
            return 0;
        }
        long extracted = handler.extractEnergy(toExtract, Action.fromSimulate(simulate));
        return (int) Math.min(extracted, Integer.MAX_VALUE);
    }

    @Override
    public int getEnergyStored() {
        return (int) Math.min(handler.getEnergy(0), Integer.MAX_VALUE);
    }

    @Override
    public int getMaxEnergyStored() {
        return (int) Math.min(handler.getMaxEnergy(0), Integer.MAX_VALUE);
    }

    @Override
    public boolean canExtract() {
        return handler.getEnergy(0) > 0;
    }

    @Override
    public boolean canReceive() {
        return handler.getNeededEnergy(0) > 0;
    }
}
