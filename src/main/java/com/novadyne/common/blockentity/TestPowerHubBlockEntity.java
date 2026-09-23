package com.novadyne.common.blockentity;

import com.novadyne.ModBlockEntities;
import net.minecraft.core.BlockPos;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.state.BlockState;
import net.neoforged.neoforge.capabilities.Capabilities;
import net.neoforged.neoforge.transfer.energy.EnergyHandler;
import net.neoforged.neoforge.transfer.transaction.Transaction;

/** Infinite FE for the 5×5 horizontal test area, on the same Y level. */
public class TestPowerHubBlockEntity extends BlockEntity {
    public static final int RADIUS = 2;
    public static final int FE_PER_MACHINE_PER_TICK = 1_000;

    public TestPowerHubBlockEntity(BlockPos pos, BlockState state) {
        super(ModBlockEntities.TEST_POWER_HUB.get(), pos, state);
    }

    public void tickServer() {
        if (level == null || level.isClientSide()) return;
        for (int x = -RADIUS; x <= RADIUS; x++) {
            for (int z = -RADIUS; z <= RADIUS; z++) {
                if (x == 0 && z == 0) continue;
                BlockPos target = worldPosition.offset(x, 0, z);
                if (!level.hasChunkAt(target) || !(level.getBlockEntity(target) instanceof AbstractMachineBlockEntity)) continue;
                EnergyHandler energy = level.getCapability(Capabilities.Energy.BLOCK, target, null);
                if (energy == null) continue;
                try (Transaction tx = Transaction.openRoot()) {
                    if (energy.insert(FE_PER_MACHINE_PER_TICK, tx) > 0) tx.commit();
                }
            }
        }
    }
}
