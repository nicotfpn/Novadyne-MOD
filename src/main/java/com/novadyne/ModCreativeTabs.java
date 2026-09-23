package com.novadyne;

import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.item.ItemStack;
import net.neoforged.neoforge.registries.DeferredHolder;
import net.neoforged.neoforge.registries.DeferredRegister;

public class ModCreativeTabs {
    public static final DeferredRegister<CreativeModeTab> CREATIVE_MODE_TABS =
            DeferredRegister.create(Registries.CREATIVE_MODE_TAB, NovaDyneMod.MODID);

    public static final DeferredHolder<CreativeModeTab, CreativeModeTab> NOVADYNE_TAB =
            CREATIVE_MODE_TABS.register("novadyne", () -> CreativeModeTab.builder()
                    .title(Component.literal("NovaDyne"))
                    .icon(() -> new ItemStack(ModItems.STACKED_ELECTRONIC_CIRCUIT.get()))
                    .displayItems((parameters, output) -> {
                        output.accept(ModBlocks.MACERATOR.get());
                        output.accept(ModBlocks.WAFER_PRESS.get());
                        output.accept(ModBlocks.PROCESSOR.get());
                        output.accept(ModBlocks.LITOGRAFIA.get());
                        output.accept(ModBlocks.TEST_POWER_HUB.get());
                        output.accept(ModBlocks.WATER_SINK.get());
                        output.accept(ModBlocks.FLUID_PIPE.get());

                        output.accept(ModItems.PURE_SILICON.get());
                        output.accept(ModItems.CERAMIC_POWDER.get());
                        output.accept(ModItems.PART_COPPER_LAYER.get());
                        output.accept(ModItems.PART_BASE_WAFER.get());
                        output.accept(ModItems.PART_SILICON_WAFER.get());
                        output.accept(ModItems.STACKED_ELECTRONIC_CIRCUIT.get());
                        output.accept(ModItems.PART_ELECTRONIC_DIRTY_SILICON_WAFER.get());
                        output.accept(ModItems.PART_ELECTRONIC_FAILED_SILICON_WAFER.get());
                        output.accept(ModItems.PART_ELECTRONIC_ETCHED_SILICON_WAFER.get());

                        output.accept(ModItems.VALVE_TIER_1.get());
                        output.accept(ModItems.VALVE_TIER_2.get());
                        output.accept(ModItems.VALVE_TIER_3.get());
                        output.accept(ModItems.VALVE_TIER_4.get());
                        output.accept(ModItems.VALVE_TIER_5.get());
                        output.accept(ModItems.VALVE_TIER_6.get());
                        output.accept(ModItems.VALVE_TIER_7.get());
                    }).build());
}
