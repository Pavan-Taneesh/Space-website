-- Latest orbital_elements row per object, with staleness flag.
-- "Latest" = most recent fetched_at per object_id (orbital_elements keeps full history, never overwritten).
CREATE OR REPLACE VIEW latest_orbital_elements AS
SELECT DISTINCT ON (oe.object_id)
    oe.*,
    (oe.fetched_at < NOW() - INTERVAL '24 hours') AS is_stale
FROM orbital_elements oe
ORDER BY oe.object_id, oe.fetched_at DESC;