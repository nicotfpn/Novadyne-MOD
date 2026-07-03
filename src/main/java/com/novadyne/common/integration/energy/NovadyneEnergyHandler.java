package com.novadyne.common.integration.energy;

import com.novadyne.api.energy.Action;
import com.novadyne.api.energy.IStrictEnergyHandler;
import net.neoforged.neoforge.transfer.TransferPreconditions;
import net.neoforged.neoforge.transfer.energy.EnergyHandler;
import net.neoforged.neoforge.transfer.transaction.SnapshotJournal;
import net.neoforged.neoforge.transfer.transaction.TransactionContext;

public class NovadyneEnergyHandler implements EnergyHandler {

    private final IStrictEnergyHandler handler;
    private final int container;

    private final EnergyJournal journal = new EnergyJournal();

    public NovadyneEnergyHandler(IStrictEnergyHandler handler, int container) {
        this.handler = handler;
        this.container = container;
    }

    public NovadyneEnergyHandler(IStrictEnergyHandler handler) {
        this(handler, 0);
    }

    @Override
    public long getAmountAsLong() {
        return handler.getEnergy(container);
    }

    @Override
    public long getCapacityAsLong() {
        return handler.getMaxEnergy(container);
    }

    @Override
    public int insert(int amount, TransactionContext transaction) {
        TransferPreconditions.checkNonNegative(amount);

        long current = handler.getEnergy(container);
        long max = handler.getMaxEnergy(container);
        long toInsert = Math.min(amount, max - current);

        if (toInsert <= 0) {
            return 0;
        }

        journal.updateSnapshots(transaction);
        long remainder = handler.insertEnergy(container, toInsert, Action.EXECUTE);
        long inserted = toInsert - remainder;
        return (int) inserted;
    }

    @Override
    public int extract(int amount, TransactionContext transaction) {
        TransferPreconditions.checkNonNegative(amount);

        long current = handler.getEnergy(container);
        if (current <= 0) {
            return 0;
        }

        long toExtract = Math.min(amount, current);
        if (toExtract <= 0) {
            return 0;
        }

        journal.updateSnapshots(transaction);
        long extracted = handler.extractEnergy(container, toExtract, Action.EXECUTE);
        return (int) extracted;
    }

    private class EnergyJournal extends SnapshotJournal<long[]> {
        @Override
        protected long[] createSnapshot() {
            return new long[] { handler.getEnergy(container), handler.getMaxEnergy(container) };
        }

        @Override
        protected void revertToSnapshot(long[] snapshot) {
            handler.setEnergy(container, snapshot[0]);
        }

        @Override
        protected void onRootCommit(long[] originalState) {
        }
    }
}
