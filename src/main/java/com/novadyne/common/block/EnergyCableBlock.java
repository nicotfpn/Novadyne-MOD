package com.novadyne.common.block;

import com.mojang.serialization.MapCodec;
import com.novadyne.ModBlocks;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.neoforged.neoforge.capabilities.Capabilities;

/** Passive cable; generators push energy along a bounded network. */
public class EnergyCableBlock extends DirectionalConduitBlock {
    public static final MapCodec<EnergyCableBlock> CODEC = simpleCodec(EnergyCableBlock::new);
    public EnergyCableBlock(Properties properties) { super(properties); }
    @Override protected MapCodec<? extends Block> codec() { return CODEC; }

    @Override protected boolean connectsTo(Level level, BlockPos neighbor, Direction side) {
        return level.getBlockState(neighbor).is(ModBlocks.ENERGY_CABLE.get())
                || level.getCapability(Capabilities.Energy.BLOCK, neighbor, side) != null;
    }

    @Override protected void onPlace(net.minecraft.world.level.block.state.BlockState state, Level level,
            BlockPos pos, net.minecraft.world.level.block.state.BlockState oldState, boolean movedByPiston) {
        super.onPlace(state, level, pos, oldState, movedByPiston);
        if (!oldState.is(this)) level.invalidateCapabilities(pos);
    }

    @Override protected void onRemove(net.minecraft.world.level.block.state.BlockState state, Level level,
            BlockPos pos, net.minecraft.world.level.block.state.BlockState newState, boolean movedByPiston) {
        if (!newState.is(this)) level.invalidateCapabilities(pos);
        super.onRemove(state, level, pos, newState, movedByPiston);
    }
}
