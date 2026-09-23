package com.novadyne;

import com.novadyne.common.block.LitografiaBlock;
import com.novadyne.common.block.MaceratorBlock;
import com.novadyne.common.block.ProcessorBlock;
import com.novadyne.common.block.TestPowerHubBlock;
import com.novadyne.common.block.WaferPressBlock;
import com.novadyne.common.block.WaterSinkBlock;
import com.novadyne.common.block.FluidPipeBlock;
import com.novadyne.common.block.FuelGeneratorBlock;
import com.novadyne.common.block.SolarGeneratorBlock;
import net.neoforged.neoforge.registries.DeferredBlock;
import net.neoforged.neoforge.registries.DeferredRegister;

public final class ModBlocks {
    public static final DeferredRegister.Blocks BLOCKS = DeferredRegister.createBlocks(NovaDyneMod.MODID);

    public static final DeferredBlock<MaceratorBlock> MACERATOR =
            BLOCKS.registerBlock("macerator", MaceratorBlock::new,
                    props -> props.strength(3.5F, 6.0F).requiresCorrectToolForDrops());
    public static final DeferredBlock<WaferPressBlock> WAFER_PRESS =
            BLOCKS.registerBlock("wafer_press", WaferPressBlock::new,
                    props -> props.strength(3.5F, 6.0F).requiresCorrectToolForDrops());
    public static final DeferredBlock<ProcessorBlock> PROCESSOR =
            BLOCKS.registerBlock("processor", ProcessorBlock::new,
                    props -> props.strength(3.5F, 6.0F).requiresCorrectToolForDrops());
    public static final DeferredBlock<LitografiaBlock> LITOGRAFIA =
            BLOCKS.registerBlock("litografia", LitografiaBlock::new,
                    props -> props.strength(3.5F, 6.0F).requiresCorrectToolForDrops());
    public static final DeferredBlock<TestPowerHubBlock> TEST_POWER_HUB =
            BLOCKS.registerBlock("test_power_hub", TestPowerHubBlock::new,
                    props -> props.strength(3.5F, 6.0F).requiresCorrectToolForDrops());
    public static final DeferredBlock<WaterSinkBlock> WATER_SINK =
            BLOCKS.registerBlock("water_sink", WaterSinkBlock::new,
                    props -> props.strength(3.5F, 6.0F).requiresCorrectToolForDrops());
    public static final DeferredBlock<FluidPipeBlock> FLUID_PIPE =
            BLOCKS.registerBlock("fluid_pipe", FluidPipeBlock::new,
                    props -> props.strength(1.5F, 6.0F).noOcclusion().requiresCorrectToolForDrops());
    public static final DeferredBlock<FuelGeneratorBlock> FUEL_GENERATOR =
            BLOCKS.registerBlock("fuel_generator", FuelGeneratorBlock::new,
                    props -> props.strength(3.5F, 6.0F).requiresCorrectToolForDrops());
    public static final DeferredBlock<SolarGeneratorBlock> BASIC_SOLAR_GENERATOR =
            BLOCKS.registerBlock("basic_solar_generator", SolarGeneratorBlock::new,
                    props -> props.strength(3.5F, 6.0F).requiresCorrectToolForDrops());
    public static final DeferredBlock<SolarGeneratorBlock> ADVANCED_SOLAR_GENERATOR =
            BLOCKS.registerBlock("advanced_solar_generator", SolarGeneratorBlock::new,
                    props -> props.strength(3.5F, 6.0F).requiresCorrectToolForDrops());

    private ModBlocks() {}
}
