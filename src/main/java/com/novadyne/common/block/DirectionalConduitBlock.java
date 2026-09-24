package com.novadyne.common.block;

import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.util.RandomSource;
import net.minecraft.world.item.context.BlockPlaceContext;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.LevelReader;
import net.minecraft.world.level.ScheduledTickAccess;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.StateDefinition;
import net.minecraft.world.level.block.state.properties.BooleanProperty;
import net.minecraft.world.phys.shapes.CollisionContext;
import net.minecraft.world.phys.shapes.Shapes;
import net.minecraft.world.phys.shapes.VoxelShape;

/** A central four-pixel conduit with arms only toward compatible, loaded neighbors. */
public abstract class DirectionalConduitBlock extends Block {
    public static final BooleanProperty NORTH = BooleanProperty.create("north");
    public static final BooleanProperty SOUTH = BooleanProperty.create("south");
    public static final BooleanProperty EAST = BooleanProperty.create("east");
    public static final BooleanProperty WEST = BooleanProperty.create("west");
    public static final BooleanProperty UP = BooleanProperty.create("up");
    public static final BooleanProperty DOWN = BooleanProperty.create("down");
    private static final VoxelShape CORE = box(6, 6, 6, 10, 10, 10);
    private static final VoxelShape[] ARMS = {
        box(6, 0, 6, 10, 6, 10), box(6, 10, 6, 10, 16, 10),
        box(6, 6, 0, 10, 10, 6), box(6, 6, 10, 10, 10, 16),
        box(0, 6, 6, 6, 10, 10), box(10, 6, 6, 16, 10, 10)
    };
    private static final BooleanProperty[] SIDES = {DOWN, UP, NORTH, SOUTH, WEST, EAST};
    private static final VoxelShape[] SHAPES = new VoxelShape[64];

    static {
        for (int mask = 0; mask < SHAPES.length; mask++) {
            VoxelShape shape = CORE;
            for (int i = 0; i < 6; i++) if ((mask & (1 << i)) != 0) shape = Shapes.or(shape, ARMS[i]);
            SHAPES[mask] = shape.optimize();
        }
    }

    protected DirectionalConduitBlock(Properties properties) {
        super(properties);
        BlockState state = stateDefinition.any();
        for (BooleanProperty side : SIDES) state = state.setValue(side, false);
        registerDefaultState(state);
    }

    @Override protected void createBlockStateDefinition(StateDefinition.Builder<Block, BlockState> builder) {
        builder.add(SIDES);
    }

    public static BooleanProperty side(Direction direction) { return SIDES[direction.get3DDataValue()]; }

    protected abstract boolean connectsTo(Level level, BlockPos neighbor, Direction side);

    private boolean connected(Level level, BlockPos pos, Direction side) {
        BlockPos neighbor = pos.relative(side);
        return level.hasChunkAt(neighbor) && connectsTo(level, neighbor, side.getOpposite());
    }

    @Override public BlockState getStateForPlacement(BlockPlaceContext context) {
        return resolve(defaultBlockState(), context.getLevel(), context.getClickedPos());
    }

    private BlockState resolve(BlockState state, Level level, BlockPos pos) {
        for (Direction direction : Direction.values())
            state = state.setValue(side(direction), connected(level, pos, direction));
        return state;
    }

    @Override protected void onPlace(BlockState state, Level level, BlockPos pos, BlockState oldState, boolean movedByPiston) {
        if (oldState.is(this) || level.isClientSide()) return;
        BlockState resolved = resolve(state, level, pos);
        if (resolved != state) level.setBlock(pos, resolved, Block.UPDATE_CLIENTS | Block.UPDATE_KNOWN_SHAPE);
    }

    @Override protected BlockState updateShape(BlockState state, LevelReader level, ScheduledTickAccess ticks,
            BlockPos pos, Direction directionToNeighbour, BlockPos neighbourPos, BlockState neighbourState, RandomSource random) {
        return state.setValue(side(directionToNeighbour),
                level instanceof Level actual && connected(actual, pos, directionToNeighbour));
    }

    @Override protected VoxelShape getShape(BlockState state, BlockGetter level, BlockPos pos, CollisionContext context) {
        int mask = 0;
        for (int i = 0; i < 6; i++) if (state.getValue(SIDES[i])) mask |= 1 << i;
        return SHAPES[mask];
    }
}
