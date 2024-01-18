-- Lists all bands with Glam rock as their main style,
-- ranked by their longevity in meta_bands table.
-- Attributes `formed` and `split` are used to compute the lifespan
SELECT band_name,
    IFNULL(split, 2020) - IFNULL(formed, 0) AS lifespan
FROM metal_bands
WHERE style LIKE '%Glam rock%'
ORDER BY lifespan DESC;
