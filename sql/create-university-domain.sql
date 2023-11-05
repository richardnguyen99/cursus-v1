-- @table public.university_domain
-- @description Create the University-Domain relation table
-- @note This table is generated based on Flask-SQLAlchemy

CREATE TABLE IF NOT EXISTS public.university_domains
(
    id                  INTEGER                  NOT NULL DEFAULT nextval('university_domains_id_seq'::regclass),
    domain_name         CHARACTER VARYING(255)   NOT NULL COLLATE pg_catalog."default",
    created_at          TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
    updated_at          TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
    school_short_name   CHARACTER VARYING(32)    NOT NULL COLLATE pg_catalog."default",

    CONSTRAINT university_domains_pkey                              PRIMARY KEY (id),
    CONSTRAINT university_domains_domain_name_school_short_name_key UNIQUE      (domain_name, school_short_name),
    CONSTRAINT university_domains_school_short_name_fkey            FOREIGN KEY (school_short_name)
        REFERENCES public.universities (short_name) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.university_domains
    OWNER to postgres;
