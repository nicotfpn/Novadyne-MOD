package com.novadyne.client.renderer;

import java.util.List;
import com.geckolib.renderer.GeoArmorRenderer;
import com.geckolib.renderer.base.GeoRenderState;
import com.novadyne.ModDataComponents;
import com.novadyne.client.model.ExosuitTier1ArmorModel;
import com.novadyne.items.ExosuitTier1Item;
import net.minecraft.client.renderer.entity.state.HumanoidRenderState;
import net.minecraft.world.entity.EquipmentSlot;

public class ExosuitTier1ArmorRenderer extends GeoArmorRenderer<ExosuitTier1Item, HumanoidRenderState> {
    public ExosuitTier1ArmorRenderer() { super(new ExosuitTier1ArmorModel()); }

    @Override
    public List<ArmorSegment> getSegmentsForSlot(HumanoidRenderState renderState, EquipmentSlot slot) {
        List<ArmorSegment> segments = super.getSegmentsForSlot(renderState, slot);
        if (slot == EquipmentSlot.CHEST && !segments.contains(ArmorSegment.HEAD)) {
            segments = new java.util.ArrayList<>(segments);
            segments.add(ArmorSegment.HEAD);
        }
        return segments;
    }

    @Override
    public void captureDefaultRenderState(ExosuitTier1Item animatable, RenderData renderData, HumanoidRenderState renderState, float partialTick) {
        super.captureDefaultRenderState(animatable, renderData, renderState, partialTick);
        long energy = renderData.itemStack().getOrDefault(ModDataComponents.EXOSUIT_ENERGY.get(), 0L);
        ((GeoRenderState) renderState).addGeckolibData(ExosuitTier1ArmorModel.EXOSUIT_ENERGY, energy);
    }
}
