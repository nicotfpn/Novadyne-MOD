---
trigger: always_on
---

- NeoForge 26.1.2, Minecraft 26.1.2, Java 25
- Package: com.novadyne, mod id: novadyne
- Use DeferredRegister for all registries (items, blocks, entities, creative tabs)
- Class is now "Identifier", NOT ResourceLocation — use Identifier.fromNamespaceAndPath("novadyne", "name")
- Use ItemStackTemplate instead of new ItemStack() in data/recipe context
- All recipes in JSON under data/novadyne/recipes/, use ingredient tags not direct items
- NeoForge item tags: #neoforge:ingots/iron, #neoforge:ingots/steel etc
- Register event buses in mod constructor via modEventBus only
- No static initializers for registry objects, always DeferredHolder/DeferredItem
- Screen rendering: use extractRenderState() not render()
- No Parchment, Mojang param names are native in 26.1
- No explanations. Code only.