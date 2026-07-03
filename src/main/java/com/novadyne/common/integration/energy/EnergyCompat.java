package com.novadyne.common.integration.energy;

import com.novadyne.api.energy.IStrictEnergyHandler;
import net.minecraft.core.Direction;
import net.neoforged.neoforge.capabilities.BlockCapability;
import net.neoforged.neoforge.capabilities.Capabilities;
import net.neoforged.neoforge.capabilities.ItemCapability;
import net.neoforged.neoforge.transfer.access.ItemAccess;
import net.neoforged.neoforge.transfer.energy.EnergyHandler;
import org.jspecify.annotations.Nullable;

@SuppressWarnings("removal")
public final class EnergyCompat {

    private EnergyCompat() {}

    public static EnergyHandler wrap(IStrictEnergyHandler handler) {
        return new NovadyneEnergyHandler(handler);
    }

    public static EnergyHandler wrap(IStrictEnergyHandler handler, int container) {
        return new NovadyneEnergyHandler(handler, container);
    }

    public static IStrictEnergyHandler fromLegacy(Object handler) {
        if (handler instanceof net.neoforged.neoforge.energy.IEnergyStorage storage) {
            return new ForgeStrictEnergyHandler(storage);
        }
        return null;
    }

    public static BlockCapability<EnergyHandler, @Nullable Direction> blockCap() {
        return Capabilities.Energy.BLOCK;
    }

    public static ItemCapability<EnergyHandler, ItemAccess> itemCap() {
        return Capabilities.Energy.ITEM;
    }
}
