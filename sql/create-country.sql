-- @table public.countries
-- @description Create the table countries
-- @note This table is generated based on Flask-SQLAlchemy


-- DROP TABLE IF EXISTS public.countries;

CREATE TABLE IF NOT EXISTS public.countries
(
    id              INTEGER                     NOT NULL DEFAULT nextval('countries_id_seq'::regclass),
    `name`          CHARACTER VARYING(128)      NOT NULL COLLATE pg_catalog."default",
    alpha2          CHARACTER VARYING(2)        NOT NULL COLLATE pg_catalog."default",
    alpha3          CHARACTER VARYING(3)        NOT NULL COLLATE pg_catalog."default",
    country_code    CHARACTER VARYING(3)        NOT NULL COLLATE pg_catalog."default",
    iso3166_2       CHARACTER VARYING(16)       NOT NULL COLLATE pg_catalog."default",
    region          CHARACTER VARYING(64)                COLLATE pg_catalog."default",
    subregion       CHARACTER VARYING(64)                COLLATE pg_catalog."default",
    region_code     CHARACTER VARYING(3)                 COLLATE pg_catalog."default",
    sub_region_code CHARACTER VARYING(3)                 COLLATE pg_catalog."default",
    created_at      TIMESTAMP WITH TIME ZONE    NOT NULL DEFAULT now(),
    updated_at      TIMESTAMP WITH TIME ZONE    NOT NULL DEFAULT now(),

    CONSTRAINT countries_pkey                   PRIMARY KEY (id),
    CONSTRAINT countries_name_alpha2_alpha3_key UNIQUE      (name, alpha2, alpha3)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.countries
    OWNER to postgres;
-- Index: ix_countries_alpha2

-- DROP INDEX IF EXISTS public.ix_countries_alpha2;

CREATE UNIQUE INDEX IF NOT EXISTS ix_countries_alpha2
    ON public.countries USING btree
    (alpha2 COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: ix_countries_alpha3

-- DROP INDEX IF EXISTS public.ix_countries_alpha3;

CREATE UNIQUE INDEX IF NOT EXISTS ix_countries_alpha3
    ON public.countries USING btree
    (alpha3 COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: ix_countries_country_code

-- DROP INDEX IF EXISTS public.ix_countries_country_code;

CREATE UNIQUE INDEX IF NOT EXISTS ix_countries_country_code
    ON public.countries USING btree
    (country_code COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: ix_countries_iso3166_2

-- DROP INDEX IF EXISTS public.ix_countries_iso3166_2;

CREATE UNIQUE INDEX IF NOT EXISTS ix_countries_iso3166_2
    ON public.countries USING btree
    (iso3166_2 COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: ix_countries_name

-- DROP INDEX IF EXISTS public.ix_countries_name;

CREATE UNIQUE INDEX IF NOT EXISTS ix_countries_name
    ON public.countries USING btree
    (name COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;
