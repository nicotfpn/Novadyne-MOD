package com.novadyne.common.blockentity;

import com.novadyne.ModBlockEntities;
import com.novadyne.ModItems;
import com.novadyne.common.menu.ProcessorMenu;
import net.minecraft.core.BlockPos;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.inventory.AbstractContainerMenu;
import net.minecraft.world.inventory.ContainerLevelAccess;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.block.state.BlockState;

public class ProcessorBlockEntity extends AbstractMachineBlockEntity {

    @Override
    public AbstractContainerMenu createMenu(int containerId, Inventory playerInventory, Player player) {
        return new ProcessorMenu(containerId, playerInventory, this, ContainerLevelAccess.create(level, worldPosition));
    }

    private static final int SLOT_INPUT_1 = 0;
    private static final int SLOT_INPUT_2 = 1;
    private static final int SLOT_INPUT_3 = 2;
    private static final int SLOT_OUTPUT = 3;
    private static final int SLOT_VALVE = 4;
    private static final int INVENTORY_SIZE = 5;

    public static final long MAX_ENERGY = 25_000;
    public static final long ENERGY_PER_TICK = 50;
    public static final int MAX_PROGRESS = 150;

    private static final ItemStack RESULT = new ItemStack(ModItems.STACKED_ELECTRONIC_CIRCUIT.get(), 1);

    public ProcessorBlockEntity(BlockPos pos, BlockState state) {
        super(ModBlockEntities.PROCESSOR.get(), pos, state, INVENTORY_SIZE, MAX_ENERGY, ENERGY_PER_TICK);
        this.maxProgress = MAX_PROGRESS;
    }

    @Override
    protected int getValveSlotIndex() {
        return SLOT_VALVE;
    }

    @Override protected int getOutputSlotIndex() { return SLOT_OUTPUT; }

    @Override
    protected boolean canProcess() {
        ItemStack input1 = getStackInSlot(SLOT_INPUT_1);
        ItemStack input2 = getStackInSlot(SLOT_INPUT_2);
        ItemStack input3 = getStackInSlot(SLOT_INPUT_3);

        if (input1.isEmpty() || input2.isEmpty() || input3.isEmpty()) return false;
        if (!input1.is(ModItems.PART_SILICON_WAFER.get())) return false;
        if (!input2.is(ModItems.PART_COPPER_LAYER.get())) return false;
        if (!input3.is(ModItems.PART_BASE_WAFER.get())) return false;

        return canOutputAccept(SLOT_OUTPUT, RESULT);
    }

    @Override
    protected void processComplete() {
        if (!canProcess()) return;
        extractItem(SLOT_INPUT_1, 1);
        extractItem(SLOT_INPUT_2, 1);
        extractItem(SLOT_INPUT_3, 1);

        insertResult(SLOT_OUTPUT, RESULT.copy());
    }
}
