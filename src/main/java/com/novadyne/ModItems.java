package com.novadyne;

import com.novadyne.items.ExosuitTier1Item;
import net.minecraft.world.item.Item;
import net.neoforged.neoforge.registries.DeferredItem;
import net.neoforged.neoforge.registries.DeferredRegister;

public class ModItems {
    public static final DeferredRegister.Items ITEMS = DeferredRegister.createItems(NovaDyneMod.MODID);

    public static final DeferredItem<ExosuitTier1Item> EXOSUIT_TIER1 = ITEMS.registerItem("exosuit_tier1",
            props -> new ExosuitTier1Item(props.component(ModDataComponents.EXOSUIT_ENERGY.get(), 0L)));
}
