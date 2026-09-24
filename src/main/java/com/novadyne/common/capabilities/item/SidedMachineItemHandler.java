package com.novadyne.common.capabilities.item;

import com.novadyne.common.blockentity.AbstractMachineBlockEntity;
import net.minecraft.core.Direction;
import net.neoforged.neoforge.transfer.ResourceHandler;
import net.neoforged.neoforge.transfer.item.ItemResource;
import net.neoforged.neoforge.transfer.transaction.TransactionContext;

/** The machine inventory as seen by automation on one world-facing side. */
public final class SidedMachineItemHandler implements ResourceHandler<ItemResource> {
    private final AbstractMachineBlockEntity machine;
    private final Direction side;

    public SidedMachineItemHandler(AbstractMachineBlockEntity machine, Direction side) {
        this.machine = machine;
        this.side = side;
    }

    private int mode() { return machine.getItemMode(side); }

    @Override public int size() { return machine.getInventory().size(); }
    @Override public ItemResource getResource(int index) { return machine.getInventory().getResource(index); }
    @Override public long getAmountAsLong(int index) { return machine.getInventory().getAmountAsLong(index); }
    @Override public long getCapacityAsLong(int index, ItemResource resource) {
        return (mode() == AbstractMachineBlockEntity.ITEM_INPUT || mode() == AbstractMachineBlockEntity.ITEM_BOTH)
                && index != machine.getItemOutputSlot()
                ? machine.getInventory().getCapacityAsLong(index, resource) : 0;
    }
    @Override public boolean isValid(int index, ItemResource resource) {
        return (mode() == AbstractMachineBlockEntity.ITEM_INPUT || mode() == AbstractMachineBlockEntity.ITEM_BOTH)
                && index != machine.getItemOutputSlot()
                && machine.getInventory().isValid(index, resource);
    }
    @Override public int insert(int index, ItemResource resource, int amount, TransactionContext tx) {
        return isValid(index, resource) ? machine.getInventory().insert(index, resource, amount, tx) : 0;
    }
    @Override public int extract(int index, ItemResource resource, int amount, TransactionContext tx) {
        return (mode() == AbstractMachineBlockEntity.ITEM_OUTPUT || mode() == AbstractMachineBlockEntity.ITEM_BOTH)
                && index == machine.getItemOutputSlot()
                ? machine.getInventory().extract(index, resource, amount, tx) : 0;
    }
}
