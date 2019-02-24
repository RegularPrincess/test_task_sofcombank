create_request =  """create table IF NOT EXISTS request
        (
	    id serial not null
		    constraint request_pkey
			primary key,
	    kind_premises varchar(10) not null,
	    post_code varchar(10),
	    region varchar(50),
	    city_type varchar(10),
	    city varchar(50),
	    street_type varchar(10),
	    street varchar(50),
	    house varchar(50),
	    block varchar(10),
	    flat varchar(10),
	    adress varchar,
	    try_num integer default 0
        );"""

create_region_code = """create table IF NOT EXISTS region_code
(
	value integer not null
		constraint region_codes_pkey
			primary key,
	name varchar not null
)
;
"""

create_district_code = """create table IF NOT EXISTS district_code
(
	value integer not null
		constraint district_codes_pkey
			primary key,
	name varchar not null,
	region_value integer not null
		constraint region_value
			references region_code
				on update cascade on delete cascade
)
;
"""

create_localy_code = """create table IF NOT EXISTS locality_code
(
	value integer not null
		constraint locality_code_pkey
			primary key,
	name varchar not null,
	district_value integer not null
		constraint district_value
			references district_code
				on update cascade on delete cascade
)
;"""

create_notify_func = """CREATE OR REPLACE FUNCTION notify_insert() RETURNS trigger AS
$BODY$
BEGIN
		EXECUTE format('NOTIFY insert_notify, ''%s''', NEW.id);
-- 		EXECUTE format('insert into region_code (value, name) VALUES (12532, ''%s'')', NEW.id);
		RETURN NULL;
END;
$BODY$
LANGUAGE plpgsql VOLATILE
COST 100;
"""

drop_notify_trigger = """DROP TRIGGER IF EXISTS insert_trigger ON request;"""

create_notify_trigger = """CREATE TRIGGER insert_trigger AFTER INSERT
	ON request
	FOR EACH ROW
	EXECUTE PROCEDURE notify_insert();"""