package com.novadyne.client.screen;

import com.novadyne.common.menu.AbstractMachineMenu;
import net.minecraft.client.gui.GuiGraphicsExtractor;
import net.minecraft.client.gui.screens.inventory.AbstractContainerScreen;
import net.minecraft.client.renderer.RenderPipelines;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.Identifier;
import net.minecraft.world.entity.player.Inventory;

import java.util.List;

public abstract class AbstractMachineScreen<T extends AbstractMachineMenu<?>> extends AbstractContainerScreen<T> {
    private final Identifier texture;

    public AbstractMachineScreen(T menu, Inventory playerInventory, Component title, Identifier texture) {
        super(menu, playerInventory, title);
        this.texture = texture;
    }

    @Override
    public void extractBackground(GuiGraphicsExtractor graphics, int mouseX, int mouseY, float delta) {
        super.extractBackground(graphics, mouseX, mouseY, delta);

        int x = this.leftPos;
        int y = this.topPos;

        graphics.blit(RenderPipelines.GUI_TEXTURED, this.texture, x, y, 0, 0, this.imageWidth, this.imageHeight, 256, 256);

        int progress = this.menu.getProgress();
        int maxProgress = this.menu.getMaxProgress();
        if (maxProgress > 0 && progress > 0) {
            int progressScaled = (int) Math.ceil(24.0 * progress / maxProgress);
            graphics.blit(RenderPipelines.GUI_TEXTURED, this.texture, x + 79, y + 34, 176, 0, progressScaled, 17, 256, 256);
        }

        long energy = this.menu.getEnergy();
        long maxEnergy = this.menu.getMaxEnergy();
        if (maxEnergy > 0 && energy > 0) {
            int energyScaled = (int) Math.ceil(50.0 * energy / maxEnergy);
            graphics.blit(RenderPipelines.GUI_TEXTURED, this.texture, x + 18, y + 17 + (50 - energyScaled), 176, 20 + (50 - energyScaled), 6, energyScaled, 256, 256);
        }
    }

    @Override
    protected void extractLabels(GuiGraphicsExtractor graphics, int mouseX, int mouseY) {
        super.extractLabels(graphics, mouseX, mouseY);

        int x = this.leftPos;
        int y = this.topPos;
        if (mouseX >= x + 18 && mouseX < x + 18 + 6 && mouseY >= y + 17 && mouseY < y + 17 + 50) {
            Component tooltip = Component.translatable("tooltip.novadyne.energy", this.menu.getEnergy(), this.menu.getMaxEnergy());
            graphics.setTooltipForNextFrame(this.font, tooltip, mouseX - x, mouseY - y);
        }
    }
}
