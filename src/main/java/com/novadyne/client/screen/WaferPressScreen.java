package com.novadyne.client.screen;

import com.novadyne.common.menu.WaferPressMenu;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.Identifier;
import net.minecraft.world.entity.player.Inventory;

public class WaferPressScreen extends AbstractMachineScreen<WaferPressMenu> {
    private static final Identifier TEXTURE = Identifier.fromNamespaceAndPath("novadyne", "textures/gui/macerator.png");

    public WaferPressScreen(WaferPressMenu menu, Inventory playerInventory, Component title) {
        super(menu, playerInventory, title, TEXTURE);
    }
}
