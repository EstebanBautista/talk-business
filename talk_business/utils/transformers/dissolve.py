import geopandas as gpd


def dissolve_count(
    gdf: gpd.GeoDataFrame,
    column: str,
) -> gpd.GeoDataFrame:
    return (
        gdf.filter(["TRACT_CODE", column, "geometry"])
        .dissolve(by="TRACT_CODE", aggfunc="sum")
        .reset_index()
    )


def dissolve_weighted_average(
    gdf: gpd.GeoDataFrame,
    by: str,
    column: str,
    weight: str,
) -> gpd.GeoDataFrame:
    return (
        gdf.filter(["COUNTY", by, "geometry", column, weight])
        .assign(premultiplied=lambda df: df[column] * df[weight])
        .dissolve(by=[by, "COUNTY"], aggfunc="sum")
        .reset_index()
        .assign(**{column: lambda df: df["premultiplied"] / df[weight]})
    )
