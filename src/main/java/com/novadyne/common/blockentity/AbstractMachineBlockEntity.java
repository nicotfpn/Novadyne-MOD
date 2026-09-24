package com.novadyne.common.blockentity;

import com.novadyne.api.energy.Action;
import com.novadyne.api.energy.AutomationType;
import com.novadyne.api.energy.IStrictEnergyHandler;
import com.novadyne.api.machine.IUpgradeableMachine;
import com.novadyne.common.capabilities.energy.MachineEnergyContainer;
import com.novadyne.common.capabilities.item.SidedMachineItemHandler;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.HolderLookup;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.network.protocol.Packet;
import net.minecraft.network.Connection;
import net.minecraft.network.protocol.game.ClientboundBlockEntityDataPacket;
import net.minecraft.network.chat.Component;
import net.minecraft.world.MenuProvider;
import net.minecraft.world.Containers;
import net.minecraft.world.SimpleContainer;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.entity.BlockEntityType;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.storage.ValueInput;
import net.minecraft.world.level.storage.ValueOutput;
import net.neoforged.neoforge.transfer.item.ItemResource;
import net.neoforged.neoforge.transfer.item.ItemStacksResourceHandler;
import net.neoforged.neoforge.capabilities.Capabilities;
import net.neoforged.neoforge.transfer.ResourceHandler;
import net.neoforged.neoforge.transfer.transaction.Transaction;
import org.jetbrains.annotations.Nullable;

public abstract class AbstractMachineBlockEntity extends BlockEntity implements IUpgradeableMachine, IStrictEnergyHandler, MenuProvider {
    protected static final String TAG_ENERGY = "energy";
    protected static final String TAG_VALVE_TIER = "valve_tier";
    protected static final String TAG_PROGRESS = "progress";
    protected static final String TAG_INVENTORY = "inventory";
    public static final int ITEM_DISABLED = 0;
    public static final int ITEM_INPUT = 1;
    public static final int ITEM_OUTPUT = 2;
    public static final int ITEM_BOTH = 3;
    private static final String TAG_AUTO_OUTPUT = "auto_output";
    private static final String TAG_SIDE_PREFIX = "item_side_";

    @Override
    public Component getDisplayName() {
        return getBlockState().getBlock().getName();
    }

    public ItemStacksResourceHandler getInventory() {
        return inventory;
    }

    protected final MachineEnergyContainer<AbstractMachineBlockEntity> energyContainer;
    protected final ItemStacksResourceHandler inventory;
    protected int valveTier = 0;
    protected int progress = 0;
    protected int maxProgress = 100;
    // Front, back, left, right, top, bottom, relative to the machine's front.
    private final int[] itemModes = {ITEM_INPUT, ITEM_INPUT, ITEM_INPUT, ITEM_INPUT, ITEM_INPUT, ITEM_OUTPUT};
    private boolean autoOutput;

    public int getItemMode(int relativeSide) { return itemModes[relativeSide]; }
    public boolean isAutoOutput() { return autoOutput; }
    public int getItemOutputSlot() { return getOutputSlotIndex(); }
    protected abstract int getOutputSlotIndex();

    public void cycleItemMode(int relativeSide) {
        if (relativeSide < 0 || relativeSide >= itemModes.length || level == null || level.isClientSide()) return;
        itemModes[relativeSide] = (itemModes[relativeSide] + 1) % 4;
        level.invalidateCapabilities(worldPosition);
        sync();
    }

    public void toggleAutoOutput() {
        if (level == null || level.isClientSide()) return;
        autoOutput = !autoOutput;
        sync();
    }

    public int getItemMode(Direction worldSide) {
        Direction front = getBlockState().getValue(com.novadyne.common.block.AbstractMachineBlock.FACING);
        if (worldSide == front) return itemModes[0];
        if (worldSide == front.getOpposite()) return itemModes[1];
        if (worldSide == front.getCounterClockWise()) return itemModes[2];
        if (worldSide == front.getClockWise()) return itemModes[3];
        return itemModes[worldSide == Direction.UP ? 4 : 5];
    }

    public @Nullable ResourceHandler<ItemResource> getSidedItemHandler(@Nullable Direction side) {
        return side == null || getItemMode(side) == ITEM_DISABLED ? null : new SidedMachineItemHandler(this, side);
    }

    public AbstractMachineBlockEntity(BlockEntityType<?> type, BlockPos pos, BlockState state,
                                       int inventorySlots, long maxEnergy, long energyPerTick) {
        super(type, pos, state);
        this.energyContainer = MachineEnergyContainer.input(this, maxEnergy, energyPerTick, this::setChanged);
        this.inventory = createInventory(inventorySlots);
    }

