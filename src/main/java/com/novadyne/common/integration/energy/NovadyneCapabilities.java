package com.novadyne.common.integration.energy;

import com.novadyne.ModBlockEntities;
import com.novadyne.ModBlocks;
import com.novadyne.api.energy.IStrictEnergyHandler;
import net.neoforged.neoforge.capabilities.Capabilities;
import net.neoforged.neoforge.capabilities.RegisterCapabilitiesEvent;

public final class NovadyneCapabilities {
    private NovadyneCapabilities() {}

    public static void onRegisterCapabilities(RegisterCapabilitiesEvent event) {
        registerBlockEntityEnergy(event, ModBlockEntities.MACERATOR.get(),
                be -> (IStrictEnergyHandler) be);
        registerBlockEntityEnergy(event, ModBlockEntities.WAFER_PRESS.get(),
                be -> (IStrictEnergyHandler) be);
        registerBlockEntityEnergy(event, ModBlockEntities.PROCESSOR.get(),
                be -> (IStrictEnergyHandler) be);
        registerBlockEntityEnergy(event, ModBlockEntities.LITOGRAFIA.get(),
                be -> (IStrictEnergyHandler) be);
        event.registerBlockEntity(Capabilities.Fluid.BLOCK, ModBlockEntities.LITOGRAFIA.get(),
                (be, direction) -> be.getWaterStorage());
        event.registerBlockEntity(Capabilities.Fluid.BLOCK, ModBlockEntities.WATER_SINK.get(),
                (be, direction) -> be.getWaterSource());
        event.registerBlockEntity(Capabilities.Energy.BLOCK, ModBlockEntities.FUEL_GENERATOR.get(),
                (be, direction) -> be.getEnergyPort());
        event.registerBlockEntity(Capabilities.Energy.BLOCK, ModBlockEntities.BASIC_SOLAR_GENERATOR.get(),
                (be, direction) -> be.getEnergyPort());
        event.registerBlockEntity(Capabilities.Energy.BLOCK, ModBlockEntities.ADVANCED_SOLAR_GENERATOR.get(),
                (be, direction) -> be.getEnergyPort());
        event.registerBlock(Capabilities.Energy.BLOCK,
                (level, pos, state, be, direction) -> new EnergyCablePort(level, pos, direction),
                ModBlocks.ENERGY_CABLE.get());
    }

    public static void registerBlockEntityEnergy(RegisterCapabilitiesEvent event,
          net.minecraft.world.level.block.entity.BlockEntityType<?> beType,
          java.util.function.Function<net.minecraft.world.level.block.entity.BlockEntity, IStrictEnergyHandler> provider) {
        event.registerBlockEntity(Capabilities.Energy.BLOCK, beType,
              (be, direction) -> EnergyCompat.wrap(provider.apply(be)));
    }

    public static void registerItemEnergy(RegisterCapabilitiesEvent event,
          net.minecraft.world.level.ItemLike item,
          java.util.function.Function<net.minecraft.world.item.ItemStack, IStrictEnergyHandler> provider) {
        event.registerItem(Capabilities.Energy.ITEM, (stack, ctx) -> EnergyCompat.wrap(provider.apply(stack)), item);
    }
}
