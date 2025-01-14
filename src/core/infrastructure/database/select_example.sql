SELECT ST_AsText(location), ST_SRID(location) FROM building LIMIT 5;

SELECT ST_AsText(ST_Transform(location, 4326)) FROM building LIMIT 5;

SELECT ST_AsText(location)
FROM building
WHERE building.id IN (10, 6);

SELECT organization.id, organization.name
FROM organization
JOIN building ON building.id = organization.building_id
WHERE ST_Covers(
    ST_SetSRID(ST_MakeEnvelope(15.330973, -119.595946, 60.067381, 115.130354), 4326),
    building.location
);


SELECT id, ST_AsText(location), ST_X(location) AS longitude, ST_Y(location) AS latitude
FROM building
WHERE id IN (10, 6);
