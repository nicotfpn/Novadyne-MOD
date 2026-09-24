package com.novadyne.common.menu;

import com.novadyne.common.blockentity.AbstractMachineBlockEntity;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.inventory.AbstractContainerMenu;
import net.minecraft.world.inventory.ContainerData;
import net.minecraft.world.inventory.ContainerLevelAccess;
import net.minecraft.world.inventory.MenuType;
import net.minecraft.world.inventory.Slot;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.block.Block;

import java.util.function.Supplier;

public abstract class AbstractMachineMenu<T extends AbstractMachineBlockEntity> extends AbstractContainerMenu {
    protected final T blockEntity;
    protected final ContainerLevelAccess access;
    protected final Supplier<? extends Block> blockSupplier;
    protected final int machineSlotsCount;

    private int clientProgress;
    private int clientMaxProgress;
    private long clientEnergy;
    private long clientMaxEnergy;
    private final int[] clientItemModes = new int[6];
    private boolean clientAutoOutput;

    protected AbstractMachineMenu(MenuType<?> menuType, int containerId, Inventory playerInv, T blockEntity, ContainerLevelAccess access, Supplier<? extends Block> blockSupplier, int machineSlotsCount) {
        super(menuType, containerId);
        this.blockEntity = blockEntity;
        this.access = access;
        this.blockSupplier = blockSupplier;
        this.machineSlotsCount = machineSlotsCount;

        addMachineSlots();
        addPlayerInventorySlots(playerInv);
        setupDataSynchronization();
    }

    protected abstract void addMachineSlots();

    private void addPlayerInventorySlots(Inventory playerInv) {
        for (int row = 0; row < 3; row++) {
            for (int col = 0; col < 9; col++) {
                this.addSlot(new Slot(playerInv, col + row * 9 + 9, 9 + col * 18, 86 + row * 18));
            }
        }
        for (int col = 0; col < 9; col++) {
            this.addSlot(new Slot(playerInv, col, 9 + col * 18, 144));
        }
    }

    private void setupDataSynchronization() {
        this.addDataSlots(new ContainerData() {
            @Override
            public int get(int index) {
                return switch (index) {
                    case 0 -> blockEntity.getProgress();
                    case 1 -> blockEntity.getMaxProgress();
                    case 2 -> (int) (blockEntity.getEnergy(0) >> 32);
                    case 3 -> (int) (blockEntity.getEnergy(0) & 0xFFFFFFFFL);
                    case 4 -> (int) (blockEntity.getMaxEnergy(0) >> 32);
                    case 5 -> (int) (blockEntity.getMaxEnergy(0) & 0xFFFFFFFFL);
                    case 12 -> blockEntity.isAutoOutput() ? 1 : 0;
                    case 6, 7, 8, 9, 10, 11 -> blockEntity.getItemMode(index - 6);
                    default -> 0;
                };
            }

            @Override
            public void set(int index, int value) {
                switch (index) {
                    case 0 -> clientProgress = value;
                    case 1 -> clientMaxProgress = value;
                    case 2 -> clientEnergy = ((long) value << 32) | (clientEnergy & 0xFFFFFFFFL);
                    case 3 -> clientEnergy = (clientEnergy & 0xFFFFFFFF00000000L) | (value & 0xFFFFFFFFL);
                    case 4 -> clientMaxEnergy = ((long) value << 32) | (clientMaxEnergy & 0xFFFFFFFFL);
                    case 5 -> clientMaxEnergy = (clientMaxEnergy & 0xFFFFFFFF00000000L) | (value & 0xFFFFFFFFL);
                    case 12 -> clientAutoOutput = value != 0;
                    case 6, 7, 8, 9, 10, 11 -> clientItemModes[index - 6] = value;
                }
            }

            @Override
            public int getCount() {
                return 13;
            }
        });
    }

    public T getBlockEntity() {
        return blockEntity;
    }

    public int getProgress() {
        return blockEntity.getLevel() != null && !blockEntity.getLevel().isClientSide() ? blockEntity.getProgress() : clientProgress;
    }

    public int getMaxProgress() {
        return blockEntity.getLevel() != null && !blockEntity.getLevel().isClientSide() ? blockEntity.getMaxProgress() : clientMaxProgress;
    }

    public long getEnergy() {
        return blockEntity.getLevel() != null && !blockEntity.getLevel().isClientSide() ? blockEntity.getEnergy(0) : clientEnergy;
    }

    public long getMaxEnergy() {
        return blockEntity.getLevel() != null && !blockEntity.getLevel().isClientSide() ? blockEntity.getMaxEnergy(0) : clientMaxEnergy;
    }

    public int getItemMode(int side) {
        return blockEntity.getLevel() != null && !blockEntity.getLevel().isClientSide()
                ? blockEntity.getItemMode(side) : clientItemModes[side];
    }

    public boolean isAutoOutput() {
        return blockEntity.getLevel() != null && !blockEntity.getLevel().isClientSide()
                ? blockEntity.isAutoOutput() : clientAutoOutput;
    }

    @Override
    public boolean clickMenuButton(Player player, int id) {
        if (id < 0 || id > 6 || !stillValid(player)) return false;
        if (id == 6) blockEntity.toggleAutoOutput();
        else blockEntity.cycleItemMode(id);
        broadcastChanges();
        return true;
    }

    @Override
    public boolean stillValid(Player player) {
        return stillValid(this.access, player, blockSupplier.get());
    }

    @Override
    public ItemStack quickMoveStack(Player player, int index) {
        ItemStack itemstack = ItemStack.EMPTY;
        Slot slot = this.slots.get(index);
        if (slot != null && slot.hasItem()) {
            ItemStack stackInSlot = slot.getItem();
            itemstack = stackInSlot.copy();

            if (index < machineSlotsCount) {
                if (!this.moveItemStackTo(stackInSlot, machineSlotsCount, machineSlotsCount + 36, true)) {
                    return ItemStack.EMPTY;
                }
            } else {
                if (!moveItemToMachine(stackInSlot)) {
                    if (index < machineSlotsCount + 27) {
                        if (!this.moveItemStackTo(stackInSlot, machineSlotsCount + 27, machineSlotsCount + 36, false)) {
                            return ItemStack.EMPTY;
                        }
                    } else {
                        if (!this.moveItemStackTo(stackInSlot, machineSlotsCount, machineSlotsCount + 27, false)) {
                            return ItemStack.EMPTY;
                        }
                    }
                }
            }

            if (stackInSlot.isEmpty()) {
                slot.setByPlayer(ItemStack.EMPTY);
            } else {
                slot.setChanged();
            }

            if (stackInSlot.getCount() == itemstack.getCount()) {
                return ItemStack.EMPTY;
            }

            slot.onTake(player, stackInSlot);
        }
        return itemstack;
    }

    protected abstract boolean moveItemToMachine(ItemStack stack);
}
