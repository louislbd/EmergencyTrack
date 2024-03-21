insert into weather_events(location_name,
                           location_x_coordinate,
                           location_y_coordinate,
                           event_type,
                           estimated_datetime,
                           event_radius,
                           instructions_for_public,
                           level_of_evacuation,
                           event_is_active,
                           county_id,
                           officer_id)
	values ('Sinkyone Wilderness Park', 39.894265, -123.922698, 'tsunami', curdate(), 10, 'mind the area', 2, 1, 6045, 2),
	       ('Stockton', 37.948473, -121.300601, 'heavy rain', curdate(), 6, 'stay inside', 0, 1, 6077, 2),
	       ('EL Centro', 32.801733, -115.598403, 'earthquake', curdate(), 10, 'seek cover', 1, 0, 6025, 2);