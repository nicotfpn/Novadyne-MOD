package com.novadyne.common.capabilities.energy;

import java.util.Objects;
import java.util.function.Predicate;
import com.novadyne.api.energy.Action;
import com.novadyne.api.energy.AutomationType;
import com.novadyne.api.energy.IContentsListener;
import com.novadyne.api.energy.IEnergyContainer;
import com.novadyne.common.util.NBTUtils;
import com.novadyne.common.util.SerializationConstants;
import net.minecraft.core.HolderLookup;
import net.minecraft.nbt.CompoundTag;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

public class BasicEnergyContainer implements IEnergyContainer {

    public static final Predicate<@NotNull AutomationType> alwaysTrue = a -> true;
    public static final Predicate<@NotNull AutomationType> internalOnly = a -> a == AutomationType.INTERNAL;
    public static final Predicate<@NotNull AutomationType> manualOnly = a -> a == AutomationType.MANUAL;
    public static final Predicate<@NotNull AutomationType> notExternal = a -> a != AutomationType.EXTERNAL;

    public static BasicEnergyContainer create(long maxEnergy, @Nullable IContentsListener listener) {
        return new BasicEnergyContainer(maxEnergy, alwaysTrue, alwaysTrue, listener);
    }

    public static BasicEnergyContainer input(long maxEnergy, @Nullable IContentsListener listener) {
        return new BasicEnergyContainer(maxEnergy, notExternal, alwaysTrue, listener);
    }

    public static BasicEnergyContainer output(long maxEnergy, @Nullable IContentsListener listener) {
        return new BasicEnergyContainer(maxEnergy, alwaysTrue, internalOnly, listener);
    }

    public static BasicEnergyContainer create(long maxEnergy, Predicate<@NotNull AutomationType> canExtract,
          Predicate<@NotNull AutomationType> canInsert, @Nullable IContentsListener listener) {
        Objects.requireNonNull(canExtract, "Extraction validity check cannot be null");
        Objects.requireNonNull(canInsert, "Insertion validity check cannot be null");
        return new BasicEnergyContainer(maxEnergy, canExtract, canInsert, listener);
    }

    private long stored = 0L;
    protected final Predicate<@NotNull AutomationType> canExtract;
    protected final Predicate<@NotNull AutomationType> canInsert;
    private final long maxEnergy;
    @Nullable
    private final IContentsListener listener;

    protected BasicEnergyContainer(long maxEnergy, Predicate<@NotNull AutomationType> canExtract,
          Predicate<@NotNull AutomationType> canInsert, @Nullable IContentsListener listener) {
        this.maxEnergy = maxEnergy;
        this.canExtract = canExtract;
        this.canInsert = canInsert;
        this.listener = listener;
    }

    @Override
    public void onContentsChanged() {
        if (listener != null) {
            listener.onContentsChanged();
        }
    }

    @Override
    public long getEnergy() {
        return stored;
    }

    protected long clampEnergy(long energy) {
        return Math.min(energy, getMaxEnergy());
    }

    @Override
    public void setEnergy(long energy) {
        if (energy < 0) {
            throw new IllegalArgumentException("Energy cannot be negative");
        }
        energy = clampEnergy(energy);
        if (stored != energy) {
            stored = energy;
            onContentsChanged();
        }
    }

    protected long getInsertRate(@Nullable AutomationType automationType) {
        return Long.MAX_VALUE;
    }

    protected long getExtractRate(@Nullable AutomationType automationType) {
        return Long.MAX_VALUE;
    }

    @Override
    public long insert(long amount, Action action, AutomationType automationType) {
        if (amount <= 0L || !canInsert.test(automationType)) {
            return amount;
        }
        long needed = Math.min(getInsertRate(automationType), getNeeded());
        if (needed == 0L) {
            return amount;
        }
        long toAdd = Math.min(amount, needed);
        if (action.execute()) {
            stored += toAdd;
            onContentsChanged();
        }
        return amount - toAdd;
    }

    @Override
    public long extract(long amount, Action action, AutomationType automationType) {
        if (isEmpty() || amount <= 0L || !canExtract.test(automationType)) {
            return 0L;
        }
        long ret = Math.min(Math.min(getExtractRate(automationType), getEnergy()), amount);
        if (ret > 0L && action.execute()) {
            stored -= ret;
            onContentsChanged();
        }
        return ret;
    }

    @Override
    public boolean isEmpty() {
        return stored == 0L;
    }

    @Override
    public long getMaxEnergy() {
        return maxEnergy;
    }

    @Override
    public CompoundTag serializeNBT(HolderLookup.Provider provider) {
        CompoundTag nbt = new CompoundTag();
        if (!isEmpty()) {
            nbt.putLong(SerializationConstants.STORED, stored);
        }
        return nbt;
    }

    @Override
    public void deserializeNBT(HolderLookup.Provider provider, CompoundTag nbt) {
        NBTUtils.setLegacyEnergyIfPresent(nbt, SerializationConstants.STORED, this::setEnergy);
    }
}
