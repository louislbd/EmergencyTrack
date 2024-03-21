drop database EmergencyTrackDB;

create database EmergencyTrackDB;

create table users (
    user_id integer auto_increment,
    first_name char(35) not null,
    last_name char(35) not null,
    email char(50) not null,
    email_status bit default 0, -- 0 = not verified, 1 = verified
    password char(128) not null,
    account_type decimal(1) default 0, -- 0 = citizen, 1 = pending officer, 2 = officer, 3 = admin
    user_icon char(12), -- path to the user icon
    primary key (user_id),
    constraint FK_users foreign key (account_type)
        references account_types(account_type));

create table account_types (
    account_type decimal(1),
    account_type_name char(20),
    primary key (account_type));

create table states (
    state_id decimal(2) not null, -- state FIPS Code
    state_name char(13) not null,
    state_population decimal(10) not null,
    primary key (state_id));

create table countys (
    county_id decimal(5) not null, -- County FIPS Code
    county_name char(22) not null,
    state_id decimal(2), -- State FIPS Code
    county_population decimal(8) not null,
    primary key (county_id),
    constraint FK_countys foreign key (state_id)
        references states(state_id));

create table departments (
    department_id mediumint unsigned auto_increment,
    county_id decimal(5) not null,
    department_type tinyint unsigned not null default 0,
    primary key (department_id),
    constraint FK_departments_county_id foreign key (county_id)
        references countys(county_id)
    constraint FK_departments_department_type foreign key (department_type)
        references department_types(department_type));

create table department_types (
    department_type tinyint unsigned not null,
    department_name char(10),
    primary key (department_type));

create table department_access (
    department_id mediumint unsigned,
    officer_id integer,
    primary key (department_id, officer_id),
    constraint FK_department_access_department_id foreign key (department_id)
        references departments(department_id),
    constraint FK_department_access_user_id foreign key (officer_id)
        references users(user_id));

create table subscriptions (
    user_id integer,
    department_id mediumint unsigned,
    primary key (user_id, department_id),
    constraint FK_subscriptions_user_id foreign key (user_id)
        references users(user_id),
    constraint FK_subscriptions_department_id foreign key (department_id)
        references departments(department_id));

create table covid_cases (
    dataset_id integer unsigned auto_increment,
    number_of_cases smallint not null,
    report_date date not null,
    county_id decimal(5) not null,
    officer_id integer,
    primary key (dataset_id),
    constraint FK_covid_cases_county_id foreign key (county_id)
        references countys(county_id),
    constraint FK_covid_cases_officer_id foreign key (officer_id)
        references users(user_id));

create table deaths (
    dataset_id integer unsigned auto_increment,
    number_of_deaths smallint not null,
    cause_of_deaths char(30) default "unknown",
    report_date date not null,
    county_id decimal(5) not null,
    officer_id integer,
    primary key (dataset_id),
    constraint FK_deaths_county_id foreign key (county_id)
        references countys(county_id),
    constraint FK_deaths_officer_id foreign key (officer_id)
        references users(user_id));

create table wildfires (
    dataset_id integer unsigned auto_increment,
    location_name char(30) not null,
    location_x_coordinate decimal(8,6) not null, -- latitude
    location_y_coordinate decimal(9,6) not null, -- longitude
    cause_of_fire char(30) default "unknown",
    date_of_fire date not null,
    instructions_for_public char(255),
    level_of_evacuation bit(2),
    fire_is_active bit default 1, -- 1 = fire active, 0 = fire has been extinguished
    county_id decimal(5) not null,
    officer_id integer,
    primary key (dataset_id),
    constraint FK_wildfires_county_id foreign key (county_id)
        references countys(county_id),
    constraint FK_wildfires_officer_id foreign key (officer_id)
        references users(user_id));

create table blocked_roads (
    dataset_id integer unsigned auto_increment,
    road_name char(30) not null,
    location_x_coordinate decimal(8,6) not null, -- latitude
    location_y_coordinate decimal(9,6) not null, -- longitude
    reason char(30) default "unknown",
    intersection1 char(30) not null,
    intersection2 char(30) not null,
    starting_datetime datetime not null,
    ending_datetime datetime not null,
    informations_for_public char(255),
    county_id decimal(5) not null,
    officer_id integer,
    primary key (dataset_id),
    constraint FK_blocked_roads_county_id foreign key (county_id)
        references countys(county_id),
    constraint FK_blocked_roads_officer_id foreign key (officer_id)
        references users(user_id));

create table security_concerns (
    dataset_id integer unsigned auto_increment,
    location_name char(30) not null,
    location_x_coordinate decimal(8,6) not null, -- latitude
    location_y_coordinate decimal(9,6) not null, -- longitude
    cause_of_concern char(30) not null,
    reported_datetime datetime default current_timestamp,
    instructions_for_public char(255),
    concern_is_present bit default 1, -- 1 = concern present, 0 = concern resolved
    county_id decimal(5) not null,
    officer_id integer,
    primary key (dataset_id),
    constraint FK_security_concerns_county_id foreign key (county_id)
        references countys(county_id),
    constraint FK_security_concerns_officer_id foreign key (officer_id)
        references users(user_id));

create table weather_events (
    dataset_id integer unsigned auto_increment,
    location_name char(30) not null,
    location_x_coordinate decimal(8,6) not null, -- latitude
    location_y_coordinate decimal(9,6) not null, -- longitude
    event_type char(30) default "unknown",
    estimated_datetime datetime not null,
    event_radius smallint unsigned,
    instructions_for_public char(255),
    level_of_evacuation bit(2),
    event_is_active bit default 1, -- 1 = event active, 0 = event has been extinguished
    county_id decimal(5) not null,
    officer_id integer,
    primary key (dataset_id),
    constraint FK_weather_events_county_id foreign key (county_id)
        references countys(county_id),
    constraint FK_weather_events_officer_id foreign key (officer_id)
        references users(user_id));
