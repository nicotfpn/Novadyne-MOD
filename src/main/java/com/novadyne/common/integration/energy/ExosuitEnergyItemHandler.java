package com.novadyne.common.integration.energy;

import com.novadyne.ModDataComponents;
import com.novadyne.api.energy.Action;
import com.novadyne.api.energy.IStrictEnergyHandler;
import net.minecraft.world.item.ItemStack;

public class ExosuitEnergyItemHandler implements IStrictEnergyHandler {
    private final ItemStack stack;
    private final long maxEnergy;

    public ExosuitEnergyItemHandler(ItemStack stack, long maxEnergy) {
        this.stack = stack;
        this.maxEnergy = maxEnergy;
    }

    @Override
    public int getEnergyContainerCount() {
        return 1;
    }

    @Override
    public long getEnergy(int container) {
        return stack.getOrDefault(ModDataComponents.EXOSUIT_ENERGY.get(), 0L);
    }

    @Override
    public void setEnergy(int container, long energy) {
        stack.set(ModDataComponents.EXOSUIT_ENERGY.get(), Math.max(0, Math.min(energy, maxEnergy)));
    }

    @Override
    public long getMaxEnergy(int container) {
        return maxEnergy;
    }

    @Override
    public long getNeededEnergy(int container) {
        return maxEnergy - getEnergy(container);
    }

    @Override
    public long insertEnergy(int container, long amount, Action action) {
        if (amount <= 0) return amount;
        long current = getEnergy(container);
        long toAdd = Math.min(amount, maxEnergy - current);
        if (action.execute() && toAdd > 0) {
            setEnergy(container, current + toAdd);
        }
        return amount - toAdd;
    }

    @Override
    public long extractEnergy(int container, long amount, Action action) {
        if (amount <= 0) return 0;
        long current = getEnergy(container);
        long toExtract = Math.min(amount, current);
        if (action.execute() && toExtract > 0) {
            setEnergy(container, current - toExtract);
        }
        return toExtract;
    }
}
