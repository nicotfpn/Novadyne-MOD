package com.novadyne.test;

import com.novadyne.ModBlocks;
import com.novadyne.ModItems;
import com.novadyne.NovaDyneMod;
import com.novadyne.api.energy.Action;
import com.novadyne.common.blockentity.AbstractMachineBlockEntity;
import com.novadyne.common.blockentity.LitografiaBlockEntity;
import com.novadyne.common.blockentity.MaceratorBlockEntity;
import com.novadyne.common.blockentity.ProcessorBlockEntity;
import com.novadyne.common.blockentity.TestPowerHubBlockEntity;
import com.novadyne.common.blockentity.WaferPressBlockEntity;
import com.novadyne.common.blockentity.WaterSinkBlockEntity;
import com.novadyne.common.blockentity.FuelGeneratorBlockEntity;
import com.novadyne.common.blockentity.SolarGeneratorBlockEntity;
import com.novadyne.common.block.DirectionalConduitBlock;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.neoforged.neoforge.registries.DeferredRegister;
import net.neoforged.neoforge.transfer.item.ItemResource;
import net.neoforged.neoforge.transfer.fluid.FluidResource;
import net.minecraft.world.level.material.Fluids;
import net.neoforged.neoforge.transfer.transaction.Transaction;

import java.util.function.Consumer;

/** Small server-side checks that can run on GitHub Actions without a game client. */
public final class CoreSmokeTests {
    public static final DeferredRegister<Consumer<GameTestHelper>> FUNCTIONS =
            DeferredRegister.create(BuiltInRegistries.TEST_FUNCTION, NovaDyneMod.MODID);

    static {
        FUNCTIONS.register("items", () -> CoreSmokeTests::items);
        FUNCTIONS.register("energy_and_outputs", () -> CoreSmokeTests::energyAndOutputs);
        FUNCTIONS.register("production_chain", () -> CoreSmokeTests::productionChain);
        FUNCTIONS.register("lithography", () -> CoreSmokeTests::lithography);
        FUNCTIONS.register("test_power_hub", () -> CoreSmokeTests::testPowerHub);
        FUNCTIONS.register("water_pipe_lithography", () -> CoreSmokeTests::waterPipeLithography);
        FUNCTIONS.register("generators", () -> CoreSmokeTests::generators);
        FUNCTIONS.register("conduit_connections", () -> CoreSmokeTests::conduitConnections);
        FUNCTIONS.register("energy_cable_network", () -> CoreSmokeTests::energyCableNetwork);
        FUNCTIONS.register("fuel_inventory_edge_cases", () -> CoreSmokeTests::fuelInventoryEdgeCases);
        FUNCTIONS.register("solar_cable_network", () -> CoreSmokeTests::solarCableNetwork);
    }

    private CoreSmokeTests() {}

    private static void check(boolean condition, String message) {
        if (!condition) throw new IllegalStateException(message);
    }

    private static void put(AbstractMachineBlockEntity machine, int slot, Item item) {
        try (Transaction tx = Transaction.openRoot()) {
            check(machine.getInventory().insert(slot, ItemResource.of(new ItemStack(item)), 1, tx) == 1,
                    "Could not fill machine slot " + slot);
            tx.commit();
        }
    }

    private static ItemStack stack(AbstractMachineBlockEntity machine, int slot) {
        return machine.getInventory().getResource(slot).toStack(machine.getInventory().getAmountAsInt(slot));
    }

    private static void tick(AbstractMachineBlockEntity machine, int count) {
        for (int i = 0; i < count; i++) machine.tickServer();
    }

