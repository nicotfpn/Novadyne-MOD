package com.novadyne.client;

import com.novadyne.ModMenuTypes;
import com.novadyne.NovaDyneMod;
import com.novadyne.client.screen.LitografiaScreen;
import com.novadyne.client.screen.MaceratorScreen;
import com.novadyne.client.screen.ProcessorScreen;
import com.novadyne.client.screen.WaferPressScreen;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.client.event.RegisterMenuScreensEvent;

@EventBusSubscriber(modid = NovaDyneMod.MODID, value = Dist.CLIENT)
public class ClientModEvents {

    @SubscribeEvent
    public static void registerScreens(RegisterMenuScreensEvent event) {
        event.register(ModMenuTypes.MACERATOR.get(), MaceratorScreen::new);
        event.register(ModMenuTypes.WAFER_PRESS.get(), WaferPressScreen::new);
        event.register(ModMenuTypes.PROCESSOR.get(), ProcessorScreen::new);
        event.register(ModMenuTypes.LITOGRAFIA.get(), LitografiaScreen::new);
    }
}
