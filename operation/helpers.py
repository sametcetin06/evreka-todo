MESSAGE_TYPE = ((
    (0, "SERVER"),
    (1, "STATUS"),
    (2, "TIMEZONE"),
    (3, "LOCATION_INTERVAL"),
    (4, "ENGINE_BLOCK_ON"),
    (5, "ENGINE_BLOCK_OFF"),
    (6, "SET_APN"),
    (7, "GET_APN"),
    (8, "RESTART"),
    (9, "SET_KM"),
    (10, "SET_SPEED_ALARM"),
    (11, "SET_IGNITION_ALARM"),
    (12, "TETIS_TEXT_MESSAGE"),
    (13, "TETIS_TEXT_AND_LOCATION_MESSAGE"),
    (14, "SET_GEOFENCE")
))

ACCESSORY_TYPE = (
    (0, 'Karel Gateway'),
    (100, 'Diğer')
)

AREA_TYPE = (
    (0, 'polygon'),
    (1, 'polyline'),
    (2, 'circle'),
    (3, 'point'),
    (4, 'town'),
)
