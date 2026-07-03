package com.novadyne.client.model;

import com.geckolib.model.GeoModel;
import com.geckolib.renderer.base.GeoRenderState;
import com.novadyne.NovaDyneMod;
import com.novadyne.items.ExosuitTier1Item;

import net.minecraft.resources.Identifier;

public class ExosuitTier1ArmorModel extends GeoModel<ExosuitTier1Item> {
    private static final Identifier MODEL = Identifier.fromNamespaceAndPath(NovaDyneMod.MODID, "exosuit_tier1");
    private static final Identifier TEXTURE = Identifier.fromNamespaceAndPath(NovaDyneMod.MODID, "textures/armor/exosuit_tier1.png");

    @Override
    public Identifier getModelResource(GeoRenderState renderState) {
        return MODEL;
    }

    @Override
    public Identifier getTextureResource(GeoRenderState renderState) {
        return TEXTURE;
    }

    @Override
    public Identifier getAnimationResource(ExosuitTier1Item animatable) {
        return null;
    }
}
