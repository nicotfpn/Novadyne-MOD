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
    public static final DeferredItem<net.minecraft.world.item.BlockItem> TEST_POWER_HUB =
            ITEMS.registerSimpleBlockItem("test_power_hub", ModBlocks.TEST_POWER_HUB);
    public static final DeferredItem<net.minecraft.world.item.BlockItem> WATER_SINK =
            ITEMS.registerSimpleBlockItem("water_sink", ModBlocks.WATER_SINK);
    public static final DeferredItem<net.minecraft.world.item.BlockItem> FLUID_PIPE =
            ITEMS.registerSimpleBlockItem("fluid_pipe", ModBlocks.FLUID_PIPE);
    public static final DeferredItem<net.minecraft.world.item.BlockItem> ENERGY_CABLE =
            ITEMS.registerSimpleBlockItem("energy_cable", ModBlocks.ENERGY_CABLE);
    public static final DeferredItem<net.minecraft.world.item.BlockItem> FUEL_GENERATOR =
            ITEMS.registerSimpleBlockItem("fuel_generator", ModBlocks.FUEL_GENERATOR);
    public static final DeferredItem<net.minecraft.world.item.BlockItem> BASIC_SOLAR_GENERATOR =
            ITEMS.registerSimpleBlockItem("basic_solar_generator", ModBlocks.BASIC_SOLAR_GENERATOR);
    public static final DeferredItem<net.minecraft.world.item.BlockItem> ADVANCED_SOLAR_GENERATOR =
            ITEMS.registerSimpleBlockItem("advanced_solar_generator", ModBlocks.ADVANCED_SOLAR_GENERATOR);

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
