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
}
