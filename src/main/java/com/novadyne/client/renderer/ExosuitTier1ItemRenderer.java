package com.novadyne.client.renderer;

import com.geckolib.renderer.GeoItemRenderer;
import com.novadyne.client.model.ExosuitTier1ArmorModel;
import com.novadyne.items.ExosuitTier1Item;

public class ExosuitTier1ItemRenderer extends GeoItemRenderer<ExosuitTier1Item> {
    public ExosuitTier1ItemRenderer() {
        super(new ExosuitTier1ArmorModel());
    }
}
