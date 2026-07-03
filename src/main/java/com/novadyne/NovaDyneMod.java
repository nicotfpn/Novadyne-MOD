package com.novadyne;

import org.slf4j.Logger;
import com.mojang.logging.LogUtils;
import com.novadyne.common.integration.energy.NovadyneCapabilities;
import com.novadyne.items.ExosuitTier1Item;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.player.Player;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.common.Mod;
import net.neoforged.neoforge.common.NeoForge;
import net.neoforged.neoforge.event.entity.living.LivingIncomingDamageEvent;

@Mod(NovaDyneMod.MODID)
public class NovaDyneMod {
    public static final String MODID = "novadyne";
    public static final Logger LOGGER = LogUtils.getLogger();

    public NovaDyneMod(IEventBus modEventBus) {
        ModItems.ITEMS.register(modEventBus);
        ModCreativeTabs.CREATIVE_MODE_TABS.register(modEventBus);
        ModDataComponents.DATA_COMPONENTS.register(modEventBus);
        modEventBus.addListener(NovadyneCapabilities::onRegisterCapabilities);
        NeoForge.EVENT_BUS.addListener(NovaDyneMod::onLivingIncomingDamage);
    }

    private static void onLivingIncomingDamage(LivingIncomingDamageEvent event) {
        if (!(event.getEntity() instanceof Player player)) return;
        var chestStack = player.getItemBySlot(EquipmentSlot.CHEST);
        if (!(chestStack.getItem() instanceof ExosuitTier1Item)) return;

        long energy = chestStack.getOrDefault(ModDataComponents.EXOSUIT_ENERGY.get(), 0L);
        if (energy <= 0) return;

        float damage = event.getAmount();
        if (damage <= 0) return;

        long toConsume = Math.min(Math.round(damage), energy);
        float remaining = damage - toConsume;

        chestStack.set(ModDataComponents.EXOSUIT_ENERGY.get(), energy - toConsume);

        if (remaining <= 0.0f) {
            event.setCanceled(true);
        } else {
            event.setAmount(remaining);
        }
    }
}
