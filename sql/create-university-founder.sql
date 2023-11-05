-- @table public.university_founder
-- @description Create the University-Founder relation table
-- @note This table is generated based on Flask-SQLAlchemy

CREATE TABLE IF NOT EXISTS public.university_founders
(
    id                  INTEGER                  NOT NULL DEFAULT nextval('university_founders_id_seq'::regclass),
    founder_name        CHARACTER VARYING(255)   NOT NULL COLLATE pg_catalog."default",
    created_at          TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
    updated_at          TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
    school_short_name   CHARACTER VARYING(32)    NOT NULL COLLATE pg_catalog."default",
    biography_link      CHARACTER VARYING(255)            COLLATE pg_catalog."default",

    CONSTRAINT university_founders_pkey                               PRIMARY KEY (id),
    CONSTRAINT university_founders_founder_name_school_short_name_key UNIQUE (founder_name, school_short_name),

    CONSTRAINT university_founders_school_short_name_fkey             FOREIGN KEY (school_short_name)
        REFERENCES public.universities (short_name) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.university_founders
    OWNER to postgres;
