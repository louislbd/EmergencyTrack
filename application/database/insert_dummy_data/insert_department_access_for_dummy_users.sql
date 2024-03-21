-- Insert entries into department_access for officers with the right department number

/*
    Structure of dummy officer data:
        email = [county_id]_[department_id]@officer-dummy.com"
        password = "password"
        first_name = [county_name][department_name]
        last_name = "Officer"
*/
insert into department_access (department_id, officer_id)
    select substring(users.email,6,length(users.email)-23) as 'department_id',
	       users.user_id as 'officer_id'
       from users
       where users.last_name = 'Officer';