    private static void items(GameTestHelper helper) {
        helper.succeedIf(() -> {
            Item[] items = {
                    ModItems.PURE_SILICON.get(), ModItems.PART_SILICON_WAFER.get(), ModItems.CERAMIC_POWDER.get(),
                    ModItems.PART_COPPER_LAYER.get(), ModItems.PART_BASE_WAFER.get(),
                    ModItems.STACKED_ELECTRONIC_CIRCUIT.get(), ModItems.PART_ELECTRONIC_DIRTY_SILICON_WAFER.get(),
                    ModItems.PART_ELECTRONIC_FAILED_SILICON_WAFER.get(), ModItems.PART_ELECTRONIC_ETCHED_SILICON_WAFER.get(),
                    ModItems.VALVE_TIER_1.get(), ModItems.VALVE_TIER_2.get(), ModItems.VALVE_TIER_3.get(),
                    ModItems.VALVE_TIER_4.get(), ModItems.VALVE_TIER_5.get(), ModItems.VALVE_TIER_6.get(),
                    ModItems.VALVE_TIER_7.get(), ModItems.MACERATOR.get(), ModItems.WAFER_PRESS.get(),
                    ModItems.PROCESSOR.get(), ModItems.LITOGRAFIA.get(),
                    ModItems.WATER_SINK.get(), ModItems.FLUID_PIPE.get(), ModItems.ENERGY_CABLE.get(), ModItems.FUEL_GENERATOR.get(),
                    ModItems.BASIC_SOLAR_GENERATOR.get(), ModItems.ADVANCED_SOLAR_GENERATOR.get()
            };
            for (Item item : items) {
                check(BuiltInRegistries.ITEM.getKey(item).getNamespace().equals(NovaDyneMod.MODID),
                        "Unregistered item: " + item);
            }
            check(ModBlocks.MACERATOR.get() != null && ModBlocks.WAFER_PRESS.get() != null
                    && ModBlocks.PROCESSOR.get() != null && ModBlocks.LITOGRAFIA.get() != null
                    && ModBlocks.TEST_POWER_HUB.get() != null && ModBlocks.WATER_SINK.get() != null
                    && ModBlocks.FLUID_PIPE.get() != null && ModBlocks.ENERGY_CABLE.get() != null && ModBlocks.FUEL_GENERATOR.get() != null
                    && ModBlocks.BASIC_SOLAR_GENERATOR.get() != null
                    && ModBlocks.ADVANCED_SOLAR_GENERATOR.get() != null,
                    "Missing machine block");
        });
    }

    private static void energyAndOutputs(GameTestHelper helper) {
        helper.succeedIf(() -> {
            MaceratorBlockEntity machine = new MaceratorBlockEntity(BlockPos.ZERO, ModBlocks.MACERATOR.get().defaultBlockState());
            put(machine, 0, Items.CLAY_BALL);
            tick(machine, 130);
            check(machine.getProgress() == 0 && stack(machine, 0).is(Items.CLAY_BALL),
                    "Machine processed without energy");
            check(machine.insertExternalEnergy(0, 10_000, Action.EXECUTE) == 0, "External energy rejected");
            check(machine.extractExternalEnergy(0, 100, Action.EXECUTE) == 0, "External consumer drained machine");
            put(machine, 1, Items.COBBLESTONE);
            tick(machine, 130);
            check(stack(machine, 0).is(Items.CLAY_BALL) && machine.getEnergy(0) == 10_000,
                    "Blocked output consumed input or energy");
        });
    }