    protected ItemStacksResourceHandler createInventory(int slots) {
        return new ItemStacksResourceHandler(slots) {
            @Override
            protected void onContentsChanged(int index, ItemStack previousContents) {
                setChanged();
            }

            @Override
            public boolean isValid(int index, ItemResource resource) {
                return AbstractMachineBlockEntity.this.isItemValidForSlot(index, resource);
            }
        };
    }

    protected boolean isItemValidForSlot(int slot, ItemResource resource) {
        if (isValveSlot(slot)) {
            return isValveItem(resource.getItem());
        }
        return true;
    }

    protected boolean isValveSlot(int slot) {
        return slot == getValveSlotIndex();
    }

    public static boolean isValveItem(ItemStack stack) {
        return !stack.isEmpty() && isValveItem(stack.getItem());
    }

    public static boolean isValveItem(Item item) {
        return BuiltInRegistries.ITEM.getKey(item).toString().contains("valve_tier_");
    }

    protected ItemStack getStackInSlot(int index) {
        return inventory.getResource(index).toStack(inventory.getAmountAsInt(index));
    }

    protected ItemStack extractItem(int index, int amount) {
        ItemResource resource = inventory.getResource(index);
        if (resource.isEmpty() || amount <= 0) {
            return ItemStack.EMPTY;
        }
        try (Transaction tx = Transaction.openRoot()) {
            int extracted = inventory.extract(index, resource, amount, tx);
            tx.commit();
            return resource.toStack(extracted);
        }
    }

    protected ItemStack insertItem(int index, ItemStack stack) {
        if (stack.isEmpty()) {
            return ItemStack.EMPTY;
        }
        try (Transaction tx = Transaction.openRoot()) {
            int inserted = inventory.insert(index, ItemResource.of(stack), stack.getCount(), tx);
            tx.commit();
            return stack.copyWithCount(stack.getCount() - inserted);
        }
    }

    protected boolean canOutputAccept(int slot, ItemStack result) {
        if (result.isEmpty()) return false;
        ItemStack output = getStackInSlot(slot);
        return (output.isEmpty() || ItemStack.isSameItemSameComponents(output, result))
                && output.getCount() + result.getCount() <= result.getMaxStackSize();
    }

    protected void insertResult(int slot, ItemStack result) {
        if (!canOutputAccept(slot, result)) {
            throw new IllegalStateException("Machine output changed before completion");
        }
        if (!insertItem(slot, result).isEmpty()) {
            throw new IllegalStateException("Machine output rejected a validated result");
        }
    }

    protected abstract int getValveSlotIndex();

    @Override
    public int getValveTier() {
        return valveTier;
    }

    @Override
    public void setValveTier(int tier) {
        int clamped = Math.max(0, Math.min(tier, 7));
        if (this.valveTier != clamped) {
            this.valveTier = clamped;
            setChanged();
        }
    }

    @Override
    public boolean canAcceptValve(ItemStack stack) {
        return isValveItem(stack);
    }

    public int getProgress() {
        return progress;
    }

    public int getMaxProgress() {
        return maxProgress;
    }

    protected boolean hasEnoughEnergy() {
        return energyContainer.getEnergy() >= energyContainer.getEnergyPerTick();
    }

    protected void consumeEnergy() {
        energyContainer.extract(energyContainer.getEnergyPerTick(), Action.EXECUTE, AutomationType.INTERNAL);
    }

    protected void resetProgress() {
        progress = 0;
        setChanged();
    }

    protected void tickProgress() {
        progress++;
        if (progress >= maxProgress) {
            processComplete();
            resetProgress();
        }
        setChanged();
    }

    protected abstract boolean canProcess();

    protected abstract void processComplete();

    public void tickServer() {
        if (autoOutput && level != null) pushOutput();
        if (!hasEnoughEnergy()) {
            if (progress != 0) resetProgress();
            return;
        }

        if (canProcess()) {
            consumeEnergy();
            tickProgress();
        } else {
            if (progress != 0) {
                resetProgress();
            }
        }
    }

    private void pushOutput() {
        int outputSlot = getOutputSlotIndex();
        ItemResource resource = inventory.getResource(outputSlot);
        if (resource.isEmpty()) return;
        for (Direction side : Direction.values()) {
            if (getItemMode(side) != ITEM_OUTPUT && getItemMode(side) != ITEM_BOTH) continue;
            ResourceHandler<ItemResource> target = level.getCapability(Capabilities.Item.BLOCK,
                    worldPosition.relative(side), side.getOpposite());
            if (target == null) continue;
            for (int index = 0; index < target.size(); index++) {
                int available = Math.min(64, inventory.getAmountAsInt(outputSlot));
                if (available == 0) return;
                try (Transaction tx = Transaction.openRoot()) {
                    int accepted = target.insert(index, resource, available, tx);
                    if (accepted > 0 && inventory.extract(outputSlot, resource, accepted, tx) == accepted) {
                        tx.commit();
                    }
                }
            }
        }
    }

