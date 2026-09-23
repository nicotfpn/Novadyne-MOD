package com.novadyne.client.screen;

import com.novadyne.common.menu.LitografiaMenu;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.Identifier;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.client.gui.GuiGraphicsExtractor;

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

    @Override
    protected void extractLabels(GuiGraphicsExtractor graphics, int mouseX, int mouseY) {
        super.extractLabels(graphics, mouseX, mouseY);
        graphics.text(this.font, Component.translatable("gui.novadyne.water", this.menu.getWaterAmount(), 4000), 78, 67, 0xFF428CD0, false);
    }
}
