package com.novadyne.client.screen;

import com.novadyne.common.menu.WaferPressMenu;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.Identifier;
import net.minecraft.world.entity.player.Inventory;

public class WaferPressScreen extends AbstractMachineScreen<WaferPressMenu> {
    private static final Identifier TEXTURE = Identifier.fromNamespaceAndPath("novadyne", "textures/gui/wafer_press.png");

    public WaferPressScreen(WaferPressMenu menu, Inventory playerInventory, Component title) {
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
