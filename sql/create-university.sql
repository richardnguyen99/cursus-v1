-- @table public.universities
-- @description Create the table universities
-- @note This table is generated based on Flask-SQLAlchemy


-- DROP TABLE IF EXISTS public.universities;

CREATE TABLE IF NOT EXISTS public.universities
(
    id          INTEGER                     NOT NULL DEFAULT extval('universities_id_seq'::regclass),
    short_name  CHARACTER   VARYING(32)     NOT NULL COLLATE pg_catalog."default",
    full_name   CHARACTER   VARYING(128)    NOT NULL COLLATE pg_catalog."default",
    created_at  TIMESTAMP   WITH TIME ZONE  NOT NULL DEFAULT now(),
    updated_at  TIMESTAMP   WITH TIME ZONE  NOT NULL DEFAULT now(),
    former_name CHARACTER   VARYING(64)              COLLATE pg_catalog."default",
    motto       CHARACTER   VARYING(256)             COLLATE pg_catalog."default",
    `type`      CHARACTER   VARYING(64)              COLLATE pg_catalog."default",
    established INTEGER,

    CONSTRAINT universities_pkey            PRIMARY KEY (id),
    CONSTRAINT universities_full_name_key   UNIQUE      (full_name)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.universities
    OWNER to postgres;
-- Index: ix_universities_short_name

-- DROP INDEX IF EXISTS public.ix_universities_short_name;

CREATE UNIQUE INDEX IF NOT EXISTS ix_universities_short_name
    ON public.universities USING btree
    (short_name COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;
