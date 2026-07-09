package com.novadyne.common.block;

import com.mojang.serialization.MapCodec;
import com.novadyne.ModBlockEntities;
import com.novadyne.common.blockentity.ProcessorBlockEntity;
import net.minecraft.core.BlockPos;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.entity.BlockEntityType;
import net.minecraft.world.level.block.state.BlockState;
import org.jetbrains.annotations.Nullable;

public class ProcessorBlock extends AbstractMachineBlock {
    public static final MapCodec<ProcessorBlock> CODEC = simpleCodec(ProcessorBlock::new);

    public ProcessorBlock(Properties properties) {
        super(properties);
    }

    @Override
    protected MapCodec<? extends AbstractMachineBlock> codec() {
        return CODEC;
    }

    @Override
    protected BlockEntityType<?> getBlockEntityType() {
        return ModBlockEntities.PROCESSOR.get();
    }

    @Override
    @Nullable
    public BlockEntity newBlockEntity(BlockPos pos, BlockState state) {
        return new ProcessorBlockEntity(pos, state);
    }
}
