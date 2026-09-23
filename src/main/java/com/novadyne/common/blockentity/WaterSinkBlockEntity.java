package com.novadyne.common.blockentity;

import com.novadyne.ModBlockEntities;
import com.novadyne.ModBlocks;
import java.util.ArrayDeque;
import java.util.HashSet;
import java.util.Set;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.material.Fluids;
import net.neoforged.neoforge.capabilities.Capabilities;
import net.neoforged.neoforge.transfer.fluid.FluidResource;
import net.neoforged.neoforge.transfer.ResourceHandler;
import net.neoforged.neoforge.transfer.InfiniteResourceHandler;
import net.neoforged.neoforge.transfer.transaction.Transaction;
import net.neoforged.neoforge.transfer.transaction.TransactionContext;

/** Infinite water source, bounded traversal, no forced chunk loads. */
public class WaterSinkBlockEntity extends BlockEntity {
    private static final int MAX_PIPES = 128;
    private static final int WATER_PER_TICK = 250;
    private static final FluidResource WATER = FluidResource.of(Fluids.WATER);

    private final ResourceHandler<FluidResource> source = new InfiniteResourceHandler<>(WATER) {
        @Override public int insert(int index, FluidResource resource, int amount, TransactionContext tx) {
            return 0;
        }
    };

    public WaterSinkBlockEntity(BlockPos pos, BlockState state) {
        super(ModBlockEntities.WATER_SINK.get(), pos, state);
    }

    public ResourceHandler<FluidResource> getWaterSource() { return source; }

    public void tickServer() {
        if (level == null || level.isClientSide()) return;
        ArrayDeque<BlockPos> queue = new ArrayDeque<>();
        Set<BlockPos> visited = new HashSet<>();
        Set<BlockPos> targets = new HashSet<>();
        queue.add(worldPosition);
        visited.add(worldPosition);

        while (!queue.isEmpty()) {
            BlockPos current = queue.removeFirst();
            for (Direction direction : Direction.values()) {
                BlockPos next = current.relative(direction);
                if (!level.hasChunkAt(next)) continue;
                if (level.getBlockState(next).is(ModBlocks.FLUID_PIPE.get())) {
                    if (visited.size() < MAX_PIPES + 1 && visited.add(next)) queue.addLast(next);
                    continue;
                }
                if (next.equals(worldPosition) || !targets.add(next)) continue;
                ResourceHandler<FluidResource> target = level.getCapability(Capabilities.Fluid.BLOCK, next, direction.getOpposite());
                if (target == null) continue;
                try (Transaction tx = Transaction.openRoot()) {
                    int moved = target.insert(WATER, WATER_PER_TICK, tx);
                    if (moved > 0) tx.commit();
                }
            }
        }
    }
}
