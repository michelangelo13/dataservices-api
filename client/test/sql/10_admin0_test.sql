-- Add to the search path the schema
SET search_path TO public,cartodb,cdb_dataservices_client;

-- Mock the server function
CREATE OR REPLACE FUNCTION cdb_dataservices_server.cdb_geocode_admin0_polygon(username text, orgname text, country_name text)
RETURNS Geometry AS $$
BEGIN
  RAISE NOTICE 'cdb_dataservices_server.cdb_geocode_admin0_polygon invoked with params (%, %, %)', username, orgname, country_name;
  RETURN NULL;
END;
$$ LANGUAGE 'plpgsql';


-- Exercise the public and the proxied function
SELECT cdb_geocode_admin0_polygon('Spain');
