package com.novadyne.common.block;

import com.mojang.serialization.MapCodec;
import net.minecraft.world.level.block.Block;

/** Passive water conduit. The sink discovers loaded, connected pipes when pumping. */
public class FluidPipeBlock extends Block {
    public static final MapCodec<FluidPipeBlock> CODEC = simpleCodec(FluidPipeBlock::new);

    public FluidPipeBlock(Properties properties) { super(properties); }

    @Override protected MapCodec<? extends Block> codec() { return CODEC; }
}
