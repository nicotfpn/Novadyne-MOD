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

    @Override
    protected int getProgressArrowX() {
        return 77;
    }

    @Override
    protected int getProgressArrowY() {
        return 21;
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
