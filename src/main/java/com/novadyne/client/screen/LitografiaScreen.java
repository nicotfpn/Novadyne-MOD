package com.novadyne.client.screen;

import com.novadyne.common.menu.LitografiaMenu;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.Identifier;
import net.minecraft.world.entity.player.Inventory;

public class LitografiaScreen extends AbstractMachineScreen<LitografiaMenu> {
    private static final Identifier TEXTURE = Identifier.fromNamespaceAndPath("novadyne", "textures/gui/litografia.png");

    public LitografiaScreen(LitografiaMenu menu, Inventory playerInventory, Component title) {
        super(menu, playerInventory, title, TEXTURE);
    }

    @Override
    protected int getProgressArrowX() {
        return 79;
    }

    @Override
    protected int getProgressArrowY() {
        return 39;
    }

    @Override
    protected int getEnergyBarX() {
        return 11;
    }

    @Override
    protected int getEnergyBarY() {
        return 20;
    }
}
