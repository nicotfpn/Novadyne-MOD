package com.novadyne;

import net.minecraft.world.item.Item;
import net.neoforged.neoforge.registries.DeferredItem;
import net.neoforged.neoforge.registries.DeferredRegister;

public final class ModItems {
    public static final DeferredRegister.Items ITEMS = DeferredRegister.createItems(NovaDyneMod.MODID);

    // Materials
    public static final DeferredItem<Item> PURE_SILICON = ITEMS.registerSimpleItem("pure_silicon");
    public static final DeferredItem<Item> PART_SILICON_WAFER = ITEMS.registerSimpleItem("part_silicon_wafer");
    public static final DeferredItem<Item> CERAMIC_POWDER = ITEMS.registerSimpleItem("ceramic_powder");
    public static final DeferredItem<Item> PART_COPPER_LAYER = ITEMS.registerSimpleItem("part_copper_layer");
    public static final DeferredItem<Item> PART_BASE_WAFER = ITEMS.registerSimpleItem("part_base_wafer");
    public static final DeferredItem<Item> STACKED_ELECTRONIC_CIRCUIT = ITEMS.registerSimpleItem("stacked_electronic_circuit");
    public static final DeferredItem<Item> PART_ELECTRONIC_DIRTY_SILICON_WAFER = ITEMS.registerSimpleItem("part_electronic_dirty_silicon_wafer");
    public static final DeferredItem<Item> PART_ELECTRONIC_FAILED_SILICON_WAFER = ITEMS.registerSimpleItem("part_electronic_failed_silicon_wafer");
    public static final DeferredItem<Item> PART_ELECTRONIC_ETCHED_SILICON_WAFER = ITEMS.registerSimpleItem("part_electronic_etched_silicon_wafer");

    // Block items
    public static final DeferredItem<net.minecraft.world.item.BlockItem> MACERATOR =
            ITEMS.registerSimpleBlockItem("macerator", ModBlocks.MACERATOR);
    public static final DeferredItem<net.minecraft.world.item.BlockItem> WAFER_PRESS =
            ITEMS.registerSimpleBlockItem("wafer_press", ModBlocks.WAFER_PRESS);
    public static final DeferredItem<net.minecraft.world.item.BlockItem> PROCESSOR =
            ITEMS.registerSimpleBlockItem("processor", ModBlocks.PROCESSOR);
    public static final DeferredItem<net.minecraft.world.item.BlockItem> LITOGRAFIA =
            ITEMS.registerSimpleBlockItem("litografia", ModBlocks.LITOGRAFIA);

    // Valve upgrades
    public static final DeferredItem<Item> VALVE_TIER_1 = ITEMS.registerSimpleItem("valve_tier_1");
    public static final DeferredItem<Item> VALVE_TIER_2 = ITEMS.registerSimpleItem("valve_tier_2");
    public static final DeferredItem<Item> VALVE_TIER_3 = ITEMS.registerSimpleItem("valve_tier_3");
    public static final DeferredItem<Item> VALVE_TIER_4 = ITEMS.registerSimpleItem("valve_tier_4");
    public static final DeferredItem<Item> VALVE_TIER_5 = ITEMS.registerSimpleItem("valve_tier_5");
    public static final DeferredItem<Item> VALVE_TIER_6 = ITEMS.registerSimpleItem("valve_tier_6");
    public static final DeferredItem<Item> VALVE_TIER_7 = ITEMS.registerSimpleItem("valve_tier_7");

    private ModItems() {}
}
