create or replace view county_statistics (county_id,
                                          county_name,
                                          state_id,
                                          covid_cases_7_days_per_100k,
                                          deaths_7_days_per_100k,
                                          wildfires,
                                          blocked_roads,
                                          security_concerns,
                                          weather_events)
       as select countys.county_id, countys.county_name, countys.state_id,
	             covid_case_statistics.last_7_days_per_100k as 'covid_cases_7_days_per_100k',
	             death_statistics.last_7_days_per_100k as 'deaths_7_days_per_100k',
	             count(wildfires.county_id) as 'wildfires',
	             count(blocked_roads.county_id) as 'blocked_roads',
	             count(security_concerns.county_id) as 'security_concerns',
	             count(weather_events.county_id) as 'weather_events'
	         from countys
		         left join covid_case_statistics on countys.county_id = covid_case_statistics.county_id
		         left join death_statistics on countys.county_id = death_statistics.county_id
		         left join wildfires on countys.county_id = wildfires.county_id
		         left join blocked_roads on countys.county_id = blocked_roads.county_id
		         left join security_concerns on countys.county_id = security_concerns.county_id
		         left join weather_events on countys.county_id = weather_events.county_id
	         group by countys.county_id;


create or replace view state_statistics (state_id,
                                         state_name,
                                         covid_cases_7_days_per_100k,
                                         deaths_7_days_per_100k,
                                         wildfires,
                                         blocked_roads,
                                         security_concerns,
                                         weather_events)
       as select states.state_id, states.state_name,
	             sum(case when covid_cases.report_date between curdate() - interval 7 day and curdate()
	                 then covid_cases.number_of_cases else 0 end) / (states.state_population / 100000)
	                 as 'covid_cases_7_days_per_100k',
	             sum(case when deaths.report_date between curdate() - interval 7 day and curdate()
	                 then deaths.number_of_deaths else 0 end) / (states.state_population / 100000)
	                 as 'deaths_7_days_per_100k',
	             sum(county_statistics.wildfires) as 'wildfires',
	             sum(county_statistics.blocked_roads) as 'blocked_roads',
	             sum(county_statistics.security_concerns) as 'security_concerns',
	             sum(county_statistics.weather_events) as 'weather_events'
	         from states join county_statistics on states.state_id = county_statistics.state_id
						 join covid_cases on covid_cases.county_id = county_statistics.county_id
                         join deaths on deaths.county_id = county_statistics.county_id
	         group by states.state_id;


create or replace view covid_case_statistics (county_id,
                                              county_name,
                                              today_per_100k,
                                              last_7_days_per_100k,
                                              month_per_100k,
                                              year_per_100k,
                                              all_time_per_100k)
       as select countys.county_id, countys.county_name,
                 sum(case when covid_cases.report_date = curdate() then covid_cases.number_of_cases else 0 end) /
                 (countys.county_population / 100000) as today_per_100k,
                 sum(case when covid_cases.report_date between curdate() - interval 7 day and curdate()
                     THEN covid_cases.number_of_cases else 0 end) /
                 (countys.county_population / 100000) as last_7_days_per_100k,
                 sum(case when month(covid_cases.report_date) = month(curdate()) and
                     year(covid_cases.report_date) = year(curdate()) then covid_cases.number_of_cases else 0 end) /
                 (countys.county_population / 100000) as month_per_100k,
                 sum(case when year(covid_cases.report_date) = year(curdate()) then covid_cases.number_of_cases else 0 end) /
                 (countys.county_population / 100000) as year_per_100k,
                 sum(covid_cases.number_of_cases) / (countys.county_population / 100000) as all_time_per_100k
            from covid_cases join countys on covid_cases.county_id = countys.county_id
            group by county_id;


create or replace view death_statistics (county_id,
                                         county_name,
                                         today_per_100k,
                                         last_7_days_per_100k,
                                         month_per_100k,
                                         year_per_100k,
                                         all_time_per_100k)
       as select countys.county_id, countys.county_name,
                 sum(case when deaths.report_date = curdate() then deaths.number_of_deaths else 0 end) /
                 (countys.county_population / 100000) as today_per_100k,
                 sum(case when deaths.report_date between curdate() - interval 7 day and curdate()
                     THEN deaths.number_of_deaths else 0 end) /
                 (countys.county_population / 100000) as last_7_days_per_100k,
                 sum(case when month(deaths.report_date) = month(curdate()) and
                     year(deaths.report_date) = year(curdate()) then deaths.number_of_deaths else 0 end) /
                 (countys.county_population / 100000) as month_per_100k,
                 sum(case when year(deaths.report_date) = year(curdate()) then deaths.number_of_deaths else 0 end) /
                 (countys.county_population / 100000) as year_per_100k,
                 sum(deaths.number_of_deaths) / (countys.county_population / 100000) as all_time_per_100k
            from deaths join countys on deaths.county_id = countys.county_id
            group by county_id;