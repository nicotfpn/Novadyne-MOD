package com.novadyne;

import com.novadyne.common.menu.LitografiaMenu;
import com.novadyne.common.menu.MaceratorMenu;
import com.novadyne.common.menu.ProcessorMenu;
import com.novadyne.common.menu.WaferPressMenu;
import net.minecraft.core.registries.Registries;
import net.minecraft.world.inventory.MenuType;
import net.neoforged.neoforge.common.extensions.IMenuTypeExtension;
import net.neoforged.neoforge.registries.DeferredHolder;
import net.neoforged.neoforge.registries.DeferredRegister;

public final class ModMenuTypes {
    public static final DeferredRegister<MenuType<?>> MENU_TYPES =
            DeferredRegister.create(Registries.MENU, NovaDyneMod.MODID);

    public static final DeferredHolder<MenuType<?>, MenuType<MaceratorMenu>> MACERATOR =
            MENU_TYPES.register("macerator", () -> IMenuTypeExtension.create(MaceratorMenu::new));

    public static final DeferredHolder<MenuType<?>, MenuType<WaferPressMenu>> WAFER_PRESS =
            MENU_TYPES.register("wafer_press", () -> IMenuTypeExtension.create(WaferPressMenu::new));

    public static final DeferredHolder<MenuType<?>, MenuType<ProcessorMenu>> PROCESSOR =
            MENU_TYPES.register("processor", () -> IMenuTypeExtension.create(ProcessorMenu::new));

    public static final DeferredHolder<MenuType<?>, MenuType<LitografiaMenu>> LITOGRAFIA =
            MENU_TYPES.register("litografia", () -> IMenuTypeExtension.create(LitografiaMenu::new));

    private ModMenuTypes() {}
}
