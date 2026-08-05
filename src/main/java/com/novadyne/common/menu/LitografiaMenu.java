package com.novadyne.common.menu;

import com.novadyne.ModBlocks;
import com.novadyne.ModMenuTypes;
import com.novadyne.common.blockentity.AbstractMachineBlockEntity;
import com.novadyne.common.blockentity.LitografiaBlockEntity;
import net.minecraft.network.RegistryFriendlyByteBuf;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.inventory.ContainerLevelAccess;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.neoforged.neoforge.items.SlotItemHandler;

public class LitografiaMenu extends AbstractMachineMenu<LitografiaBlockEntity> {
    public LitografiaMenu(int containerId, Inventory playerInv, RegistryFriendlyByteBuf extraData) {
        this(containerId, playerInv, (LitografiaBlockEntity) playerInv.player.level().getBlockEntity(extraData.readBlockPos()), ContainerLevelAccess.NULL);
    }

    public LitografiaMenu(int containerId, Inventory playerInv, LitografiaBlockEntity blockEntity, ContainerLevelAccess access) {
        super(ModMenuTypes.LITOGRAFIA.get(), containerId, playerInv, blockEntity, access, ModBlocks.LITOGRAFIA, 4);
    }

    @Override
    protected void addMachineSlots() {
        addSlot(new SlotItemHandler(blockEntity.getInventory(), 0, 56, 17));
        addSlot(new SlotItemHandler(blockEntity.getInventory(), 1, 56, 53));
        addSlot(new SlotItemHandler(blockEntity.getInventory(), 2, 38, 53));
        addSlot(new SlotItemHandler(blockEntity.getInventory(), 3, 116, 35) {
            @Override
            public boolean mayPlace(ItemStack stack) {
                return false;
            }
        });
    }

    @Override
    protected boolean moveItemToMachine(ItemStack stack) {
        if (AbstractMachineBlockEntity.isValveItem(stack)) {
            if (this.moveItemStackTo(stack, 2, 3, false)) return true;
        }
        if (stack.is(Items.WATER_BUCKET)) {
            if (this.moveItemStackTo(stack, 1, 2, false)) return true;
        }
        return this.moveItemStackTo(stack, 0, 1, false);
    }
}
