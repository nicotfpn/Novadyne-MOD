package com.novadyne.common.integration.energy;

import net.neoforged.neoforge.capabilities.Capabilities;
import net.neoforged.neoforge.capabilities.RegisterCapabilitiesEvent;

public final class NovadyneCapabilities {

    private NovadyneCapabilities() {}

    public static void onRegisterCapabilities(RegisterCapabilitiesEvent event) {
    }

    public static void registerBlockEntityEnergy(RegisterCapabilitiesEvent event,
          net.minecraft.world.level.block.entity.BlockEntityType<?> beType,
          java.util.function.Function<net.minecraft.world.level.block.entity.BlockEntity, com.novadyne.api.energy.IStrictEnergyHandler> provider) {
        event.registerBlockEntity(Capabilities.Energy.BLOCK, beType,
              (be, direction) -> EnergyCompat.wrap(provider.apply(be)));
    }

    public static void registerItemEnergy(RegisterCapabilitiesEvent event,
          net.minecraft.world.level.ItemLike item,
          java.util.function.Function<net.minecraft.world.item.ItemStack, com.novadyne.api.energy.IStrictEnergyHandler> provider) {
        event.registerItem(Capabilities.Energy.ITEM, (stack, ctx) -> EnergyCompat.wrap(provider.apply(stack)), item);
    }
}
