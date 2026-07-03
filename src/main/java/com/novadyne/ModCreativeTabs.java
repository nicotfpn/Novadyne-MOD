package com.novadyne;

import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.item.ItemStack;
import net.neoforged.neoforge.registries.DeferredHolder;
import net.neoforged.neoforge.registries.DeferredRegister;

public class ModCreativeTabs {
    public static final DeferredRegister<CreativeModeTab> CREATIVE_MODE_TABS =
            DeferredRegister.create(Registries.CREATIVE_MODE_TAB, NovaDyneMod.MODID);

    public static final DeferredHolder<CreativeModeTab, CreativeModeTab> NOVADYNE_TAB =
            CREATIVE_MODE_TABS.register("novadyne", () -> CreativeModeTab.builder()
                    .title(Component.literal("NovaDyne"))
                    .icon(() -> new ItemStack(ModItems.EXOSUIT_TIER1.get()))
                    .displayItems((parameters, output) -> {
                        output.accept(new ItemStack(ModItems.EXOSUIT_TIER1.get()));
                    }).build());
}
