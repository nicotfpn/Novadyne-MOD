package com.novadyne.client.loader;

import com.novadyne.NovaDyneMod;
import com.novadyne.client.model.OBJModel;
import net.minecraft.resources.Identifier;
import net.minecraft.client.Minecraft;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

public final class OBJLoader {
    private static final Map<String, OBJModel> CACHE = new HashMap<>();
    private static final Map<String, Map<String, int[]>> OBJECT_RANGES_CACHE = new HashMap<>();

    private OBJLoader() {}

    public static OBJModel getModel(String path) {
        return CACHE.computeIfAbsent(path, OBJLoader::loadModel);
    }

    public static Map<String, int[]> getObjectRanges(String path) {
        getModel(path);
        return OBJECT_RANGES_CACHE.get(path);
    }

    private static OBJModel loadModel(String path) {
        Identifier location = Identifier.fromNamespaceAndPath(NovaDyneMod.MODID, path);

        List<float[]> rawVertices = new ArrayList<>();
        List<float[]> rawUvs = new ArrayList<>();
        List<float[]> rawNormals = new ArrayList<>();

        List<Float> outVertices = new ArrayList<>();
        List<Float> outUvs = new ArrayList<>();
        List<Float> outNormals = new ArrayList<>();

        Map<String, int[]> objectRanges = new LinkedHashMap<>();
        String currentObject = null;
        int objectStart = 0;

        try (BufferedReader reader = new BufferedReader(
                new InputStreamReader(Minecraft.getInstance().getResourceManager().open(location)))) {

            String line;
            while ((line = reader.readLine()) != null) {
                line = line.trim();

                if (line.isEmpty() || line.startsWith("#") || line.startsWith("s ") || line.startsWith("g ") || line.startsWith("usemtl ")) {
                    continue;
                }

                if (line.startsWith("o ")) {
                    if (currentObject != null) {
                        int objectEnd = outVertices.size() / 3;
                        if (objectEnd > objectStart) {
                            objectRanges.put(currentObject, new int[]{objectStart, objectEnd});
                        }
                    }
                    currentObject = line.substring(2).trim();
                    objectStart = outVertices.size() / 3;
                } else if (line.startsWith("v ")) {
                    String[] parts = line.split("\\s+");
                    if (parts.length >= 4) {
                        rawVertices.add(new float[]{
                                Float.parseFloat(parts[1]),
                                Float.parseFloat(parts[2]),
                                Float.parseFloat(parts[3])
                        });
                    }
                } else if (line.startsWith("vt ")) {
                    String[] parts = line.split("\\s+");
                    if (parts.length >= 3) {
                        float u = Float.parseFloat(parts[1]);
                        float v = Float.parseFloat(parts[2]);
                        rawUvs.add(new float[]{u, 1.0F - v});
                    }
                } else if (line.startsWith("vn ")) {
                    String[] parts = line.split("\\s+");
                    if (parts.length >= 4) {
                        rawNormals.add(new float[]{
                                Float.parseFloat(parts[1]),
                                Float.parseFloat(parts[2]),
                                Float.parseFloat(parts[3])
                        });
                    }
                } else if (line.startsWith("f ")) {
                    String[] parts = line.split("\\s+");
                    if (parts.length < 4) continue;

                    int[][] faceData = new int[parts.length - 1][3];

                    for (int i = 1; i < parts.length; i++) {
                        faceData[i - 1] = parseFaceVertex(parts[i]);
                    }

                    for (int i = 1; i < faceData.length - 1; i++) {
                        addFaceVertex(outVertices, outUvs, outNormals, faceData[0], rawVertices, rawUvs, rawNormals);
                        addFaceVertex(outVertices, outUvs, outNormals, faceData[i], rawVertices, rawUvs, rawNormals);
                        addFaceVertex(outVertices, outUvs, outNormals, faceData[i + 1], rawVertices, rawUvs, rawNormals);
                    }
                }
            }

            if (currentObject != null) {
                int objectEnd = outVertices.size() / 3;
                if (objectEnd > objectStart) {
                    objectRanges.put(currentObject, new int[]{objectStart, objectEnd});
                }
            }
        } catch (Exception e) {
            NovaDyneMod.LOGGER.error("Failed to load OBJ model: {}", path, e);
            OBJECT_RANGES_CACHE.put(path, new java.util.LinkedHashMap<>());
            return createFallbackModel();
        }

        float[] verts = toFloatArray(outVertices);
        float[] uvArr = toFloatArray(outUvs);
        float[] normArr = toFloatArray(outNormals);
        int[] idxArr = new int[verts.length / 3];
        for (int i = 0; i < idxArr.length; i++) {
            idxArr[i] = i;
        }

        OBJECT_RANGES_CACHE.put(path, objectRanges);
        return new OBJModel(verts, uvArr, normArr, idxArr);
    }

    private static int[] parseFaceVertex(String token) {
        String[] parts = token.split("/");
        int[] result = new int[3];
        result[0] = Integer.parseInt(parts[0]) - 1;
        if (parts.length >= 2 && !parts[1].isEmpty()) {
            result[1] = Integer.parseInt(parts[1]) - 1;
        } else {
            result[1] = -1;
        }
        if (parts.length >= 3 && !parts[2].isEmpty()) {
            result[2] = Integer.parseInt(parts[2]) - 1;
        } else {
            result[2] = -1;
        }
        return result;
    }

    private static void addFaceVertex(List<Float> outVerts, List<Float> outUvs, List<Float> outNormals,
                                       int[] faceData, List<float[]> vertices, List<float[]> uvs, List<float[]> normals) {
        float[] v = vertices.get(faceData[0]);
        outVerts.add(v[0]);
        outVerts.add(v[1]);
        outVerts.add(v[2]);

        if (faceData[1] >= 0 && faceData[1] < uvs.size()) {
            float[] uv = uvs.get(faceData[1]);
            outUvs.add(uv[0]);
            outUvs.add(uv[1]);
        } else {
            outUvs.add(0.0F);
            outUvs.add(0.0F);
        }

        if (faceData[2] >= 0 && faceData[2] < normals.size()) {
            float[] n = normals.get(faceData[2]);
            outNormals.add(n[0]);
            outNormals.add(n[1]);
            outNormals.add(n[2]);
        } else {
            outNormals.add(0.0F);
            outNormals.add(1.0F);
            outNormals.add(0.0F);
        }
    }

    private static float[] toFloatArray(List<Float> list) {
        float[] arr = new float[list.size()];
        for (int i = 0; i < list.size(); i++) {
            arr[i] = list.get(i);
        }
        return arr;
    }

    private static OBJModel createFallbackModel() {
        float[] verts = {
            -1.0F, 0.0F, -1.0F,
             1.0F, 0.0F, -1.0F,
            -1.0F, 2.0F, -1.0F,
             1.0F, 2.0F, -1.0F
        };
        float[] uv = {
            0.0F, 0.0F, 1.0F, 0.0F, 0.0F, 1.0F, 1.0F, 1.0F
        };
        float[] norm = {
            0.0F, 0.0F, 1.0F, 0.0F, 0.0F, 1.0F, 0.0F, 0.0F, 1.0F, 0.0F, 0.0F, 1.0F
        };
        int[] indices = {0, 1, 2, 2, 1, 3};
        return new OBJModel(verts, uv, norm, indices);
    }

    public static void clearCache() {
        CACHE.clear();
        OBJECT_RANGES_CACHE.clear();
    }
}
