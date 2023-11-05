-- @block Bookmarked query
-- @group cursus
-- @name select-university-domains
-- @description Create the university domains table
-- @table public.university_campuses

CREATE TABLE IF NOT EXISTS public.university_domains (
    id          INTEGER                 NOT NULL DEFAULT nextval('university_domains_id_seq'::regclass),
    domain_name CHARACTER VARYING(255)  NOT NULL COLLATE pg_catalog."default",
    school_id   CHARACTER VARYING(11)   NOT NULL COLLATE pg_catalog."default" ,

    CONSTRAINT university_domains_pkey           PRIMARY KEY (id),
    CONSTRAINT university_domains_
    CONSTRAINT university_domains_school_id_fkey FOREIGN KEY (school_id)
        REFERENCES public.universities (object_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);




