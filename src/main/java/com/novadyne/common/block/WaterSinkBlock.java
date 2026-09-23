package com.novadyne.common.block;

import com.mojang.serialization.MapCodec;
import com.novadyne.ModBlockEntities;
import com.novadyne.common.blockentity.WaterSinkBlockEntity;
import net.minecraft.core.BlockPos;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.BaseEntityBlock;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.entity.BlockEntityTicker;
import net.minecraft.world.level.block.entity.BlockEntityType;
import net.minecraft.world.level.block.state.BlockState;
import org.jetbrains.annotations.Nullable;

public class WaterSinkBlock extends BaseEntityBlock {
    public static final MapCodec<WaterSinkBlock> CODEC = simpleCodec(WaterSinkBlock::new);

    public WaterSinkBlock(Properties properties) { super(properties); }

    @Override protected MapCodec<? extends BaseEntityBlock> codec() { return CODEC; }

    @Override @Nullable public BlockEntity newBlockEntity(BlockPos pos, BlockState state) {
        return new WaterSinkBlockEntity(pos, state);
    }

    @Override @Nullable
    public <T extends BlockEntity> BlockEntityTicker<T> getTicker(Level level, BlockState state, BlockEntityType<T> type) {
        if (level.isClientSide() || type != ModBlockEntities.WATER_SINK.get()) return null;
        return (lvl, pos, st, be) -> {
            if (be instanceof WaterSinkBlockEntity sink) sink.tickServer();
        };
    }
}
