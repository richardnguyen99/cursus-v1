-- @sequence public.university_founders_id_seq
-- @description Create the University-Founder relation table
-- @note This table is generated based on Flask-SQLAlchemy

-- DROP SEQUENCE IF EXISTS public.university_founders_address_id_seq;

-- This sequence is used to generate the primary key for the table University-
-- Founders relation.

CREATE SEQUENCE IF NOT EXISTS public.university_founders_id_seq
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1
    OWNED BY university_founders.id;

ALTER SEQUENCE public.university_founders_id_seq
    OWNER TO postgres;
