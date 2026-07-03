package com.novadyne;

import com.mojang.serialization.Codec;
import net.minecraft.core.component.DataComponentType;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.codec.ByteBufCodecs;
import net.neoforged.neoforge.registries.DeferredHolder;
import net.neoforged.neoforge.registries.DeferredRegister;

public final class ModDataComponents {
    public static final DeferredRegister.DataComponents DATA_COMPONENTS = DeferredRegister.createDataComponents(
            Registries.DATA_COMPONENT_TYPE, NovaDyneMod.MODID);

    public static final DeferredHolder<DataComponentType<?>, DataComponentType<Long>> EXOSUIT_ENERGY =
            DATA_COMPONENTS.registerComponentType(
                    "exosuit_energy",
                    builder -> builder
                            .persistent(Codec.LONG)
                            .networkSynchronized(ByteBufCodecs.VAR_LONG));

    private ModDataComponents() {}
}
