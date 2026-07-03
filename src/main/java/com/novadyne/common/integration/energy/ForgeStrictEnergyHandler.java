package com.novadyne.common.integration.energy;

import com.novadyne.api.energy.Action;
import com.novadyne.api.energy.IStrictEnergyHandler;
import net.neoforged.neoforge.energy.IEnergyStorage;

@SuppressWarnings("removal")

public class ForgeStrictEnergyHandler implements IStrictEnergyHandler {

    private final IEnergyStorage storage;

    public ForgeStrictEnergyHandler(IEnergyStorage storage) {
        this.storage = storage;
    }

    @Override
    public int getEnergyContainerCount() {
        return 1;
    }

    @Override
    public long getEnergy(int container) {
        return container == 0 ? storage.getEnergyStored() : 0L;
    }

    @Override
    public void setEnergy(int container, long energy) {
    }

    @Override
    public long getMaxEnergy(int container) {
        return container == 0 ? storage.getMaxEnergyStored() : 0L;
    }

    @Override
    public long getNeededEnergy(int container) {
        return container == 0 ? Math.max(0, storage.getMaxEnergyStored() - storage.getEnergyStored()) : 0L;
    }

    @Override
    public long insertEnergy(int container, long amount, Action action) {
        if (container != 0 || amount <= 0) {
            return amount;
        }
        int toInsert = (int) Math.min(amount, Integer.MAX_VALUE);
        int inserted = storage.receiveEnergy(toInsert, action.simulate());
        return amount - inserted;
    }

    @Override
    public long insertEnergy(long amount, Action action) {
        if (!storage.canReceive() || amount <= 0) {
            return amount;
        }
        int toInsert = (int) Math.min(amount, Integer.MAX_VALUE);
        int inserted = storage.receiveEnergy(toInsert, action.simulate());
        return amount - inserted;
    }

    @Override
    public long extractEnergy(int container, long amount, Action action) {
        if (container != 0 || amount <= 0) {
            return 0L;
        }
        int toExtract = (int) Math.min(amount, Integer.MAX_VALUE);
        return storage.extractEnergy(toExtract, action.simulate());
    }

    @Override
    public long extractEnergy(long amount, Action action) {
        if (!storage.canExtract() || amount <= 0) {
            return 0L;
        }
        int toExtract = (int) Math.min(amount, Integer.MAX_VALUE);
        return storage.extractEnergy(toExtract, action.simulate());
    }
}
