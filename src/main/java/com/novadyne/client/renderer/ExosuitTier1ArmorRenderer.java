package com.novadyne.client.renderer;

import java.util.List;

import com.geckolib.renderer.GeoArmorRenderer;
import com.novadyne.client.model.ExosuitTier1ArmorModel;
import com.novadyne.items.ExosuitTier1Item;

import net.minecraft.client.renderer.entity.state.HumanoidRenderState;
import net.minecraft.world.entity.EquipmentSlot;

public class ExosuitTier1ArmorRenderer extends GeoArmorRenderer<ExosuitTier1Item, HumanoidRenderState> {
    public ExosuitTier1ArmorRenderer() {
        super(new ExosuitTier1ArmorModel());
    }

    @Override
    public List<ArmorSegment> getSegmentsForSlot(HumanoidRenderState renderState, EquipmentSlot slot) {
        List<ArmorSegment> segments = super.getSegmentsForSlot(renderState, slot);
        if (slot == EquipmentSlot.CHEST && !segments.contains(ArmorSegment.HEAD)) {
            segments = new java.util.ArrayList<>(segments);
            segments.add(ArmorSegment.HEAD);
        }
        return segments;
    }
}
