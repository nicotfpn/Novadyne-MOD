package com.novadyne.client.screen;

import com.novadyne.common.menu.ProcessorMenu;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.Identifier;
import net.minecraft.world.entity.player.Inventory;

public class ProcessorScreen extends AbstractMachineScreen<ProcessorMenu> {
    private static final Identifier TEXTURE = Identifier.fromNamespaceAndPath("novadyne", "textures/gui/processor.png");

    public ProcessorScreen(ProcessorMenu menu, Inventory playerInventory, Component title) {
        super(menu, playerInventory, title, TEXTURE);
    }

    @Override
    protected int getProgressArrowX() {
        return 91;
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
