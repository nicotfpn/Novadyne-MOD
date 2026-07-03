package com.novadyne;

import java.util.Map;

import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.Identifier;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.item.equipment.ArmorMaterial;
import net.minecraft.world.item.equipment.ArmorType;
import net.minecraft.world.item.equipment.EquipmentAsset;
import net.minecraft.world.item.equipment.EquipmentAssets;
import net.minecraft.tags.ItemTags;

public class ModArmorMaterials {
    public static final ResourceKey<EquipmentAsset> EXOSUIT_TIER1_ASSET =
            ResourceKey.create(EquipmentAssets.ROOT_ID, Identifier.fromNamespaceAndPath(NovaDyneMod.MODID, "exosuit_tier1"));

    public static final ArmorMaterial EXOSUIT_TIER1 = new ArmorMaterial(
            15,
            Map.of(
                    ArmorType.HELMET, 3,
                    ArmorType.CHESTPLATE, 7,
                    ArmorType.LEGGINGS, 5,
                    ArmorType.BOOTS, 3
            ),
            12,
            SoundEvents.ARMOR_EQUIP_IRON,
            1.0F,
            0.0F,
            ItemTags.REPAIRS_IRON_ARMOR,
            EXOSUIT_TIER1_ASSET
    );
}