    private static void productionChain(GameTestHelper helper) {
        helper.succeedIf(() -> {
            MaceratorBlockEntity macerator = new MaceratorBlockEntity(BlockPos.ZERO, ModBlocks.MACERATOR.get().defaultBlockState());
            macerator.setEnergy(0, 10_000);
            put(macerator, 0, Items.CLAY_BALL);
            tick(macerator, MaceratorBlockEntity.MAX_PROGRESS);
            check(stack(macerator, 1).is(ModItems.CERAMIC_POWDER.get()), "Macerator failed");

            WaferPressBlockEntity press = new WaferPressBlockEntity(BlockPos.ZERO, ModBlocks.WAFER_PRESS.get().defaultBlockState());
            press.setEnergy(0, 15_000);
            put(press, 0, ModItems.PURE_SILICON.get());
            tick(press, WaferPressBlockEntity.MAX_PROGRESS);
            check(stack(press, 1).is(ModItems.PART_SILICON_WAFER.get()), "Wafer Press failed");

            ProcessorBlockEntity processor = new ProcessorBlockEntity(BlockPos.ZERO, ModBlocks.PROCESSOR.get().defaultBlockState());
            processor.setEnergy(0, 25_000);
            put(processor, 0, ModItems.PART_SILICON_WAFER.get());
            put(processor, 1, ModItems.PART_COPPER_LAYER.get());
            put(processor, 2, ModItems.PART_BASE_WAFER.get());
            tick(processor, ProcessorBlockEntity.MAX_PROGRESS);
            check(stack(processor, 3).is(ModItems.STACKED_ELECTRONIC_CIRCUIT.get()), "Processor failed");

            MaceratorBlockEntity recycle = new MaceratorBlockEntity(BlockPos.ZERO, ModBlocks.MACERATOR.get().defaultBlockState());
            recycle.setEnergy(0, 10_000);
            put(recycle, 0, ModItems.PART_ELECTRONIC_FAILED_SILICON_WAFER.get());
            put(recycle, 1, ModItems.PART_COPPER_LAYER.get());
            tick(recycle, MaceratorBlockEntity.MAX_PROGRESS);
            check(stack(recycle, 0).is(ModItems.PART_ELECTRONIC_FAILED_SILICON_WAFER.get()),
                    "Random recycling started with occupied output");
        });
    }

    private static void lithography(GameTestHelper helper) {
        helper.succeedIf(() -> {
            LitografiaBlockEntity cleaner = new LitografiaBlockEntity(BlockPos.ZERO, ModBlocks.LITOGRAFIA.get().defaultBlockState());
            cleaner.setEnergy(0, 20_000);
            put(cleaner, 0, ModItems.PART_ELECTRONIC_DIRTY_SILICON_WAFER.get());
            put(cleaner, 1, Items.WATER_BUCKET);
            tick(cleaner, LitografiaBlockEntity.MAX_PROGRESS);
            check(stack(cleaner, 3).is(ModItems.PART_ELECTRONIC_ETCHED_SILICON_WAFER.get()), "Cleaning output missing");
            check(stack(cleaner, 1).is(Items.BUCKET), "Empty bucket missing from bucket slot");

            LitografiaBlockEntity engraver = new LitografiaBlockEntity(BlockPos.ZERO, ModBlocks.LITOGRAFIA.get().defaultBlockState());
            engraver.setEnergy(0, 20_000);
            put(engraver, 0, ModItems.STACKED_ELECTRONIC_CIRCUIT.get());
            put(engraver, 2, ModItems.VALVE_TIER_7.get());
            tick(engraver, LitografiaBlockEntity.MAX_PROGRESS);
            check(engraver.getValveTier() == 7, "Valve tier was not applied");
            check(stack(engraver, 3).is(ModItems.PART_ELECTRONIC_DIRTY_SILICON_WAFER.get())
                            || stack(engraver, 3).is(ModItems.PART_ELECTRONIC_FAILED_SILICON_WAFER.get()),
                    "Engraving output missing");
        });
    }

    private static void testPowerHub(GameTestHelper helper) {
        helper.succeedIf(() -> {
            BlockPos center = new BlockPos(1, 1, 1);
            BlockPos edge = new BlockPos(3, 1, 3);
            BlockPos outside = new BlockPos(4, 1, 1);
            helper.setBlock(center, ModBlocks.TEST_POWER_HUB.get());
            helper.setBlock(edge, ModBlocks.MACERATOR.get());
            helper.setBlock(outside, ModBlocks.MACERATOR.get());
            TestPowerHubBlockEntity hub = helper.getBlockEntity(center, TestPowerHubBlockEntity.class);
            MaceratorBlockEntity inside = helper.getBlockEntity(edge, MaceratorBlockEntity.class);
            MaceratorBlockEntity beyond = helper.getBlockEntity(outside, MaceratorBlockEntity.class);
            hub.tickServer();
            check(inside.getEnergy(0) == TestPowerHubBlockEntity.FE_PER_MACHINE_PER_TICK,
                    "Machine on the corner of the 5x5 area received no energy");
            check(beyond.getEnergy(0) == 0, "Machine outside the 5x5 area received energy");
        });
    }

