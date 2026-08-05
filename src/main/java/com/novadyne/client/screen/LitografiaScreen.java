package com.novadyne.client.screen;

import com.novadyne.common.menu.LitografiaMenu;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.Identifier;
import net.minecraft.world.entity.player.Inventory;

public class LitografiaScreen extends AbstractMachineScreen<LitografiaMenu> {
    private static final Identifier TEXTURE = Identifier.fromNamespaceAndPath("novadyne", "textures/gui/furnace.png");

    public LitografiaScreen(LitografiaMenu menu, Inventory playerInventory, Component title) {
        super(menu, playerInventory, title, TEXTURE);
    }
}
