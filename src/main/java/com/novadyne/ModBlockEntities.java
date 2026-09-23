package com.novadyne;

import com.novadyne.common.blockentity.LitografiaBlockEntity;
import com.novadyne.common.blockentity.MaceratorBlockEntity;
import com.novadyne.common.blockentity.ProcessorBlockEntity;
import com.novadyne.common.blockentity.TestPowerHubBlockEntity;
import com.novadyne.common.blockentity.WaferPressBlockEntity;
import com.novadyne.common.blockentity.WaterSinkBlockEntity;
import net.minecraft.core.registries.Registries;
import net.minecraft.world.level.block.entity.BlockEntityType;
import net.neoforged.neoforge.registries.DeferredHolder;
import net.neoforged.neoforge.registries.DeferredRegister;

public final class ModBlockEntities {
    public static final DeferredRegister<BlockEntityType<?>> BLOCK_ENTITIES =
            DeferredRegister.create(Registries.BLOCK_ENTITY_TYPE, NovaDyneMod.MODID);

    public static final DeferredHolder<BlockEntityType<?>, BlockEntityType<MaceratorBlockEntity>> MACERATOR =
            BLOCK_ENTITIES.register("macerator", () ->
                    new BlockEntityType<>(MaceratorBlockEntity::new, ModBlocks.MACERATOR.get()));
    public static final DeferredHolder<BlockEntityType<?>, BlockEntityType<WaferPressBlockEntity>> WAFER_PRESS =
            BLOCK_ENTITIES.register("wafer_press", () ->
                    new BlockEntityType<>(WaferPressBlockEntity::new, ModBlocks.WAFER_PRESS.get()));
    public static final DeferredHolder<BlockEntityType<?>, BlockEntityType<ProcessorBlockEntity>> PROCESSOR =
            BLOCK_ENTITIES.register("processor", () ->
                    new BlockEntityType<>(ProcessorBlockEntity::new, ModBlocks.PROCESSOR.get()));
    public static final DeferredHolder<BlockEntityType<?>, BlockEntityType<LitografiaBlockEntity>> LITOGRAFIA =
            BLOCK_ENTITIES.register("litografia", () ->
                    new BlockEntityType<>(LitografiaBlockEntity::new, ModBlocks.LITOGRAFIA.get()));
    public static final DeferredHolder<BlockEntityType<?>, BlockEntityType<TestPowerHubBlockEntity>> TEST_POWER_HUB =
            BLOCK_ENTITIES.register("test_power_hub", () ->
                    new BlockEntityType<>(TestPowerHubBlockEntity::new, ModBlocks.TEST_POWER_HUB.get()));
    public static final DeferredHolder<BlockEntityType<?>, BlockEntityType<WaterSinkBlockEntity>> WATER_SINK =
            BLOCK_ENTITIES.register("water_sink", () ->
                    new BlockEntityType<>(WaterSinkBlockEntity::new, ModBlocks.WATER_SINK.get()));

    private ModBlockEntities() {}
}
