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
        // HACK: The exosuit is a single-piece chestplate item, but its model includes the
        // full body (head included). We force-add HEAD so the entire exosuit renders even
        // when the player isn't wearing a separate helmet. Do not remove or gate this
        // behind a helmet-equip check without understanding the model design.
        if (slot == EquipmentSlot.CHEST && !segments.contains(ArmorSegment.HEAD)) {
            segments = new java.util.ArrayList<>(segments);
            segments.add(ArmorSegment.HEAD);
        }
        return segments;
    }
}