    protected void updateValveTierFromSlot() {
        ItemStack valveStack = getStackInSlot(getValveSlotIndex());
        if (!valveStack.isEmpty()) {
            String id = BuiltInRegistries.ITEM.getKey(valveStack.getItem()).toString();
            for (int t = 1; t <= 7; t++) {
                if (id.contains("valve_tier_" + t)) {
                    setValveTier(t);
                    return;
                }
            }
        }
        setValveTier(0);
    }

    public void dropInventory() {
        SimpleContainer container = new SimpleContainer(inventory.size());
        for (int i = 0; i < inventory.size(); i++) {
            container.setItem(i, getStackInSlot(i));
        }
        if (level != null) {
            Containers.dropContents(level, worldPosition, container);
        }
    }

    @Override
    public void preRemoveSideEffects(BlockPos pos, BlockState state) {
        super.preRemoveSideEffects(pos, state);
        dropInventory();
    }

    @Override
    protected void saveAdditional(ValueOutput output) {
        super.saveAdditional(output);
        output.putLong(TAG_ENERGY, energyContainer.getEnergy());
        output.putInt(TAG_VALVE_TIER, valveTier);
        output.putInt(TAG_PROGRESS, progress);
        inventory.serialize(output.child(TAG_INVENTORY));
        output.putBoolean(TAG_AUTO_OUTPUT, autoOutput);
        for (int i = 0; i < itemModes.length; i++) output.putInt(TAG_SIDE_PREFIX + i, itemModes[i]);
    }

    @Override
    protected void loadAdditional(ValueInput input) {
        super.loadAdditional(input);
        energyContainer.setEnergy(input.getLongOr(TAG_ENERGY, 0));
        valveTier = input.getIntOr(TAG_VALVE_TIER, 0);
        progress = input.getIntOr(TAG_PROGRESS, 0);
        ValueInput invInput = input.childOrEmpty(TAG_INVENTORY);
        inventory.deserialize(invInput);
        autoOutput = input.getBooleanOr(TAG_AUTO_OUTPUT, false);
        for (int i = 0; i < itemModes.length; i++) {
            int value = input.getIntOr(TAG_SIDE_PREFIX + i, itemModes[i]);
            itemModes[i] = Math.clamp(value, ITEM_DISABLED, ITEM_BOTH);
        }
    }

    @Override
    public CompoundTag getUpdateTag(HolderLookup.Provider registries) {
        CompoundTag tag = super.getUpdateTag(registries);
        tag.putLong(TAG_ENERGY, energyContainer.getEnergy());
        tag.putInt(TAG_VALVE_TIER, valveTier);
        tag.putInt(TAG_PROGRESS, progress);
        return tag;
    }

    @Override
    public void handleUpdateTag(ValueInput input) {
        energyContainer.setEnergy(input.getLongOr(TAG_ENERGY, energyContainer.getEnergy()));
        valveTier = input.getIntOr(TAG_VALVE_TIER, valveTier);
        progress = input.getIntOr(TAG_PROGRESS, progress);
    }

    @Override
    public void onDataPacket(Connection connection, ValueInput input) {
        handleUpdateTag(input);
    }

    @Override
    @Nullable
    public Packet<net.minecraft.network.protocol.game.ClientGamePacketListener> getUpdatePacket() {
        return ClientboundBlockEntityDataPacket.create(this);
    }

    protected void sync() {
        setChanged();
        if (level != null) {
            level.sendBlockUpdated(worldPosition, getBlockState(), getBlockState(), Block.UPDATE_ALL);
        }
    }

    // IStrictEnergyHandler

    @Override
    public int getEnergyContainerCount() {
        return 1;
    }

    @Override
    public long getEnergy(int container) {
        return energyContainer.getEnergy();
    }

    @Override
    public void setEnergy(int container, long energy) {
        energyContainer.setEnergy(energy);
    }

    @Override
    public long getMaxEnergy(int container) {
        return energyContainer.getMaxEnergy();
    }

    @Override
    public long getNeededEnergy(int container) {
        return energyContainer.getNeeded();
    }

    @Override
    public long insertEnergy(int container, long amount, Action action) {
        return energyContainer.insert(amount, action, AutomationType.INTERNAL);
    }

    @Override
    public long extractEnergy(int container, long amount, Action action) {
        return energyContainer.extract(amount, action, AutomationType.INTERNAL);
    }

    public long insertExternalEnergy(int container, long amount, Action action) {
        return container == 0 ? energyContainer.insert(amount, action, AutomationType.EXTERNAL) : amount;
    }

    public long extractExternalEnergy(int container, long amount, Action action) {
        return container == 0 ? energyContainer.extract(amount, action, AutomationType.EXTERNAL) : 0;
    }
}
