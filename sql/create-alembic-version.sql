-- @table public.alembic_version
-- @description Create the table Alembic Version
-- @note This table is generated based on Flask-SQLAlchemy

CREATE TABLE IF NOT EXISTS public.alembic_version
(
    version_num CHARACTER VARYING(32) NOT NULL COLLATE pg_catalog."default" ,

    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.alembic_version
    OWNER to postgres;
