package com.novadyne.common.block;

import com.mojang.serialization.MapCodec;
import com.novadyne.ModBlockEntities;
import com.novadyne.common.blockentity.WaferPressBlockEntity;
import net.minecraft.core.BlockPos;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.entity.BlockEntityType;
import net.minecraft.world.level.block.state.BlockState;
import org.jetbrains.annotations.Nullable;

public class WaferPressBlock extends AbstractMachineBlock {
    public static final MapCodec<WaferPressBlock> CODEC = simpleCodec(WaferPressBlock::new);

    public WaferPressBlock(Properties properties) {
        super(properties);
    }

    @Override
    protected MapCodec<? extends AbstractMachineBlock> codec() {
        return CODEC;
    }

    @Override
    protected BlockEntityType<?> getBlockEntityType() {
        return ModBlockEntities.WAFER_PRESS.get();
    }

    @Override
    @Nullable
    public BlockEntity newBlockEntity(BlockPos pos, BlockState state) {
        return new WaferPressBlockEntity(pos, state);
    }
}
