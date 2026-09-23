package com.novadyne.common.blockentity;

import com.novadyne.ModBlockEntities;
import com.novadyne.ModItems;
import com.novadyne.common.capabilities.fluid.WaterStorage;
import com.novadyne.common.menu.LitografiaMenu;
import net.minecraft.core.BlockPos;
import net.minecraft.core.HolderLookup;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.util.RandomSource;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.inventory.AbstractContainerMenu;
import net.minecraft.world.inventory.ContainerLevelAccess;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.storage.ValueInput;
import net.minecraft.world.level.storage.ValueOutput;

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
    public static final int WATER_PER_WAFER = 1000;
    public static final int WATER_CAPACITY = 4000;
    private final WaterStorage water = new WaterStorage(WATER_CAPACITY, this::setChanged);

    public WaterStorage getWaterStorage() { return water; }
    public int getWaterAmount() { return water.amount(); }

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

        if (input.is(ModItems.STACKED_ELECTRONIC_CIRCUIT.get())) {
            // Both the success and failure result must have somewhere to go.
            return getStackInSlot(SLOT_OUTPUT).isEmpty();
        }

        if (input.is(ModItems.PART_ELECTRONIC_DIRTY_SILICON_WAFER.get())) {
            if (water.amount() >= WATER_PER_WAFER || getStackInSlot(SLOT_BUCKET).is(Items.WATER_BUCKET)) {
                return canOutputAccept(SLOT_OUTPUT, new ItemStack(ModItems.PART_ELECTRONIC_ETCHED_SILICON_WAFER.get()));
            }
        }

        return false;
    }

    @Override
    protected void processComplete() {
        if (!canProcess()) return;
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

        insertResult(SLOT_OUTPUT, result);
    }

    private void processCleaning() {
        extractItem(SLOT_INPUT, 1);
        if (water.amount() >= WATER_PER_WAFER) {
            water.consume(WATER_PER_WAFER);
        } else {
            extractItem(SLOT_BUCKET, 1);
            // The consumed water bucket leaves its empty bucket in the bucket slot.
            insertResult(SLOT_BUCKET, new ItemStack(Items.BUCKET));
        }
        insertResult(SLOT_OUTPUT, new ItemStack(ModItems.PART_ELECTRONIC_ETCHED_SILICON_WAFER.get()));
    }

    @Override protected void saveAdditional(ValueOutput output) {
        super.saveAdditional(output);
        output.putInt("water", water.amount());
    }

    @Override protected void loadAdditional(ValueInput input) {
        super.loadAdditional(input);
        water.setAmount(input.getIntOr("water", 0));
    }

    @Override public CompoundTag getUpdateTag(HolderLookup.Provider registries) {
        CompoundTag tag = super.getUpdateTag(registries);
        tag.putInt("water", water.amount());
        return tag;
    }

    @Override public void handleUpdateTag(ValueInput input) {
        super.handleUpdateTag(input);
        water.setAmount(input.getIntOr("water", water.amount()));
    }
}
