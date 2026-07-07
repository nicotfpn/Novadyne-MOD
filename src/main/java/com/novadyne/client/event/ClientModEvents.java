package com.novadyne.client.event;

import com.novadyne.NovaDyneMod;
import com.novadyne.client.renderer.NovaDyneArmorRenderer;
import net.minecraft.client.model.geom.ModelLayers;
import net.minecraft.client.model.player.PlayerModel;
import net.minecraft.client.player.AbstractClientPlayer;
import net.minecraft.client.renderer.entity.ArmorModelSet;
import net.minecraft.client.renderer.entity.player.AvatarRenderer;
import net.minecraft.world.entity.player.PlayerModelType;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.client.event.EntityRenderersEvent;

@EventBusSubscriber(value = Dist.CLIENT, modid = NovaDyneMod.MODID)
public final class ClientModEvents {

    private ClientModEvents() {}

    @SubscribeEvent
    public static void onAddLayers(EntityRenderersEvent.AddLayers event) {
        for (PlayerModelType skin : event.getSkins()) {
            AvatarRenderer<AbstractClientPlayer> renderer = event.getPlayerRenderer(skin);
            if (renderer != null) {
                boolean slim = skin == PlayerModelType.SLIM;
                ArmorModelSet<PlayerModel> armorModelSet = ArmorModelSet.bake(
                        slim ? ModelLayers.PLAYER_SLIM_ARMOR : ModelLayers.PLAYER_ARMOR,
                        event.getEntityModels(),
                        part -> new PlayerModel(part, slim)
                );
                renderer.addLayer(new NovaDyneArmorRenderer(
                        renderer, armorModelSet, event.getContext().getEquipmentRenderer(), slim
                ));
            }
        }
    }
}