    private static void waterPipeLithography(GameTestHelper helper) {
        helper.succeedIf(() -> {
            BlockPos sinkPos = new BlockPos(1, 1, 1);
            BlockPos pipePos = new BlockPos(2, 1, 1);
            BlockPos machinePos = new BlockPos(3, 1, 1);
            helper.setBlock(sinkPos, ModBlocks.WATER_SINK.get());
            helper.setBlock(pipePos, ModBlocks.FLUID_PIPE.get());
            helper.setBlock(machinePos, ModBlocks.LITOGRAFIA.get());
            WaterSinkBlockEntity sink = helper.getBlockEntity(sinkPos, WaterSinkBlockEntity.class);
            LitografiaBlockEntity cleaner = helper.getBlockEntity(machinePos, LitografiaBlockEntity.class);
            for (int i = 0; i < 4; i++) sink.tickServer();
            check(cleaner.getWaterAmount() == LitografiaBlockEntity.WATER_PER_WAFER, "Pipe did not fill tank");
            try (Transaction tx = Transaction.openRoot()) {
                check(cleaner.getWaterStorage().extract(FluidResource.of(Fluids.WATER), 1000, tx) == 0,
                        "External consumer drained the cleaning tank");
            }
            cleaner.setEnergy(0, 20_000);
            put(cleaner, 0, ModItems.PART_ELECTRONIC_DIRTY_SILICON_WAFER.get());
            put(cleaner, 3, Items.COBBLESTONE);
            tick(cleaner, LitografiaBlockEntity.MAX_PROGRESS);
            check(cleaner.getWaterAmount() == 1000 && !stack(cleaner, 0).isEmpty(),
                    "Blocked output consumed input or water");
            try (Transaction tx = Transaction.openRoot()) {
                cleaner.getInventory().extract(3, ItemResource.of(Items.COBBLESTONE), 1, tx);
                tx.commit();
            }
            tick(cleaner, LitografiaBlockEntity.MAX_PROGRESS);
            check(stack(cleaner, 3).is(ModItems.PART_ELECTRONIC_ETCHED_SILICON_WAFER.get()),
                    "Piped water did not clean the wafer");
            check(cleaner.getWaterAmount() == 0 && stack(cleaner, 1).isEmpty(),
                    "Cleaning via tank consumed bucket or wrong water quantity");
            cleaner.getWaterStorage().setAmount(3950);
            sink.tickServer();
            check(cleaner.getWaterAmount() == 4000, "Pipe could not top off a partially filled tank");
        });
    }

