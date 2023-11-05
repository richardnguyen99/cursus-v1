-- @table public.university_campus
-- @description Create the University-Campus relation table
-- @note This table is generated based on Flask-SQLAlchemy

-- DROP TABLE IF EXISTS public.university_campuses;

CREATE TABLE IF NOT EXISTS public.university_campuses
(
    address_id        INTEGER                   NOT NULL DEFAULT nextval('university_campuses_address_id_seq'::regclass),
    address_number    CHARACTER VARYING(16)     NOT NULL COLLATE pg_catalog."default",
    address_street    CHARACTER VARYING(64)     NOT NULL COLLATE pg_catalog."default",
    address_city      CHARACTER VARYING(64)     NOT NULL COLLATE pg_catalog."default",
    address_state     CHARACTER VARYING(64)     NOT NULL COLLATE pg_catalog."default",
    address_zip_code  CHARACTER VARYING(16)     NOT NULL COLLATE pg_catalog."default",
    created_at        TIMESTAMP WITH TIME ZONE  NOT NULL DEFAULT now(),
    updated_at        TIMESTAMP WITH TIME ZONE  NOT NULL DEFAULT now(),
    country_code      CHARACTER VARYING(2)      NOT NULL COLLATE pg_catalog."default",
    school_short_name CHARACTER VARYING(32)     NOT NULL COLLATE pg_catalog."default",

    CONSTRAINT university_campuses_pkey                                        PRIMARY KEY (address_id),
    CONSTRAINT university_campuses_address_number_address_street_country_c_key UNIQUE      (address_number, address_street, country_code, school_short_name),

    CONSTRAINT university_campuses_country_code_fkey FOREIGN KEY (country_code)
        REFERENCES public.countries (alpha2) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,

    CONSTRAINT university_campuses_school_short_name_fkey FOREIGN KEY (school_short_name)
        REFERENCES public.universities (short_name) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.university_campuses
    OWNER to postgres;
