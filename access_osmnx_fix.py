def load_osm_roads(aoi_bounds, network_type="drive", simplify=True):
    from shapely.geometry import box
    poly = box(aoi_bounds["xmin"], aoi_bounds["ymin"], aoi_bounds["xmax"], aoi_bounds["ymax"])
    G = ox.graph_from_polygon(poly, network_type=network_type)
    gdf_edges = ox.graph_to_gdfs(G, nodes=False, edges=True).reset_index().rename(columns={"u":"u_id","v":"v_id"})
    if simplify:
        gdf_edges["geometry"] = gdf_edges.geometry.simplify(tolerance=0.00005)
    return gdf_edges
