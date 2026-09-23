package com.novadyne.common.blockentity;

import com.novadyne.ModBlockEntities;
import com.novadyne.api.energy.Action;
import com.novadyne.api.energy.AutomationType;
import com.novadyne.common.menu.FuelGeneratorMenu;
import net.minecraft.core.BlockPos;
import net.minecraft.network.chat.Component;
import net.minecraft.world.Containers;
import net.minecraft.world.MenuProvider;
import net.minecraft.world.SimpleContainer;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.inventory.AbstractContainerMenu;
import net.minecraft.world.inventory.ContainerLevelAccess;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.crafting.RecipeType;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.storage.ValueInput;
import net.minecraft.world.level.storage.ValueOutput;
import net.neoforged.neoforge.transfer.item.ItemResource;
import net.neoforged.neoforge.transfer.item.ItemStacksResourceHandler;
import net.neoforged.neoforge.transfer.transaction.Transaction;
import org.jetbrains.annotations.Nullable;

/** Burns furnace fuels, including wood. Pauses when the FE buffer is full. */
public class FuelGeneratorBlockEntity extends AbstractGeneratorBlockEntity implements MenuProvider {
    public static final int FE_PER_TICK = 80;
    private final ItemStacksResourceHandler inventory = new ItemStacksResourceHandler(2) {
        @Override protected void onContentsChanged(int index, ItemStack previousContents) { setChanged(); }
        @Override public boolean isValid(int index, ItemResource resource) {
            return index == 1 || index == 0 && isFuel(resource.toStack(1));
        }
    };
    private int burnRemaining;
    private int burnTotal;

    public FuelGeneratorBlockEntity(BlockPos pos, BlockState state) {
        super(ModBlockEntities.FUEL_GENERATOR.get(), pos, state);
    }

    public ItemStacksResourceHandler getInventory() { return inventory; }
    public int getBurnRemaining() { return burnRemaining; }
    public int getBurnTotal() { return burnTotal; }

    public boolean isFuel(ItemStack stack) {
        return level != null && !stack.isEmpty()
                && stack.getBurnTime(RecipeType.SMELTING, level.fuelValues()) > 0;
    }

    @Override protected int maxTransferPerTick() { return FE_PER_TICK; }

    @Override protected void generate() {
        if (energy.getNeeded() < FE_PER_TICK) return;
        if (burnRemaining == 0 && !startBurning()) return;
        energy.insert(FE_PER_TICK, Action.EXECUTE, AutomationType.INTERNAL);
        burnRemaining--;
        setChanged();
    }

    private boolean startBurning() {
        ItemResource fuel = inventory.getResource(0);
        if (fuel.isEmpty()) return false;
        ItemStack stack = fuel.toStack(1);
        int burnTime = stack.getBurnTime(RecipeType.SMELTING, level.fuelValues());
        if (burnTime <= 0) return false;
        var remainderTemplate = stack.getCraftingRemainder();
        ItemStack remainder = remainderTemplate != null ? remainderTemplate.create() : ItemStack.EMPTY;
        try (Transaction tx = Transaction.openRoot()) {
            if (inventory.extract(0, fuel, 1, tx) != 1) return false;
            if (!remainder.isEmpty() && inventory.insert(1, ItemResource.of(remainder), remainder.getCount(), tx) != remainder.getCount()) {
                return false;
            }
            tx.commit();
        }
        burnRemaining = burnTotal = burnTime;
        setChanged();
        return true;
    }

    @Override public Component getDisplayName() { return getBlockState().getBlock().getName(); }

    @Override @Nullable
    public AbstractContainerMenu createMenu(int id, Inventory playerInventory, Player player) {
        return new FuelGeneratorMenu(id, playerInventory, this, ContainerLevelAccess.create(level, worldPosition));
    }

    @Override public void preRemoveSideEffects(BlockPos pos, BlockState state) {
        super.preRemoveSideEffects(pos, state);
        if (level == null) return;
        SimpleContainer container = new SimpleContainer(inventory.size());
        for (int i = 0; i < inventory.size(); i++) {
            container.setItem(i, inventory.getResource(i).toStack(inventory.getAmountAsInt(i)));
        }
        Containers.dropContents(level, worldPosition, container);
    }

    @Override protected void saveAdditional(ValueOutput output) {
        super.saveAdditional(output);
        output.putInt("burn_remaining", burnRemaining);
        output.putInt("burn_total", burnTotal);
        inventory.serialize(output.child("inventory"));
    }

    @Override protected void loadAdditional(ValueInput input) {
        super.loadAdditional(input);
        burnRemaining = Math.max(0, input.getIntOr("burn_remaining", 0));
        burnTotal = Math.max(0, input.getIntOr("burn_total", 0));
        inventory.deserialize(input.childOrEmpty("inventory"));
    }
}
