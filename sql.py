Create_User_Table = """
    CREATE TABLE BucketList.tbl_user (
        user_id BIGINT NULL AUTO_INCREMENT,
        user_name VARCHAR(45) NULL,
        user_username VARCHAR(45) NULL,
        user_password TEXT,
        PRIMARY KEY (user_id)
    );
"""

sp_Create_User = """
    CREATE DEFINER=`root`@`localhost` PROCEDURE sp_Create_User (
            IN p_name VARCHAR(20),
            IN p_username VARCHAR(20),
            IN p_password TEXT
    )
    BEGIN
        IF ( select exists (select 1 from tb1_user where user_username = p_username) ) THEN
            select 'Username Already Exists !!!';
        ELSE
            insert into tb1_user (
                user_name,
                user_username,
                user_password
            )
            values (
                p_name,
                p_username,
                p_password
            );
        END IF;
    END $$
"""

sp_Validate_Login = """
    CREATE DEFINER='root'@'localhost' PROCEDURE sp_Validate_Login (
            IN p_username VARCHAR(20)
    )
    BEGIN
            select * from tb1_user where user_name = p_username;
    END$$
"""

Create_Wish_Table = """
    CREATE TABLE tb1_wish (
            wish_id BIGINT UNIQUE AUTO_INCREMENT,
            wish_title VARCHAR(45) DEFAULT NULL,
            wish_description TEXT,
            wish_user_id BIGINT DEFAULT NULL,
            wish_date datetime DEFAULT NULL
        )
    """

sp_Add_Wish = """
    CREATE DEFINER='root'@'localhost' PROCEDURE sp_Add_Wish (
        IN P_title varchar(45),
        IN p_description text,
        IN p_user_id bigint
    )
    BEGIN
        insert into tb1_wish (
            wish_title,
            wish_description,
            wish_user_id,
            wish_date
        )
        values (
            p_title,
            p_description,
            p_user_id,
            NOW()
        );
    END$$
"""

sp_Get_Wish_By_User = """
    CREATE DEFINER='root'@'localhost' PROCEDURE sp_Get_Wish_By_User (
        IN p_user_id bigintl
    )
    BEGIN
        select * from tb1_wish where wish_user_id = p_user_id;
    END$$
 """

sp_Get_Wish_By_Id = """
    CREATE DEFINER=`root`@`localhost` PROCEDURE sp_Get_Wish_By_Id (
        IN p_wish_id bigint,
        IN p_user_id bigint
    )
    BEGIN select * from tb1_wish where wish_id = p_wish_id and wish_user_id = p_user_id;
    END$$
"""

sp_Update_Wish = """
    CREATE DEFINER='root'@'localhost' PROCEDURE sp_Update_Wish (
        IN p_title varchar(45),
        IN p_description text,
        IN p_user_id bigint,
        IN p_wish_id bigint,
        IN P_wish_file_path varchar(200),
        IN p_wish_accomplished int,
        IN p_wish_private int
    )
    BEGIN
        update tb1_wish set wish_title=p_title,
        wish_description = p_description,
        wish_file_path = p_wish_file_path,
        wish_accomplished = p_wish_accomplished,
        wish_private = p_wish_private,
        where wish_user_id = p_user_id
        and wish_id = p_wish_id;
    END$$
"""

sp_Delete_Wish = """
    CREATE DEFINER='root'@'localhost' PROCEDURE sp_Delete_Wish (
        IN p_user_id bigint,
        IN p_wish_id bigint,
        OUT p_wish_file_path varchar(200)
    )
    BEGIN
        select wish_file_path into p_wish_file_path  from tb1_wish where user_id = p_user_id and wish_id = p_wish_id;
        delete from tb1_wish where user_id = p_user_id and wish_id = p_wish_id;
    END$$
"""

sp_Get_Wish_By_User_To_Paginate = """
    CREATE DEFINER='root'@'localhost' PROCEDURE sp_Get_Wish_By_User_To_Paginate (
        IN p_user_id bigint,
        IN p_limit int,
        IN p_offset int,
        OUT p_total bigint
    )
    BEGIN
        select count(*) into p_total from tb1_wish where wish_user_id = p_user_id;
        SET @t1 = CONCAT('select * from tb1_wish where wish_user_id = ', p_user_id, ' order by wish_date desc limit ', p_limit, ' offset ', p_offset);
        PREPARE stmt FROM @t1;
        EXECUTE stmt;
        DEALLOCATE PREPARE stmt;
    END$$
"""
