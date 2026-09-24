package com.novadyne.client.screen;

import com.novadyne.common.menu.AbstractMachineMenu;
import net.minecraft.client.gui.GuiGraphicsExtractor;
import net.minecraft.client.gui.components.Button;
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
    private final Button[] sideButtons = new Button[6];
    private Button autoOutputButton;
    private static final String[] SIDE_NAMES = {"front", "back", "left", "right", "top", "bottom"};
    private static final String[] MODE_NAMES = {"off", "input", "output", "both"};
    private static final int[] MODE_COLORS = {0xFFFFFF, 0x439DFF, 0xFFA43A, 0xB475F2};
    // A cube net: top, left-front-right, bottom, back.
    private static final int[] SIDE_X = {222, 222, 197, 247, 222, 222};
    private static final int[] SIDE_Y = {48, 98, 48, 48, 23, 73};

    public AbstractMachineScreen(T menu, Inventory playerInventory, Component title, Identifier texture) {
        super(menu, playerInventory, title, 310, 166);
        this.texture = texture;
    }

    @Override
    protected void init() {
        super.init();
        for (int side = 0; side < sideButtons.length; side++) {
            int selected = side;
            sideButtons[side] = addRenderableWidget(Button.builder(sideSquare(side), button -> {
                if (minecraft != null && minecraft.gameMode != null)
                    minecraft.gameMode.handleInventoryButtonClick(menu.containerId, selected);
            }).bounds(leftPos + SIDE_X[side], topPos + SIDE_Y[side], 23, 23).build());
        }
        autoOutputButton = addRenderableWidget(Button.builder(autoLabel(), button -> {
            if (minecraft != null && minecraft.gameMode != null)
                minecraft.gameMode.handleInventoryButtonClick(menu.containerId, 6);
        }).bounds(leftPos + 182, topPos + 144, 120, 18).build());
    }

    @Override
    protected void containerTick() {
        super.containerTick();
        for (int side = 0; side < sideButtons.length; side++) sideButtons[side].setMessage(sideSquare(side));
        autoOutputButton.setMessage(autoLabel());
    }

    private Component sideLabel(int side) {
        return Component.translatable("gui.novadyne.side." + SIDE_NAMES[side]).append(": ")
                .append(Component.translatable("gui.novadyne.mode." + MODE_NAMES[menu.getItemMode(side)]));
    }

    private Component sideSquare(int side) {
        return Component.literal("■").withStyle(style -> style.withColor(MODE_COLORS[menu.getItemMode(side)]));
    }

    private Component autoLabel() {
        return Component.translatable("gui.novadyne.auto_output").append(": ")
                .append(Component.translatable(menu.isAutoOutput() ? "gui.novadyne.on" : "gui.novadyne.off"));
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

        graphics.blit(RenderPipelines.GUI_TEXTURED, this.texture, x, y, 0, 0, 176, this.imageHeight, 256, 256);
        graphics.fill(x + 176, y, x + imageWidth, y + imageHeight, 0xFF222A33);

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
        graphics.text(this.font, Component.translatable("gui.novadyne.item_sides"), 183, 9, 0xFFFFFFFF, true);
        graphics.text(this.font, Component.translatable("gui.novadyne.side_hint"), 183, 129, 0xFFB5BEC8, false);

        int x = this.leftPos;
        int y = this.topPos;
        if (mouseX >= x + getEnergyBarX() && mouseX < x + getEnergyBarX() + ENERGY_BAR_WIDTH && mouseY >= y + getEnergyBarY() && mouseY < y + getEnergyBarY() + ENERGY_BAR_HEIGHT) {
            Component tooltip = Component.translatable("tooltip.novadyne.energy", String.format("%,d", this.menu.getEnergy()), String.format("%,d", this.menu.getMaxEnergy()));
            graphics.setTooltipForNextFrame(this.font, tooltip, mouseX, mouseY);
        }
        for (int side = 0; side < sideButtons.length; side++) {
            if (mouseX >= x + SIDE_X[side] && mouseX < x + SIDE_X[side] + 23
                    && mouseY >= y + SIDE_Y[side] && mouseY < y + SIDE_Y[side] + 23) {
                graphics.setTooltipForNextFrame(this.font, sideLabel(side), mouseX, mouseY);
            }
        }
    }
}
