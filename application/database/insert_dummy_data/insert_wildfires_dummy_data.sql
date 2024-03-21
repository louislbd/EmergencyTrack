insert into wildfires(location_name,
                      location_x_coordinate,
                      location_y_coordinate,
                      cause_of_fire,
                      date_of_fire,
                      instructions_for_public,
                      level_of_evacuation,
                      fire_is_active,
                      county_id,
                      officer_id)
	values ('Yosemite National Park', 37.721690, -119.651102, 'planned fire', curdate(), 'were a mask', 0, 1, 6043, 2),
	       ('Smith River Complex', 41.963989, -123.985184, null, curdate(), 'mind the area', 2, 1, 6015, 2),
	       ('Sequoia National Monument', 36.726365, -118.871935, 'arson', curdate(), 'mind area', 1, 0, 6107, 2);