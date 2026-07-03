package com.novadyne.common.util;

import java.util.function.LongConsumer;
import net.minecraft.nbt.CompoundTag;

public final class NBTUtils {

    public static void setLongIfPresent(CompoundTag nbt, String key, LongConsumer setter) {
        if (nbt.contains(key)) {
            nbt.getLong(key).ifPresent(val -> setter.accept(val));
        }
    }

    public static void setLegacyEnergyIfPresent(CompoundTag nbt, String key, LongConsumer setter) {
        if (nbt.contains(key)) {
            nbt.getLong(key).ifPresent(val -> setter.accept(Math.max(0, val)));
        }
    }

    private NBTUtils() {}
}
