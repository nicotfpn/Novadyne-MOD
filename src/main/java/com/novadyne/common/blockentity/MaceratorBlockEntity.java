package com.novadyne.common.blockentity;

import com.novadyne.ModBlockEntities;
import com.novadyne.ModItems;
import com.novadyne.common.menu.MaceratorMenu;
import net.minecraft.core.BlockPos;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.inventory.AbstractContainerMenu;
import net.minecraft.world.inventory.ContainerLevelAccess;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.block.state.BlockState;
import java.util.Map;
import java.util.function.Predicate;

public class MaceratorBlockEntity extends AbstractMachineBlockEntity {

    @Override
    public AbstractContainerMenu createMenu(int containerId, Inventory playerInventory, Player player) {
        return new MaceratorMenu(containerId, playerInventory, this, ContainerLevelAccess.create(level, worldPosition));
    }

    private static final int SLOT_INPUT = 0;
    private static final int SLOT_OUTPUT = 1;
    private static final int SLOT_VALVE = 2;
    private static final int INVENTORY_SIZE = 3;

    public static final long MAX_ENERGY = 10_000;
    public static final long ENERGY_PER_TICK = 20;
    public static final int MAX_PROGRESS = 120;

    /*
     * FUTURE: Tag-based ore doubling recipes (c:ores/* -> 2x c:dusts/*)
     * This is where you'd integrate with the vanilla recipe manager or tag system.
     * For example:
     *   for (var oreTag : BuiltInRegistries.ITEM.getTagNames()
     *       .filter(tag -> tag.location().getPath().startsWith("ores/"))
     *       .toList()) {
     *       var dustTag = TagKey.create(Registries.ITEM,
     *           ResourceLocation.fromNamespaceAndPath("c", "dusts/" + oreName));
     *       recipes.put(new SimpleItemStackPredicate(oreTag), new RecipeResult(dustTag, 2));
     *   }
     */
    private static final Map<Predicate<ItemStack>, ItemStack> RECIPES = Map.of(
            stack -> stack.is(Items.CLAY_BALL),
            new ItemStack(ModItems.CERAMIC_POWDER.get(), 1),

            stack -> stack.is(ModItems.PART_ELECTRONIC_FAILED_SILICON_WAFER.get()),
            new ItemStack(ModItems.PART_COPPER_LAYER.get(), 1)

            // FUTURE: c:ores/* -> 2x c:dusts/* handled here via tag matching
    );

    public MaceratorBlockEntity(BlockPos pos, BlockState state) {
        super(ModBlockEntities.MACERATOR.get(), pos, state, INVENTORY_SIZE, MAX_ENERGY, ENERGY_PER_TICK);
        this.maxProgress = MAX_PROGRESS;
    }

    @Override
    protected int getValveSlotIndex() {
        return SLOT_VALVE;
    }

    @Override
    protected boolean canProcess() {
        updateValveTierFromSlot();

        ItemStack input = inventory.getStackInSlot(SLOT_INPUT);
        if (input.isEmpty()) return false;

        ItemStack output = inventory.getStackInSlot(SLOT_OUTPUT);
        ItemStack result = findRecipe(input);
        if (result.isEmpty()) return false;

        if (input.is(ModItems.PART_ELECTRONIC_FAILED_SILICON_WAFER.get())) {
            if (!output.isEmpty()) {
                if (!output.is(ModItems.PART_COPPER_LAYER.get()) && !output.is(ModItems.PART_BASE_WAFER.get()))
                    return false;
                if (output.getCount() >= output.getMaxStackSize())
                    return false;
            }
            return true;
        }

        if (!output.isEmpty()) {
            if (!ItemStack.isSameItemSameComponents(result, output)) return false;
            if (output.getCount() + result.getCount() > output.getMaxStackSize()) return false;
        }

        return true;
    }

    @Override
    protected void processComplete() {
        ItemStack input = inventory.getStackInSlot(SLOT_INPUT);
        ItemStack result = findRecipe(input);

        // Failed wafer: 50/50 chance per item between copper layer and base wafer
        if (input.is(ModItems.PART_ELECTRONIC_FAILED_SILICON_WAFER.get())) {
            ItemStack output;
            if (level != null && level.getRandom().nextBoolean()) {
                output = new ItemStack(ModItems.PART_COPPER_LAYER.get(), 1);
            } else {
                output = new ItemStack(ModItems.PART_BASE_WAFER.get(), 1);
            }
            inventory.extractItem(SLOT_INPUT, 1, false);
            insertOrDropOutput(output);
            return;
        }

        inventory.extractItem(SLOT_INPUT, 1, false);
        insertOrDropOutput(result.copy());
    }

    private void insertOrDropOutput(ItemStack stack) {
        ItemStack remaining = inventory.insertItem(SLOT_OUTPUT, stack, false);
        if (!remaining.isEmpty()) {
            if (level != null) {
                java.util.Objects.requireNonNull(level).addFreshEntity(
                        new net.minecraft.world.entity.item.ItemEntity(level,
                                worldPosition.getX() + 0.5, worldPosition.getY() + 1.0, worldPosition.getZ() + 0.5,
                                remaining));
            }
        }
    }

    private ItemStack findRecipe(ItemStack input) {
        for (var entry : RECIPES.entrySet()) {
            if (entry.getKey().test(input)) {
                return entry.getValue().copy();
            }
        }
        return ItemStack.EMPTY;
    }
}
