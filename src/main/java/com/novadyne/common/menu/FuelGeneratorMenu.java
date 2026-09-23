package com.novadyne.common.menu;

import com.novadyne.ModBlocks;
import com.novadyne.ModMenuTypes;
import com.novadyne.common.blockentity.FuelGeneratorBlockEntity;
import net.minecraft.network.RegistryFriendlyByteBuf;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.inventory.AbstractContainerMenu;
import net.minecraft.world.inventory.ContainerData;
import net.minecraft.world.inventory.ContainerLevelAccess;
import net.minecraft.world.inventory.Slot;
import net.minecraft.world.item.ItemStack;
import net.neoforged.neoforge.transfer.item.ResourceHandlerSlot;

public class FuelGeneratorMenu extends AbstractContainerMenu {
    private final FuelGeneratorBlockEntity generator;
    private final ContainerLevelAccess access;
    private int energy, capacity, remaining, total;

    public FuelGeneratorMenu(int id, Inventory playerInventory, RegistryFriendlyByteBuf data) {
        this(id, playerInventory,
                (FuelGeneratorBlockEntity) playerInventory.player.level().getBlockEntity(data.readBlockPos()),
                ContainerLevelAccess.NULL);
    }

    public FuelGeneratorMenu(int id, Inventory playerInventory, FuelGeneratorBlockEntity generator, ContainerLevelAccess access) {
        super(ModMenuTypes.FUEL_GENERATOR.get(), id);
        this.generator = generator;
        this.access = access;
        addSlot(new ResourceHandlerSlot(generator.getInventory(), generator.getInventory()::set, 0, 56, 53));
        addSlot(new ResourceHandlerSlot(generator.getInventory(), generator.getInventory()::set, 1, 116, 35) {
            @Override public boolean mayPlace(ItemStack stack) { return false; }
        });
        for (int row = 0; row < 3; row++) {
            for (int col = 0; col < 9; col++) {
                addSlot(new Slot(playerInventory, col + row * 9 + 9, 9 + col * 18, 86 + row * 18));
            }
        }
        for (int col = 0; col < 9; col++) {
            addSlot(new Slot(playerInventory, col, 9 + col * 18, 144));
        }
        addDataSlots(new ContainerData() {
            @Override public int get(int index) {
                return switch (index) {
                    case 0 -> (int) generator.getEnergy(0);
                    case 1 -> (int) generator.getMaxEnergy(0);
                    case 2 -> generator.getBurnRemaining();
                    case 3 -> generator.getBurnTotal();
                    default -> 0;
                };
            }
            @Override public void set(int index, int value) {
                switch (index) {
                    case 0 -> energy = value;
                    case 1 -> capacity = value;
                    case 2 -> remaining = value;
                    case 3 -> total = value;
                }
            }
            @Override public int getCount() { return 4; }
        });
    }

    public int getEnergy() { return generator.getLevel().isClientSide() ? energy : (int) generator.getEnergy(0); }
    public int getCapacity() { return generator.getLevel().isClientSide() ? capacity : (int) generator.getMaxEnergy(0); }
    public int getBurnRemaining() { return generator.getLevel().isClientSide() ? remaining : generator.getBurnRemaining(); }
    public int getBurnTotal() { return generator.getLevel().isClientSide() ? total : generator.getBurnTotal(); }

    @Override public boolean stillValid(Player player) {
        return stillValid(access, player, ModBlocks.FUEL_GENERATOR.get());
    }

    @Override public ItemStack quickMoveStack(Player player, int index) {
        ItemStack result = ItemStack.EMPTY;
        Slot slot = slots.get(index);
        if (slot == null || !slot.hasItem()) return result;
        ItemStack stack = slot.getItem();
        result = stack.copy();
        if (index < 2) {
            if (!moveItemStackTo(stack, 2, 38, true)) return ItemStack.EMPTY;
        } else if (generator.isFuel(stack)) {
            if (!moveItemStackTo(stack, 0, 1, false)) return ItemStack.EMPTY;
        } else if (index < 29) {
            if (!moveItemStackTo(stack, 29, 38, false)) return ItemStack.EMPTY;
        } else if (!moveItemStackTo(stack, 2, 29, false)) return ItemStack.EMPTY;
        if (stack.isEmpty()) slot.setByPlayer(ItemStack.EMPTY);
        else slot.setChanged();
        if (stack.getCount() == result.getCount()) return ItemStack.EMPTY;
        slot.onTake(player, stack);
        return result;
    }
}
