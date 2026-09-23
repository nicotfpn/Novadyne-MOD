package com.novadyne.common.blockentity;

import com.novadyne.api.energy.Action;
import com.novadyne.api.energy.AutomationType;
import com.novadyne.api.energy.IStrictEnergyHandler;
import com.novadyne.common.capabilities.energy.BasicEnergyContainer;
import com.novadyne.common.integration.energy.NovadyneEnergyHandler;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.entity.BlockEntityType;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.storage.ValueInput;
import net.minecraft.world.level.storage.ValueOutput;
import net.neoforged.neoforge.capabilities.Capabilities;
import net.neoforged.neoforge.transfer.energy.EnergyHandler;
import net.neoforged.neoforge.transfer.transaction.Transaction;

/** NovaDyne energy storage with a NeoForge output capability. */
public abstract class AbstractGeneratorBlockEntity extends BlockEntity implements IStrictEnergyHandler {
    public static final long CAPACITY = 40_000;
    protected final BasicEnergyContainer energy = BasicEnergyContainer.output(CAPACITY, this::setChanged);
    private final EnergyHandler energyPort = new NovadyneEnergyHandler(this);

    protected AbstractGeneratorBlockEntity(BlockEntityType<?> type, BlockPos pos, BlockState state) {
        super(type, pos, state);
    }

    public EnergyHandler getEnergyPort() { return energyPort; }

    public void tickServer() {
        if (level == null || level.isClientSide()) return;
        generate();
        pushEnergy();
    }

    protected abstract void generate();
    protected abstract int maxTransferPerTick();

    private void pushEnergy() {
        int remaining = maxTransferPerTick();
        for (Direction direction : Direction.values()) {
            if (remaining == 0 || energy.isEmpty()) break;
            BlockPos neighbor = worldPosition.relative(direction);
            if (!level.hasChunkAt(neighbor)) continue;
            EnergyHandler target = level.getCapability(Capabilities.Energy.BLOCK, neighbor, direction.getOpposite());
            if (target == null) continue;
            try (Transaction tx = Transaction.openRoot()) {
                int offered = (int) Math.min(remaining, energy.getEnergy());
                int inserted = target.insert(offered, tx);
                int extracted = energyPort.extract(inserted, tx);
                if (inserted > 0 && extracted == inserted) {
                    tx.commit();
                    remaining -= inserted;
                }
            }
        }
    }

    @Override protected void saveAdditional(ValueOutput output) {
        super.saveAdditional(output);
        output.putLong("energy", energy.getEnergy());
    }

    @Override protected void loadAdditional(ValueInput input) {
        super.loadAdditional(input);
        energy.setEnergy(input.getLongOr("energy", 0));
    }

    @Override public int getEnergyContainerCount() { return 1; }
    @Override public long getEnergy(int container) { return energy.getEnergy(); }
    @Override public void setEnergy(int container, long amount) { energy.setEnergy(amount); }
    @Override public long getMaxEnergy(int container) { return energy.getMaxEnergy(); }
    @Override public long getNeededEnergy(int container) { return energy.getNeeded(); }
    @Override public long insertEnergy(int container, long amount, Action action) {
        return energy.insert(amount, action, AutomationType.EXTERNAL);
    }
    @Override public long extractEnergy(int container, long amount, Action action) {
        return energy.extract(amount, action, AutomationType.EXTERNAL);
    }
}
