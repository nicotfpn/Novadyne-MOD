package com.novadyne.common.block;

import com.mojang.serialization.MapCodec;
import com.novadyne.ModBlockEntities;
import com.novadyne.common.blockentity.SolarGeneratorBlockEntity;
import net.minecraft.core.BlockPos;
import net.minecraft.network.chat.Component;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.BaseEntityBlock;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.entity.BlockEntityTicker;
import net.minecraft.world.level.block.entity.BlockEntityType;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.phys.BlockHitResult;
import org.jetbrains.annotations.Nullable;

public class SolarGeneratorBlock extends BaseEntityBlock {
    public static final MapCodec<SolarGeneratorBlock> CODEC = simpleCodec(SolarGeneratorBlock::new);
    public SolarGeneratorBlock(Properties properties) { super(properties); }
    @Override protected MapCodec<? extends BaseEntityBlock> codec() { return CODEC; }

    @Override @Nullable public BlockEntity newBlockEntity(BlockPos pos, BlockState state) {
        return new SolarGeneratorBlockEntity(pos, state);
    }

    @Override protected InteractionResult useWithoutItem(BlockState state, Level level, BlockPos pos, Player player, BlockHitResult hit) {
        if (!level.isClientSide() && level.getBlockEntity(pos) instanceof SolarGeneratorBlockEntity solar) {
            player.displayClientMessage(Component.translatable("message.novadyne.solar_energy", solar.getEnergy(0), solar.getMaxEnergy(0)), true);
        }
        return InteractionResult.SUCCESS;
    }

    @Override @Nullable
    public <T extends BlockEntity> BlockEntityTicker<T> getTicker(Level level, BlockState state, BlockEntityType<T> type) {
        if (level.isClientSide() || type != ModBlockEntities.BASIC_SOLAR_GENERATOR.get()
                && type != ModBlockEntities.ADVANCED_SOLAR_GENERATOR.get()) return null;
        return (lvl, pos, st, be) -> {
            if (be instanceof SolarGeneratorBlockEntity solar) solar.tickServer();
        };
    }
}
