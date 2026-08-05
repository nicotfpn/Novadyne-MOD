package com.novadyne.client.screen;

import com.novadyne.common.menu.AbstractMachineMenu;
import net.minecraft.client.gui.GuiGraphicsExtractor;
import net.minecraft.client.gui.screens.inventory.AbstractContainerScreen;
import net.minecraft.client.renderer.RenderPipelines;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.Identifier;
import net.minecraft.world.entity.player.Inventory;


public abstract class AbstractMachineScreen<T extends AbstractMachineMenu<?>> extends AbstractContainerScreen<T> {
    private static final int PROGRESS_ARROW_WIDTH = 24;
    private static final int PROGRESS_ARROW_HEIGHT = 17;
    private static final int PROGRESS_ARROW_UV_X = 176;
    private static final int PROGRESS_ARROW_UV_Y = 0;
    private static final int ENERGY_BAR_WIDTH = 6;
    private static final int ENERGY_BAR_HEIGHT = 54;
    private static final int ENERGY_BAR_UV_X = 176;
    private static final int ENERGY_BAR_UV_Y = 17;

    private final Identifier texture;

    public AbstractMachineScreen(T menu, Inventory playerInventory, Component title, Identifier texture) {
        super(menu, playerInventory, title);
        this.texture = texture;
    }

    protected abstract int getProgressArrowX();

    protected abstract int getProgressArrowY();

    protected abstract int getEnergyBarX();

    protected abstract int getEnergyBarY();

    @Override
    public void extractBackground(GuiGraphicsExtractor graphics, int mouseX, int mouseY, float delta) {
        super.extractBackground(graphics, mouseX, mouseY, delta);

        int x = this.leftPos;
        int y = this.topPos;

        graphics.blit(RenderPipelines.GUI_TEXTURED, this.texture, x, y, 0, 0, this.imageWidth, this.imageHeight, 256, 256);

        int progress = this.menu.getProgress();
        int maxProgress = this.menu.getMaxProgress();
        if (maxProgress > 0 && progress > 0) {
            int progressScaled = (int) Math.ceil(PROGRESS_ARROW_WIDTH * progress / maxProgress);
            graphics.blit(RenderPipelines.GUI_TEXTURED, this.texture, x + getProgressArrowX(), y + getProgressArrowY(), PROGRESS_ARROW_UV_X, PROGRESS_ARROW_UV_Y, progressScaled, PROGRESS_ARROW_HEIGHT, 256, 256);
        }

        long energy = this.menu.getEnergy();
        long maxEnergy = this.menu.getMaxEnergy();
        if (maxEnergy > 0 && energy > 0) {
            int energyScaled = (int) Math.ceil(ENERGY_BAR_HEIGHT * energy / maxEnergy);
            graphics.blit(RenderPipelines.GUI_TEXTURED, this.texture, x + getEnergyBarX(), y + getEnergyBarY() + (ENERGY_BAR_HEIGHT - energyScaled), ENERGY_BAR_UV_X, ENERGY_BAR_UV_Y + (ENERGY_BAR_HEIGHT - energyScaled), ENERGY_BAR_WIDTH, energyScaled, 256, 256);
        }
    }

    @Override
    protected void extractLabels(GuiGraphicsExtractor graphics, int mouseX, int mouseY) {
        graphics.text(this.font, this.title, this.titleLabelX, this.titleLabelY, 0xFFFFFFFF, true);
        graphics.text(this.font, this.playerInventoryTitle, this.inventoryLabelX, this.inventoryLabelY, 0xFFFFFFFF, true);

        int x = this.leftPos;
        int y = this.topPos;
        if (mouseX >= x + getEnergyBarX() && mouseX < x + getEnergyBarX() + ENERGY_BAR_WIDTH && mouseY >= y + getEnergyBarY() && mouseY < y + getEnergyBarY() + ENERGY_BAR_HEIGHT) {
            Component tooltip = Component.translatable("tooltip.novadyne.energy", String.format("%,d", this.menu.getEnergy()), String.format("%,d", this.menu.getMaxEnergy()));
            graphics.setTooltipForNextFrame(this.font, tooltip, mouseX, mouseY);
        }
    }
}
