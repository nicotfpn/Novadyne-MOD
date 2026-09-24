package com.novadyne.common.integration.energy;

import com.novadyne.ModBlocks;
import java.util.ArrayDeque;
import java.util.HashSet;
import java.util.Set;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.world.level.Level;
import net.neoforged.neoforge.capabilities.Capabilities;
import net.neoforged.neoforge.transfer.TransferPreconditions;
import net.neoforged.neoforge.transfer.energy.EnergyHandler;
import net.neoforged.neoforge.transfer.transaction.TransactionContext;

/** A stateless insertion port: energy goes directly to consumers in the caller's transaction. */
public final class EnergyCablePort implements EnergyHandler {
    private final Level level;
    private final BlockPos pos;
    private final Direction incomingSide;

    public EnergyCablePort(Level level, BlockPos pos, Direction incomingSide) {
        this.level = level;
        this.pos = pos;
        this.incomingSide = incomingSide;
    }

    @Override public long getAmountAsLong() { return 0; }
    @Override public long getCapacityAsLong() { return Integer.MAX_VALUE; }
    @Override public int extract(int amount, TransactionContext transaction) { return 0; }

    @Override public int insert(int amount, TransactionContext transaction) {
        TransferPreconditions.checkNonNegative(amount);
        if (amount == 0 || level.isClientSide() || !level.hasChunkAt(pos)
                || !level.getBlockState(pos).is(ModBlocks.ENERGY_CABLE.get())) return 0;

        BlockPos sender = incomingSide == null ? null : pos.relative(incomingSide);
        ArrayDeque<BlockPos> queue = new ArrayDeque<>();
        Set<BlockPos> visited = new HashSet<>();
        Set<BlockPos> supplied = new HashSet<>();
        queue.add(pos);
        visited.add(pos);
        int remaining = amount;
        while (!queue.isEmpty() && remaining > 0) {
            BlockPos current = queue.removeFirst();
            for (Direction direction : Direction.values()) {
                BlockPos neighbor = current.relative(direction);
                if (!level.hasChunkAt(neighbor)) continue;
                if (level.getBlockState(neighbor).is(ModBlocks.ENERGY_CABLE.get())) {
                    if (visited.size() < 128 && visited.add(neighbor)) queue.addLast(neighbor);
                    continue;
                }
                if (neighbor.equals(sender) || supplied.contains(neighbor)) continue;
                EnergyHandler target = level.getCapability(Capabilities.Energy.BLOCK, neighbor, direction.getOpposite());
                if (target == null) continue;
                int accepted = target.insert(remaining, transaction);
                if (accepted < 0 || accepted > remaining) throw new IllegalStateException("Invalid energy transfer amount");
                remaining -= accepted;
                if (accepted > 0) supplied.add(neighbor);
                if (remaining == 0) break;
            }
        }
        return amount - remaining;
    }
}
