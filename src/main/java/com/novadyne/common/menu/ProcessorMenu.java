package com.novadyne.common.menu;

import com.novadyne.ModBlocks;
import com.novadyne.ModMenuTypes;
import com.novadyne.common.blockentity.AbstractMachineBlockEntity;
import com.novadyne.common.blockentity.ProcessorBlockEntity;
import net.minecraft.network.RegistryFriendlyByteBuf;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.inventory.ContainerLevelAccess;
import net.minecraft.world.item.ItemStack;
import net.neoforged.neoforge.items.SlotItemHandler;

public class ProcessorMenu extends AbstractMachineMenu<ProcessorBlockEntity> {
    public ProcessorMenu(int containerId, Inventory playerInv, RegistryFriendlyByteBuf extraData) {
        this(containerId, playerInv, (ProcessorBlockEntity) playerInv.player.level().getBlockEntity(extraData.readBlockPos()), ContainerLevelAccess.NULL);
    }

    public ProcessorMenu(int containerId, Inventory playerInv, ProcessorBlockEntity blockEntity, ContainerLevelAccess access) {
        super(ModMenuTypes.PROCESSOR.get(), containerId, playerInv, blockEntity, access, ModBlocks.PROCESSOR, 5);
    }

    @Override
    protected void addMachineSlots() {
        addSlot(new SlotItemHandler(blockEntity.getInventory(), 0, 44, 17));
        addSlot(new SlotItemHandler(blockEntity.getInventory(), 1, 44, 35));
        addSlot(new SlotItemHandler(blockEntity.getInventory(), 2, 44, 53));
        addSlot(new SlotItemHandler(blockEntity.getInventory(), 3, 116, 35) {
            @Override
            public boolean mayPlace(ItemStack stack) {
                return false;
            }
        });
        addSlot(new SlotItemHandler(blockEntity.getInventory(), 4, 68, 53));
    }

    @Override
    protected boolean moveItemToMachine(ItemStack stack) {
        if (AbstractMachineBlockEntity.isValveItem(stack)) {
            if (this.moveItemStackTo(stack, 4, 5, false)) return true;
        }
        return this.moveItemStackTo(stack, 0, 3, false);
    }
}
