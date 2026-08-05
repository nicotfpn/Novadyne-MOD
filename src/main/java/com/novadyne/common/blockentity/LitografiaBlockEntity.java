package com.novadyne.common.blockentity;

import com.novadyne.ModBlockEntities;
import com.novadyne.ModItems;
import com.novadyne.common.menu.LitografiaMenu;
import net.minecraft.core.BlockPos;
import net.minecraft.util.RandomSource;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.inventory.AbstractContainerMenu;
import net.minecraft.world.inventory.ContainerLevelAccess;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.block.state.BlockState;

public class LitografiaBlockEntity extends AbstractMachineBlockEntity {

    @Override
    public AbstractContainerMenu createMenu(int containerId, Inventory playerInventory, Player player) {
        return new LitografiaMenu(containerId, playerInventory, this, ContainerLevelAccess.create(level, worldPosition));
    }

    private static final int SLOT_INPUT = 0;
    private static final int SLOT_BUCKET = 1;
    private static final int SLOT_VALVE = 2;
    private static final int SLOT_OUTPUT = 3;
    private static final int INVENTORY_SIZE = 4;

    public static final long MAX_ENERGY = 20_000;
    public static final long ENERGY_PER_TICK = 40;
    public static final int MAX_PROGRESS = 120;

    public LitografiaBlockEntity(BlockPos pos, BlockState state) {
        super(ModBlockEntities.LITOGRAFIA.get(), pos, state, INVENTORY_SIZE, MAX_ENERGY, ENERGY_PER_TICK);
        this.maxProgress = MAX_PROGRESS;
    }

    @Override
    protected int getValveSlotIndex() {
        return SLOT_VALVE;
    }

    @Override
    protected boolean canProcess() {
        updateValveTierFromSlot();

        ItemStack input = getStackInSlot(SLOT_INPUT);
        if (input.isEmpty()) return false;

        ItemStack output = getStackInSlot(SLOT_OUTPUT);

        if (input.is(ModItems.STACKED_ELECTRONIC_CIRCUIT.get())) {
            return canOutputAccept(output, ItemStack.EMPTY);
        }

        if (input.is(ModItems.PART_ELECTRONIC_DIRTY_SILICON_WAFER.get())) {
            if (getStackInSlot(SLOT_BUCKET).is(Items.WATER_BUCKET)) {
                return canOutputAccept(output, new ItemStack(ModItems.PART_ELECTRONIC_ETCHED_SILICON_WAFER.get()));
            }
        }

        return false;
    }

    private boolean canOutputAccept(ItemStack output, ItemStack result) {
        if (output.isEmpty()) return true;
        if (result.isEmpty()) return output.getCount() < output.getMaxStackSize();
        if (!ItemStack.isSameItemSameComponents(result, output)) return false;
        return output.getCount() + result.getCount() <= output.getMaxStackSize();
    }

    @Override
    protected void processComplete() {
        ItemStack input = getStackInSlot(SLOT_INPUT);

        if (input.is(ModItems.STACKED_ELECTRONIC_CIRCUIT.get())) {
            processEngraving();
        } else if (input.is(ModItems.PART_ELECTRONIC_DIRTY_SILICON_WAFER.get())) {
            processCleaning();
        }
    }

    private void processEngraving() {
        int tier = Math.max(1, valveTier);

        // Linear failure chance: tier 1 = 30%, tier 7 ≈ 5%
        // failureChance = 0.30 - (tier - 1) * 0.04167
        double failureChance = 0.30 - (tier - 1) * (0.25 / 6.0);
        failureChance = Math.max(0.05, Math.min(0.30, failureChance));

        RandomSource rng = level != null ? level.getRandom() : RandomSource.create();
        boolean success = rng.nextDouble() >= failureChance;

        extractItem(SLOT_INPUT, 1);

        ItemStack result;
        if (success) {
            result = new ItemStack(ModItems.PART_ELECTRONIC_DIRTY_SILICON_WAFER.get(), 1);
        } else {
            result = new ItemStack(ModItems.PART_ELECTRONIC_FAILED_SILICON_WAFER.get(), 1);
        }

        insertOrDropOutput(result);
    }

    private void processCleaning() {
        extractItem(SLOT_INPUT, 1);
        extractItem(SLOT_BUCKET, 1);

        insertOrDropOutput(new ItemStack(ModItems.PART_ELECTRONIC_ETCHED_SILICON_WAFER.get(), 1));
        insertOrDropOutput(new ItemStack(Items.BUCKET, 1));
    }

    private void insertOrDropOutput(ItemStack stack) {
        ItemStack remaining = insertItem(SLOT_OUTPUT, stack);
        if (!remaining.isEmpty()) {
            if (level != null) {
                java.util.Objects.requireNonNull(level).addFreshEntity(
                        new net.minecraft.world.entity.item.ItemEntity(level,
                                worldPosition.getX() + 0.5, worldPosition.getY() + 1.0, worldPosition.getZ() + 0.5,
                                remaining));
            }
        }
    }
}
