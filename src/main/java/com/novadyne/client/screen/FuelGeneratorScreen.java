package com.novadyne.client.screen;

import com.novadyne.common.menu.FuelGeneratorMenu;
import net.minecraft.client.gui.GuiGraphicsExtractor;
import net.minecraft.client.gui.screens.inventory.AbstractContainerScreen;
import net.minecraft.client.renderer.RenderPipelines;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.Identifier;
import net.minecraft.world.entity.player.Inventory;

public class FuelGeneratorScreen extends AbstractContainerScreen<FuelGeneratorMenu> {
    private static final Identifier TEXTURE = Identifier.withDefaultNamespace("textures/gui/container/furnace.png");

    public FuelGeneratorScreen(FuelGeneratorMenu menu, Inventory inventory, Component title) {
        super(menu, inventory, title);
    }

    @Override public void extractBackground(GuiGraphicsExtractor graphics, int mouseX, int mouseY, float delta) {
        super.extractBackground(graphics, mouseX, mouseY, delta);
        graphics.blit(RenderPipelines.GUI_TEXTURED, TEXTURE, leftPos, topPos, 0, 0, imageWidth, imageHeight, 256, 256);
        int remaining = menu.getBurnRemaining();
        int total = menu.getBurnTotal();
        if (total > 0 && remaining > 0) {
            int height = Math.max(1, 14 * remaining / total);
            graphics.blit(RenderPipelines.GUI_TEXTURED, TEXTURE, leftPos + 56, topPos + 36 + (14 - height),
                    176, 14 - height, 14, height, 256, 256);
        }
    }

    @Override protected void extractLabels(GuiGraphicsExtractor graphics, int mouseX, int mouseY) {
        graphics.text(font, title, titleLabelX, titleLabelY, 0xFFFFFFFF, true);
        graphics.text(font, playerInventoryTitle, inventoryLabelX, inventoryLabelY, 0xFFFFFFFF, true);
        graphics.text(font, Component.translatable("gui.novadyne.fe_stored", menu.getEnergy(), menu.getCapacity()), 67, 67, 0xFF404040, false);
    }
}
