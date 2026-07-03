package com.novadyne.items;

import java.util.function.Consumer;

import com.geckolib.animatable.GeoItem;
import com.geckolib.animatable.client.GeoRenderProvider;
import com.geckolib.animatable.instance.AnimatableInstanceCache;
import com.geckolib.animatable.manager.AnimatableManager;
import com.geckolib.util.GeckoLibUtil;
import com.novadyne.client.renderer.ExosuitTier1ArmorRenderer;
import com.novadyne.client.renderer.ExosuitTier1ItemRenderer;

import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.equipment.ArmorMaterials;
import net.minecraft.world.item.equipment.ArmorType;

public class ExosuitTier1Item extends Item implements GeoItem {
    private final AnimatableInstanceCache cache = GeckoLibUtil.createInstanceCache(this);

    public ExosuitTier1Item(Item.Properties properties) {
        super(properties.humanoidArmor(ArmorMaterials.IRON, ArmorType.CHESTPLATE));
    }

    @Override
    public void createGeoRenderer(Consumer<GeoRenderProvider> consumer) {
        consumer.accept(new GeoRenderProvider() {
            private ExosuitTier1ArmorRenderer armorRenderer;
            private ExosuitTier1ItemRenderer itemRenderer;

            @Override
            public ExosuitTier1ItemRenderer getGeoItemRenderer() {
                if (this.itemRenderer == null)
                    this.itemRenderer = new ExosuitTier1ItemRenderer();
                return this.itemRenderer;
            }

            @Override
            public ExosuitTier1ArmorRenderer getGeoArmorRenderer(ItemStack itemStack, EquipmentSlot slot) {
                if (this.armorRenderer == null)
                    this.armorRenderer = new ExosuitTier1ArmorRenderer();
                return this.armorRenderer;
            }
        });
    }

    @Override
    public void registerControllers(AnimatableManager.ControllerRegistrar controllers) {
    }

    @Override
    public AnimatableInstanceCache getAnimatableInstanceCache() {
        return this.cache;
    }
}
