SELECT U.full_name, UD.domain_name, UD.type
FROM universities AS U
JOIN university_domains AS UD 
    ON U.short_name = UD.school_short_name
WHERE U.short_name = 'ucla-edu';
