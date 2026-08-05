package com.novadyne.common.menu;

import com.novadyne.ModBlocks;
import com.novadyne.ModMenuTypes;
import com.novadyne.common.blockentity.AbstractMachineBlockEntity;
import com.novadyne.common.blockentity.MaceratorBlockEntity;
import net.minecraft.network.RegistryFriendlyByteBuf;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.inventory.ContainerLevelAccess;
import net.minecraft.world.item.ItemStack;
import net.neoforged.neoforge.transfer.item.ResourceHandlerSlot;

public class MaceratorMenu extends AbstractMachineMenu<MaceratorBlockEntity> {
    public MaceratorMenu(int containerId, Inventory playerInv, RegistryFriendlyByteBuf extraData) {
        this(containerId, playerInv, (MaceratorBlockEntity) playerInv.player.level().getBlockEntity(extraData.readBlockPos()), ContainerLevelAccess.NULL);
    }

    public MaceratorMenu(int containerId, Inventory playerInv, MaceratorBlockEntity blockEntity, ContainerLevelAccess access) {
        super(ModMenuTypes.MACERATOR.get(), containerId, playerInv, blockEntity, access, ModBlocks.MACERATOR, 3);
    }

    @Override
    protected void addMachineSlots() {
        addSlot(new ResourceHandlerSlot(blockEntity.getInventory(), blockEntity.getInventory()::set, 0, 56, 17));
        addSlot(new ResourceHandlerSlot(blockEntity.getInventory(), blockEntity.getInventory()::set, 1, 116, 35) {
            @Override
            public boolean mayPlace(ItemStack stack) {
                return false;
            }
        });
        addSlot(new ResourceHandlerSlot(blockEntity.getInventory(), blockEntity.getInventory()::set, 2, 56, 53));
    }

    @Override
    protected boolean moveItemToMachine(ItemStack stack) {
        if (AbstractMachineBlockEntity.isValveItem(stack)) {
            if (this.moveItemStackTo(stack, 2, 3, false)) return true;
        }
        return this.moveItemStackTo(stack, 0, 1, false);
    }
}
