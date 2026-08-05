package com.novadyne.client.screen;

import com.novadyne.common.menu.MaceratorMenu;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.Identifier;
import net.minecraft.world.entity.player.Inventory;

public class MaceratorScreen extends AbstractMachineScreen<MaceratorMenu> {
    private static final Identifier TEXTURE = Identifier.fromNamespaceAndPath("novadyne", "textures/gui/macerator.png");

    public MaceratorScreen(MaceratorMenu menu, Inventory playerInventory, Component title) {
        super(menu, playerInventory, title, TEXTURE);
    }
}
