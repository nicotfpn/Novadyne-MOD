package com.novadyne.common.capabilities.energy;

import java.util.function.Predicate;
import com.novadyne.api.energy.AutomationType;
import com.novadyne.api.energy.IContentsListener;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

public class MachineEnergyContainer<MACHINE> extends BasicEnergyContainer {

    public static <MACHINE> MachineEnergyContainer<MACHINE> input(MACHINE machine, long maxEnergy, long energyPerTick,
          @Nullable IContentsListener listener) {
        return new MachineEnergyContainer<>(maxEnergy, energyPerTick, notExternal, alwaysTrue, machine, listener);
    }

    public static <MACHINE> MachineEnergyContainer<MACHINE> internal(MACHINE machine, long maxEnergy, long energyPerTick,
          @Nullable IContentsListener listener) {
        return new MachineEnergyContainer<>(maxEnergy, energyPerTick, internalOnly, internalOnly, machine, listener);
    }

    protected final MACHINE machine;
    private final long baseEnergyPerTick;
    private long currentMaxEnergy;
    protected long currentEnergyPerTick;

    protected MachineEnergyContainer(long maxEnergy, long energyPerTick, Predicate<@NotNull AutomationType> canExtract,
          Predicate<@NotNull AutomationType> canInsert, MACHINE machine, @Nullable IContentsListener listener) {
        super(maxEnergy, canExtract, canInsert, listener);
        this.baseEnergyPerTick = energyPerTick;
        this.machine = machine;
        currentMaxEnergy = getBaseMaxEnergy();
        currentEnergyPerTick = baseEnergyPerTick;
    }

    public boolean adjustableRates() {
        return false;
    }

    @Override
    public long getMaxEnergy() {
        return currentMaxEnergy;
    }

    public long getBaseMaxEnergy() {
        return super.getMaxEnergy();
    }

    public void setMaxEnergy(long maxEnergy) {
        this.currentMaxEnergy = maxEnergy;
        setEnergy(getEnergy());
    }

    public long getEnergyPerTick() {
        return currentEnergyPerTick;
    }

    public long getBaseEnergyPerTick() {
        return baseEnergyPerTick;
    }

    public void setEnergyPerTick(long energyPerTick) {
        this.currentEnergyPerTick = energyPerTick;
    }
}
