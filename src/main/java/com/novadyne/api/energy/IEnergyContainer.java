package com.novadyne.api.energy;

import com.novadyne.common.util.SerializationConstants;
import net.minecraft.core.HolderLookup;
import net.minecraft.nbt.CompoundTag;
import org.jetbrains.annotations.Range;

public interface IEnergyContainer extends IContentsListener {

    @Range(from = 0, to = Long.MAX_VALUE)
    long getEnergy();

    void setEnergy(@Range(from = 0, to = Long.MAX_VALUE) long energy);

    @Range(from = 0, to = Long.MAX_VALUE)
    default long insert(@Range(from = 0, to = Long.MAX_VALUE) long amount, Action action, AutomationType automationType) {
        if (amount <= 0) {
            return amount;
        }
        long needed = getNeeded();
        if (needed == 0) {
            return amount;
        }
        long toAdd = Math.min(amount, needed);
        if (action.execute()) {
            setEnergy(getEnergy() + toAdd);
        }
        return amount - toAdd;
    }

    @Range(from = 0, to = Long.MAX_VALUE)
    default long extract(@Range(from = 0, to = Long.MAX_VALUE) long amount, Action action, AutomationType automationType) {
        if (isEmpty() || amount <= 0) {
            return 0;
        }
        long ret = Math.min(getEnergy(), amount);
        if (ret > 0 && action.execute()) {
            setEnergy(getEnergy() - ret);
        }
        return ret;
    }

    long getMaxEnergy();

    default boolean isEmpty() {
        return getEnergy() == 0L;
    }

    default void setEmpty() {
        setEnergy(0L);
    }

    @Range(from = 0, to = Long.MAX_VALUE)
    default long getNeeded() {
        return getMaxEnergy() - getEnergy();
    }

    default CompoundTag serializeNBT(HolderLookup.Provider provider) {
        CompoundTag nbt = new CompoundTag();
        if (!isEmpty()) {
            nbt.putLong(SerializationConstants.STORED, getEnergy());
        }
        return nbt;
    }

    void deserializeNBT(HolderLookup.Provider provider, CompoundTag nbt);
}
