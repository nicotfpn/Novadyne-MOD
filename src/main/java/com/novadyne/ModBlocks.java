package com.novadyne;

import com.novadyne.common.block.LitografiaBlock;
import com.novadyne.common.block.MaceratorBlock;
import com.novadyne.common.block.ProcessorBlock;
import com.novadyne.common.block.WaferPressBlock;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.neoforged.neoforge.registries.DeferredBlock;
import net.neoforged.neoforge.registries.DeferredRegister;

public final class ModBlocks {
    public static final DeferredRegister.Blocks BLOCKS = DeferredRegister.createBlocks(NovaDyneMod.MODID);

    public static final DeferredBlock<MaceratorBlock> MACERATOR =
            BLOCKS.registerBlock("macerator", MaceratorBlock::new,
                    props -> props.of().strength(3.5F, 6.0F).requiresCorrectToolForDrops());
    public static final DeferredBlock<WaferPressBlock> WAFER_PRESS =
            BLOCKS.registerBlock("wafer_press", WaferPressBlock::new,
                    props -> props.of().strength(3.5F, 6.0F).requiresCorrectToolForDrops());
    public static final DeferredBlock<ProcessorBlock> PROCESSOR =
            BLOCKS.registerBlock("processor", ProcessorBlock::new,
                    props -> props.of().strength(3.5F, 6.0F).requiresCorrectToolForDrops());
    public static final DeferredBlock<LitografiaBlock> LITOGRAFIA =
            BLOCKS.registerBlock("litografia", LitografiaBlock::new,
                    props -> props.of().strength(3.5F, 6.0F).requiresCorrectToolForDrops());

    private ModBlocks() {}
}
