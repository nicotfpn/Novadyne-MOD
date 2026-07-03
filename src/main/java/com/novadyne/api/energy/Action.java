package com.novadyne.api.energy;

public enum Action {
    EXECUTE,
    SIMULATE;

    public boolean execute() {
        return this == EXECUTE;
    }

    public boolean simulate() {
        return this == SIMULATE;
    }

    public static Action fromSimulate(boolean simulate) {
        return simulate ? SIMULATE : EXECUTE;
    }
}
