package com.novadyne.common.block;

import com.mojang.serialization.MapCodec;
import com.novadyne.ModBlockEntities;
import com.novadyne.common.blockentity.LitografiaBlockEntity;
import net.minecraft.core.BlockPos;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.entity.BlockEntityType;
import net.minecraft.world.level.block.state.BlockState;
import org.jetbrains.annotations.Nullable;

public class LitografiaBlock extends AbstractMachineBlock {
    public static final MapCodec<LitografiaBlock> CODEC = simpleCodec(LitografiaBlock::new);

    public LitografiaBlock(Properties properties) {
        super(properties);
    }

    @Override
    protected MapCodec<? extends AbstractMachineBlock> codec() {
        return CODEC;
    }

    @Override
    protected BlockEntityType<?> getBlockEntityType() {
        return ModBlockEntities.LITOGRAFIA.get();
    }

    @Override
    @Nullable
    public BlockEntity newBlockEntity(BlockPos pos, BlockState state) {
        return new LitografiaBlockEntity(pos, state);
    }
}