    private static void generators(GameTestHelper helper) {
        helper.succeedIf(() -> {
            BlockPos generatorPos = new BlockPos(1, 1, 1);
            BlockPos machinePos = new BlockPos(2, 1, 1);
            helper.setBlock(generatorPos, ModBlocks.FUEL_GENERATOR.get());
            helper.setBlock(machinePos, ModBlocks.MACERATOR.get());
            FuelGeneratorBlockEntity generator = helper.getBlockEntity(generatorPos, FuelGeneratorBlockEntity.class);
            MaceratorBlockEntity machine = helper.getBlockEntity(machinePos, MaceratorBlockEntity.class);
            try (Transaction tx = Transaction.openRoot()) {
                check(generator.getInventory().insert(0, ItemResource.of(Items.OAK_PLANKS), 1, tx) == 1,
                        "Wood was rejected as furnace fuel");
                tx.commit();
            }
            generator.tickServer();
            check(machine.getEnergy(0) == FuelGeneratorBlockEntity.FE_PER_TICK,
                    "Fuel generator did not power an adjacent machine");
            check(generator.getBurnRemaining() > 0 && generator.getEnergy(0) == 0,
                    "Fuel generator burned without producing transferable energy");
            try (Transaction tx = Transaction.openRoot()) {
                check(generator.getEnergyPort().insert(1000, tx) == 0, "Generator accepted external energy");
            }

            BlockPos pausedPos = new BlockPos(1, 1, 3);
            helper.setBlock(pausedPos, ModBlocks.FUEL_GENERATOR.get());
            FuelGeneratorBlockEntity paused = helper.getBlockEntity(pausedPos, FuelGeneratorBlockEntity.class);
            paused.setEnergy(0, paused.getMaxEnergy(0));
            try (Transaction tx = Transaction.openRoot()) {
                paused.getInventory().insert(0, ItemResource.of(Items.OAK_PLANKS), 1, tx);
                tx.commit();
            }
            paused.tickServer();
            check(paused.getInventory().getAmountAsInt(0) == 1 && paused.getBurnRemaining() == 0,
                    "Full generator wasted fuel");

            BlockPos bucketPos = new BlockPos(3, 1, 3);
            helper.setBlock(bucketPos, ModBlocks.FUEL_GENERATOR.get());
            FuelGeneratorBlockEntity bucketGenerator = helper.getBlockEntity(bucketPos, FuelGeneratorBlockEntity.class);
            try (Transaction tx = Transaction.openRoot()) {
                check(bucketGenerator.getInventory().insert(0, ItemResource.of(Items.LAVA_BUCKET), 1, tx) == 1,
                        "Lava bucket rejected as fuel");
                bucketGenerator.getInventory().insert(1, ItemResource.of(Items.COBBLESTONE), 1, tx);
                tx.commit();
            }
            bucketGenerator.tickServer();
            check(bucketGenerator.getInventory().getResource(0).getItem() == Items.LAVA_BUCKET,
                    "Generator burned lava bucket with blocked remainder slot");
            try (Transaction tx = Transaction.openRoot()) {
                bucketGenerator.getInventory().extract(1, ItemResource.of(Items.COBBLESTONE), 1, tx);
                tx.commit();
            }
            bucketGenerator.tickServer();
            check(bucketGenerator.getInventory().getResource(1).getItem() == Items.BUCKET,
                    "Empty bucket was lost after burning lava");

            check(SolarGeneratorBlockEntity.outputFor(false, true, true) == 40, "Basic solar daytime rate");
            check(SolarGeneratorBlockEntity.outputFor(false, false, true) == 0, "Basic solar ran at night");
            check(SolarGeneratorBlockEntity.outputFor(true, true, true) == 100, "Advanced solar daytime rate");
            check(SolarGeneratorBlockEntity.outputFor(true, false, true) == 25, "Advanced solar night rate");
            check(SolarGeneratorBlockEntity.outputFor(true, true, false) == 0, "Covered solar generated energy");
        });
    }

    private static void conduitConnections(GameTestHelper helper) {
        helper.succeedIf(() -> {
            BlockPos sink = new BlockPos(1, 1, 1);
            BlockPos first = new BlockPos(2, 1, 1);
            BlockPos second = new BlockPos(3, 1, 1);
            BlockPos machine = new BlockPos(4, 1, 1);
            helper.setBlock(first, ModBlocks.FLUID_PIPE.get());
            check(!helper.getBlockState(first).getValue(DirectionalConduitBlock.WEST)
                    && !helper.getBlockState(first).getValue(DirectionalConduitBlock.EAST), "Isolated pipe has arms");
            helper.setBlock(sink, ModBlocks.WATER_SINK.get());
            helper.setBlock(second, ModBlocks.FLUID_PIPE.get());
            helper.setBlock(machine, ModBlocks.LITOGRAFIA.get());
            check(helper.getBlockState(first).getValue(DirectionalConduitBlock.WEST)
                    && helper.getBlockState(first).getValue(DirectionalConduitBlock.EAST), "Pipe missed sink or pipe");
            check(helper.getBlockState(second).getValue(DirectionalConduitBlock.EAST), "Pipe missed fluid machine");
            WaterSinkBlockEntity water = helper.getBlockEntity(sink, WaterSinkBlockEntity.class);
            water.tickServer();
            check(helper.getBlockEntity(machine, LitografiaBlockEntity.class).getWaterAmount() == 250,
                    "Two pipes did not carry water");
            helper.setBlock(machine, ModBlocks.MACERATOR.get());
            check(!helper.getBlockState(second).getValue(DirectionalConduitBlock.EAST), "Pipe joined dry machine");
            helper.setBlock(sink, Blocks.STONE);
            check(!helper.getBlockState(first).getValue(DirectionalConduitBlock.WEST), "Pipe joined solid block");
        });
    }

