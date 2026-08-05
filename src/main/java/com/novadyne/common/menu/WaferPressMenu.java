package com.novadyne.common.menu;

import com.novadyne.ModBlocks;
import com.novadyne.ModMenuTypes;
import com.novadyne.common.blockentity.AbstractMachineBlockEntity;
import com.novadyne.common.blockentity.WaferPressBlockEntity;
import net.minecraft.network.RegistryFriendlyByteBuf;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.inventory.ContainerLevelAccess;
import net.minecraft.world.item.ItemStack;
import net.neoforged.neoforge.items.SlotItemHandler;

public class WaferPressMenu extends AbstractMachineMenu<WaferPressBlockEntity> {
    public WaferPressMenu(int containerId, Inventory playerInv, RegistryFriendlyByteBuf extraData) {
        this(containerId, playerInv, (WaferPressBlockEntity) playerInv.player.level().getBlockEntity(extraData.readBlockPos()), ContainerLevelAccess.NULL);
    }

    public WaferPressMenu(int containerId, Inventory playerInv, WaferPressBlockEntity blockEntity, ContainerLevelAccess access) {
        super(ModMenuTypes.WAFER_PRESS.get(), containerId, playerInv, blockEntity, access, ModBlocks.WAFER_PRESS, 3);
    }

    @Override
    protected void addMachineSlots() {
        addSlot(new SlotItemHandler(blockEntity.getInventory(), 0, 56, 17));
        addSlot(new SlotItemHandler(blockEntity.getInventory(), 1, 116, 35) {
            @Override
            public boolean mayPlace(ItemStack stack) {
                return false;
            }
        });
        addSlot(new SlotItemHandler(blockEntity.getInventory(), 2, 56, 53));
    }

    @Override
    protected boolean moveItemToMachine(ItemStack stack) {
        if (AbstractMachineBlockEntity.isValveItem(stack)) {
            if (this.moveItemStackTo(stack, 2, 3, false)) return true;
        }
        return this.moveItemStackTo(stack, 0, 1, false);
    }
}
