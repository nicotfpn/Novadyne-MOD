package com.novadyne;

import org.slf4j.Logger;
import com.mojang.logging.LogUtils;
import com.novadyne.common.integration.energy.NovadyneCapabilities;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.common.Mod;

@Mod(NovaDyneMod.MODID)
public class NovaDyneMod {
    public static final String MODID = "novadyne";
    public static final Logger LOGGER = LogUtils.getLogger();

    public NovaDyneMod(IEventBus modEventBus) {
        ModItems.ITEMS.register(modEventBus);
        ModCreativeTabs.CREATIVE_MODE_TABS.register(modEventBus);
        ModDataComponents.DATA_COMPONENTS.register(modEventBus);
        modEventBus.addListener(NovadyneCapabilities::onRegisterCapabilities);
    }
}
