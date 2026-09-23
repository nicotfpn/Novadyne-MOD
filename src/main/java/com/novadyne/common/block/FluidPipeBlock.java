package com.novadyne.common.block;

import com.mojang.serialization.MapCodec;
import net.minecraft.core.BlockPos;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.phys.shapes.CollisionContext;
import net.minecraft.world.phys.shapes.Shapes;
import net.minecraft.world.phys.shapes.VoxelShape;

/** Passive water conduit. The sink discovers loaded, connected pipes when pumping. */
public class FluidPipeBlock extends Block {
    public static final MapCodec<FluidPipeBlock> CODEC = simpleCodec(FluidPipeBlock::new);
    private static final VoxelShape SHAPE = Shapes.or(
            box(0, 6, 6, 16, 10, 10),
            box(6, 0, 6, 10, 16, 10),
            box(6, 6, 0, 10, 10, 16));

    public FluidPipeBlock(Properties properties) { super(properties); }

    @Override protected MapCodec<? extends Block> codec() { return CODEC; }

    @Override
    protected VoxelShape getShape(BlockState state, BlockGetter level, BlockPos pos, CollisionContext context) {
        return SHAPE;
    }
}