    private static void energyCableNetwork(GameTestHelper helper) {
        helper.succeedIf(() -> {
            BlockPos generatorPos = new BlockPos(1, 1, 1);
            BlockPos first = new BlockPos(2, 1, 1);
            BlockPos second = new BlockPos(3, 1, 1);
            BlockPos machinePos = new BlockPos(4, 1, 1);
            helper.setBlock(first, ModBlocks.ENERGY_CABLE.get());
            check(!helper.getBlockState(first).getValue(DirectionalConduitBlock.WEST), "Isolated cable has an arm");
            helper.setBlock(generatorPos, ModBlocks.FUEL_GENERATOR.get());
            helper.setBlock(second, ModBlocks.ENERGY_CABLE.get());
            helper.setBlock(machinePos, ModBlocks.MACERATOR.get());
            check(helper.getBlockState(first).getValue(DirectionalConduitBlock.WEST)
                    && helper.getBlockState(first).getValue(DirectionalConduitBlock.EAST)
                    && helper.getBlockState(second).getValue(DirectionalConduitBlock.EAST), "Cable connections missing");
            FuelGeneratorBlockEntity generator = helper.getBlockEntity(generatorPos, FuelGeneratorBlockEntity.class);
            MaceratorBlockEntity machine = helper.getBlockEntity(machinePos, MaceratorBlockEntity.class);
            generator.setEnergy(0, 200);
            generator.tickServer();
            check(generator.getEnergy(0) == 120 && machine.getEnergy(0) == 80, "Cable lost or duplicated energy");
            try (Transaction tx = Transaction.openRoot()) {
                generator.getEnergyPort().extract(30, tx);
            }
            check(generator.getEnergy(0) == 120, "Cancelled transaction consumed energy");
            check(machine.extractExternalEnergy(0, 50, Action.EXECUTE) == 0, "Cable drained consumer");
            helper.setBlock(machinePos, Blocks.STONE);
            check(!helper.getBlockState(second).getValue(DirectionalConduitBlock.EAST), "Cable joined solid block");
        });
    }

    private static void fuelInventoryEdgeCases(GameTestHelper helper) {
        helper.succeedIf(() -> {
            BlockPos pos = new BlockPos(1, 1, 1);
            helper.setBlock(pos, ModBlocks.FUEL_GENERATOR.get());
            FuelGeneratorBlockEntity generator = helper.getBlockEntity(pos, FuelGeneratorBlockEntity.class);
            try (Transaction tx = Transaction.openRoot()) {
                check(generator.getInventory().insert(0, ItemResource.of(Items.COAL), 1, tx) == 1, "Coal rejected");
                tx.commit();
            }
            generator.tickServer();
            check(generator.getBurnRemaining() > 0 && generator.getInventory().getAmountAsInt(0) == 0,
                    "Coal did not burn");
            check(generator.getInventory().getAmountAsInt(1) == 0, "Fuel created a bogus remainder");
        });
    }

    private static void solarCableNetwork(GameTestHelper helper) {
        helper.succeedIf(() -> {
            BlockPos generatorPos = new BlockPos(1, 1, 1);
            BlockPos cablePos = new BlockPos(2, 1, 1);
            BlockPos machinePos = new BlockPos(3, 1, 1);
            helper.setBlock(generatorPos, ModBlocks.BASIC_SOLAR_GENERATOR.get());
            helper.setBlock(cablePos, ModBlocks.ENERGY_CABLE.get());
            helper.setBlock(machinePos, ModBlocks.MACERATOR.get());
            SolarGeneratorBlockEntity solar = helper.getBlockEntity(generatorPos, SolarGeneratorBlockEntity.class);
            MaceratorBlockEntity machine = helper.getBlockEntity(machinePos, MaceratorBlockEntity.class);
            solar.setEnergy(0, 100);
            solar.tickServer();
            check(machine.getEnergy(0) == SolarGeneratorBlockEntity.BASIC_FE_PER_TICK,
                    "Solar generator did not feed the machine through a cable");
        });
    }
}
