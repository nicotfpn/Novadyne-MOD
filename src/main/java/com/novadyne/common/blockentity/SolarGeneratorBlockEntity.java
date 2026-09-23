package com.novadyne.common.blockentity;

import com.novadyne.ModBlockEntities;
import com.novadyne.ModBlocks;
import com.novadyne.api.energy.Action;
import com.novadyne.api.energy.AutomationType;
import net.minecraft.core.BlockPos;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.level.block.state.BlockState;

public class SolarGeneratorBlockEntity extends AbstractGeneratorBlockEntity {
    public static final int BASIC_FE_PER_TICK = 40;
    public static final int ADVANCED_FE_PER_TICK = 100;
    private final boolean advanced;

    public SolarGeneratorBlockEntity(BlockPos pos, BlockState state) {
        super(state.is(ModBlocks.ADVANCED_SOLAR_GENERATOR.get())
                ? ModBlockEntities.ADVANCED_SOLAR_GENERATOR.get()
                : ModBlockEntities.BASIC_SOLAR_GENERATOR.get(), pos, state);
        advanced = state.is(ModBlocks.ADVANCED_SOLAR_GENERATOR.get());
    }

    public static int outputFor(boolean advanced, boolean day, boolean exposedToSky) {
        if (!exposedToSky) return 0;
        if (advanced) return day ? ADVANCED_FE_PER_TICK : ADVANCED_FE_PER_TICK / 4;
        return day ? BASIC_FE_PER_TICK : 0;
    }

    @Override protected void generate() {
        if (!(level instanceof ServerLevel server)) return;
        boolean day = Math.floorMod(server.getDefaultClockTime(), 24_000L) < 12_000L;
        int production = outputFor(advanced, day, level.canSeeSky(worldPosition.above()));
        if (production > 0) energy.insert(production, Action.EXECUTE, AutomationType.INTERNAL);
    }

    @Override protected int maxTransferPerTick() {
        return advanced ? ADVANCED_FE_PER_TICK : BASIC_FE_PER_TICK;
    }
}
