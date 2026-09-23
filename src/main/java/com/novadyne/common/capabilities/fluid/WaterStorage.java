package com.novadyne.common.capabilities.fluid;

import java.util.Objects;
import net.minecraft.world.level.material.Fluids;
import net.neoforged.neoforge.transfer.TransferPreconditions;
import net.neoforged.neoforge.transfer.fluid.FluidResource;
import net.neoforged.neoforge.transfer.ResourceHandler;
import net.neoforged.neoforge.transfer.transaction.SnapshotJournal;
import net.neoforged.neoforge.transfer.transaction.TransactionContext;

/** A single water tank. External consumers may fill it, but cannot drain it. */
public final class WaterStorage extends SnapshotJournal<Integer> implements ResourceHandler<FluidResource> {
    private static final FluidResource WATER = FluidResource.of(Fluids.WATER);
    private final int capacity;
    private final Runnable changed;
    private int amount;

    public WaterStorage(int capacity, Runnable changed) {
        this.capacity = capacity;
        this.changed = changed;
    }

    public int amount() { return amount; }

    public void setAmount(int value) {
        int clamped = Math.max(0, Math.min(capacity, value));
        if (amount != clamped) {
            amount = clamped;
            changed.run();
        }
    }

    public boolean consume(int value) {
        if (value < 0 || amount < value) return false;
        setAmount(amount - value);
        return true;
    }

    @Override public int size() { return 1; }
    @Override public FluidResource getResource(int index) {
        Objects.checkIndex(index, 1);
        return amount == 0 ? FluidResource.EMPTY : WATER;
    }
    @Override public long getAmountAsLong(int index) {
        Objects.checkIndex(index, 1);
        return amount;
    }
    @Override public long getCapacityAsLong(int index, FluidResource resource) {
        Objects.checkIndex(index, 1);
        return capacity;
    }
    @Override public boolean isValid(int index, FluidResource resource) {
        Objects.checkIndex(index, 1);
        return WATER.equals(resource);
    }
    @Override public int insert(int index, FluidResource resource, int value, TransactionContext tx) {
        Objects.checkIndex(index, 1);
        TransferPreconditions.checkNonEmptyNonNegative(resource, value);
        if (!isValid(index, resource)) return 0;
        int inserted = Math.min(value, capacity - amount);
        if (inserted > 0) {
            updateSnapshots(tx);
            amount += inserted;
        }
        return inserted;
    }
    @Override public int extract(int index, FluidResource resource, int value, TransactionContext tx) {
        Objects.checkIndex(index, 1);
        TransferPreconditions.checkNonEmptyNonNegative(resource, value);
        return 0;
    }
    @Override protected Integer createSnapshot() { return amount; }
    @Override protected void revertToSnapshot(Integer snapshot) { amount = snapshot; }
    @Override protected void onRootCommit(Integer snapshot) { if (amount != snapshot) changed.run(); }
}
