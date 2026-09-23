package com.novadyne.common.block;

import com.mojang.serialization.MapCodec;
import com.novadyne.ModBlockEntities;
import com.novadyne.common.blockentity.FuelGeneratorBlockEntity;
import net.minecraft.core.BlockPos;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.entity.BlockEntityTicker;
import net.minecraft.world.level.block.entity.BlockEntityType;
import net.minecraft.world.level.block.state.BlockState;
import org.jetbrains.annotations.Nullable;

public class FuelGeneratorBlock extends AbstractMachineBlock {
    public static final MapCodec<FuelGeneratorBlock> CODEC = simpleCodec(FuelGeneratorBlock::new);
    public FuelGeneratorBlock(Properties properties) { super(properties); }
    @Override protected MapCodec<? extends AbstractMachineBlock> codec() { return CODEC; }

    @Override protected BlockEntityType<?> getBlockEntityType() { return ModBlockEntities.FUEL_GENERATOR.get(); }

    @Override @Nullable public BlockEntity newBlockEntity(BlockPos pos, BlockState state) {
        return new FuelGeneratorBlockEntity(pos, state);
    }

    @Override @Nullable
    public <T extends BlockEntity> BlockEntityTicker<T> getTicker(Level level, BlockState state, BlockEntityType<T> type) {
        if (level.isClientSide() || type != ModBlockEntities.FUEL_GENERATOR.get()) return null;
        return (lvl, pos, st, be) -> {
            if (be instanceof FuelGeneratorBlockEntity generator) generator.tickServer();
        };
    }
}
