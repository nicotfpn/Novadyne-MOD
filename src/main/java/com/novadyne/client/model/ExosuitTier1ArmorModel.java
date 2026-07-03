package com.novadyne.client.model;

import com.geckolib.constant.dataticket.DataTicket;
import com.geckolib.model.GeoModel;
import com.geckolib.renderer.base.GeoRenderState;
import com.novadyne.NovaDyneMod;
import com.novadyne.items.ExosuitTier1Item;

import net.minecraft.resources.Identifier;

public class ExosuitTier1ArmorModel extends GeoModel<ExosuitTier1Item> {
    public static final DataTicket<Long> EXOSUIT_ENERGY = DataTicket.create("exosuit_energy", Long.class);

    private static final Identifier MODEL = Identifier.fromNamespaceAndPath(NovaDyneMod.MODID, "exosuit_tier1");
    private static final Identifier TEXTURE = Identifier.fromNamespaceAndPath(NovaDyneMod.MODID, "textures/armor/exosuit_tier1.png");
    private static final Identifier TEXTURE_UNPOWERED = Identifier.fromNamespaceAndPath(NovaDyneMod.MODID, "textures/armor/exosuit_tier1_unpowered.png");

    @Override
    public Identifier getModelResource(GeoRenderState renderState) {
        return MODEL;
    }

    @Override
    public Identifier getTextureResource(GeoRenderState renderState) {
        Long energy = renderState.getGeckolibData(EXOSUIT_ENERGY);
        return energy != null && energy > 0 ? TEXTURE : TEXTURE_UNPOWERED;
    }

    @Override
    public Identifier getAnimationResource(ExosuitTier1Item animatable) {
        return null;
    }
}
