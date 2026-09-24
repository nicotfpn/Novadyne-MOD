package com.novadyne.common.block;

import com.mojang.serialization.MapCodec;
import com.novadyne.ModBlocks;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.neoforged.neoforge.capabilities.Capabilities;

/** Passive water conduit. The sink discovers loaded, connected pipes when pumping. */
public class FluidPipeBlock extends DirectionalConduitBlock {
    public static final MapCodec<FluidPipeBlock> CODEC = simpleCodec(FluidPipeBlock::new);

    public FluidPipeBlock(Properties properties) { super(properties); }

    @Override protected MapCodec<? extends Block> codec() { return CODEC; }

    @Override protected boolean connectsTo(Level level, BlockPos neighbor, Direction side) {
        return level.getBlockState(neighbor).is(ModBlocks.FLUID_PIPE.get())
                || level.getCapability(Capabilities.Fluid.BLOCK, neighbor, side) != null;
    }
}
