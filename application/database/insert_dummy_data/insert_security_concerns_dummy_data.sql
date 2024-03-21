insert into security_concerns(location_name,
                              location_x_coordinate,
                              location_y_coordinate,
                              cause_of_concern,
                              reported_datetime,
                              instructions_for_public,
                              concern_is_present,
                              county_id,
                              officer_id)
	values ('Rodeo Drive', 34.067579, -118.400742, 'armed robbery', now(), 'mind the area', 1, 6037, 2),
	       ('Pier 39', 37.810740, -122.411253, 'Sea lion on the loose', now(), 'don''t feed the sea lions', 0, 6075, 2),
	       ('Pacific Coast Highway', 34.461824, -120.011260, 'car chase', now(), 'mind the highway 1 & make space for police cars', 1, 6083, 2);