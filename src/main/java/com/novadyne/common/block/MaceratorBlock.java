package com.novadyne.common.block;

import com.mojang.serialization.MapCodec;
import com.novadyne.ModBlockEntities;
import com.novadyne.common.blockentity.MaceratorBlockEntity;
import net.minecraft.core.BlockPos;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.entity.BlockEntityType;
import net.minecraft.world.level.block.state.BlockState;
import org.jetbrains.annotations.Nullable;

public class MaceratorBlock extends AbstractMachineBlock {
    public static final MapCodec<MaceratorBlock> CODEC = simpleCodec(MaceratorBlock::new);

    public MaceratorBlock(Properties properties) {
        super(properties);
    }

    @Override
    protected MapCodec<? extends AbstractMachineBlock> codec() {
        return CODEC;
    }

    @Override
    protected BlockEntityType<?> getBlockEntityType() {
        return ModBlockEntities.MACERATOR.get();
    }

    @Override
    @Nullable
    public BlockEntity newBlockEntity(BlockPos pos, BlockState state) {
        return new MaceratorBlockEntity(pos, state);
    }
}
