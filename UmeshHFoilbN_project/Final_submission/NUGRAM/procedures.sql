DELIMITER //

CREATE PROCEDURE InsertUser(
    IN p_NUID VARCHAR(255),
    IN p_first_name VARCHAR(255),
    IN p_last_name VARCHAR(255),
    IN p_email VARCHAR(255),
    IN p_phone_number VARCHAR(20),
    IN p_profile_picture LONGTEXT,
    IN p_degree VARCHAR(255),
    IN p_major VARCHAR(255),
    IN p_college VARCHAR(255),
    IN p_password VARCHAR(255)
)
BEGIN
    INSERT INTO Users (NUID, first_name, last_name, email, phone_number, profile_picture, degree, major, college, password)
    VALUES (p_NUID, p_first_name, p_last_name, p_email, p_phone_number, p_profile_picture, p_degree, p_major, p_college, p_password);
    SELECT LAST_INSERT_ID();
END //

DELIMITER ;



DELIMITER //

CREATE PROCEDURE UserLogin(
    IN p_email VARCHAR(255),
    IN p_password VARCHAR(255),
    OUT p_valid TINYINT(1)
)
BEGIN
    DECLARE user_count INT DEFAULT 0;

    SELECT COUNT(*)
    INTO user_count
    FROM Users
    WHERE email = p_email AND password = p_password;

    IF user_count = 1 THEN
        SET p_valid = 1;
    ELSE
        SET p_valid = 0;
    END IF;
END //

DELIMITER ;


DELIMITER //
CREATE PROCEDURE SearchUsers(IN p_search_term VARCHAR(255))
BEGIN
    SELECT * FROM Users WHERE first_name LIKE CONCAT('%', p_search_term, '%') OR last_name LIKE CONCAT('%', p_search_term, '%');
END //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE FollowUser(IN p_follower_id INT, IN p_followed_id INT, IN p_follow_date DATETIME)
BEGIN
    INSERT INTO Follows (follower_id, followed_id, follow_date) VALUES (p_follower_id, p_followed_id, p_follow_date);
END //
DELIMITER ;



DELIMITER //
CREATE PROCEDURE JoinGroup(IN p_NUID INT, IN p_group_name VARCHAR(255))
BEGIN
    INSERT INTO User_Groups (NUID, group_name) VALUES (p_NUID, p_group_name);
END //
DELIMITER ;

DELIMITER //

CREATE PROCEDURE InsertReport(
    IN p_reporter_id INT,
    IN p_reported_id INT,
    IN p_report_category VARCHAR(255),
    IN p_report_description TEXT,
    IN p_timestamp DATETIME
)
BEGIN
    INSERT INTO Reports (reporter_id, reported_id, report_category, report_description,report_time)
    VALUES (p_reporter_id, p_reported_id, p_report_category, p_report_description,p_timestamp);
END //

DELIMITER ;

DELIMITER //

CREATE PROCEDURE InsertMessage(
    IN p_sender_id INT,
    IN p_receiver_id INT,
    IN p_message_body TEXT,
    IN p_message_date DATETIME
)
BEGIN
    INSERT INTO Messages (sender_id, receiver_id, message_body, message_date, read_receipt)
    VALUES (p_sender_id, p_receiver_id, p_message_body, p_message_date, FALSE);
END //

DELIMITER ;


DELIMITER //
CREATE PROCEDURE GetFollowers(IN user_id INT)
BEGIN
    SELECT U.* FROM Users U
    JOIN Follows F ON U.user_id = F.follower_id
    WHERE F.followed_id = user_id;
END //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE GetFollowing(IN user_id INT)
BEGIN
    SELECT U.* FROM Users U
    JOIN Follows F ON U.user_id = F.followed_id
    WHERE F.follower_id = user_id;
END //
DELIMITER ;

// new 
DELIMITER //
CREATE PROCEDURE GetUserIdFromCredentials(IN input_email VARCHAR(255))
BEGIN
    SELECT user_id, NUID FROM Users WHERE email = input_email;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE UnfollowUser(IN input_follower_id INT, IN input_followed_id INT)
BEGIN
    DELETE FROM Follows WHERE follower_id = input_follower_id AND followed_id = input_followed_id;
END //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE CreateGroup(
    IN input_group_name VARCHAR(255),
    IN input_description TEXT,
    IN input_date_created DATETIME,
    IN input_group_image LONGTEXT
)
BEGIN
    INSERT INTO `Groups` (group_name, description, date_created, group_image) 
    VALUES (input_group_name, input_description, input_date_created, input_group_image);
END //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE GetGroups()
BEGIN
    SELECT group_name, description, group_image FROM `Groups`;
END //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE GetReportsByUserId(IN input_user_id INT)
BEGIN
    SELECT * FROM Reports WHERE reporter_id = input_user_id ORDER BY report_time DESC;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE CheckFollowStatus(IN input_follower_id INT, IN input_followed_id INT)
BEGIN
    SELECT COUNT(*) FROM Follows WHERE follower_id = input_follower_id AND followed_id = input_followed_id;
END //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE GetMessages(IN input_user1_id INT, IN input_user2_id INT)
BEGIN
    SELECT Messages.*, 
           sender.first_name as sender_first_name, 
           receiver.first_name as receiver_first_name
    FROM Messages
    JOIN Users as sender ON Messages.sender_id = sender.user_id
    JOIN Users as receiver ON Messages.receiver_id = receiver.user_id
    WHERE (sender_id = input_user1_id AND receiver_id = input_user2_id) 
       OR (sender_id = input_user2_id AND receiver_id = input_user1_id)
    ORDER BY message_date;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE GetAllUsers()
BEGIN
    SELECT * FROM Users;
END //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE GetFollowersPosts(IN input_user_id INT)
BEGIN
    SELECT Posts.*, Users.first_name, Users.last_name 
    FROM Posts
    JOIN Users ON Posts.user_id = Users.user_id
    WHERE Posts.user_id IN (
        SELECT followed_id FROM Follows WHERE follower_id = input_user_id
    )
    ORDER BY timestamp DESC;
END //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE CreatePost(
    IN input_user_id INT,
    IN input_caption TEXT,
    IN input_post LONGTEXT,
    IN input_timestamp DATETIME
)
BEGIN
    INSERT INTO Posts (user_id, caption, post, timestamp) 
    VALUES (input_user_id, input_caption, input_post, input_timestamp);
END //
DELIMITER ;



DELIMITER //
CREATE PROCEDURE GetUserPosts(IN input_user_id INT)
BEGIN
    SELECT P.*, U.first_name, U.last_name 
    FROM Posts P
    JOIN Users U ON P.user_id = U.user_id
    WHERE P.user_id = input_user_id
    ORDER BY P.timestamp DESC;
END //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE GetPostLikeCount(IN p_post_id INT)
BEGIN
    SELECT COUNT(*) as like_count 
    FROM Likes 
    WHERE post_id = p_post_id;
END //
DELIMITER ;



DELIMITER //
CREATE PROCEDURE GetPostComments(IN post_id INT)
BEGIN
    SELECT Comments.*, Users.first_name 
    FROM Comments
    JOIN Users ON Comments.user_id = Users.user_id
    WHERE Comments.post_id = post_id
    ORDER BY Comments.comment_date DESC;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE GetFollowedUsersPosts(IN user_id INT)
BEGIN
    SELECT Posts.* 
    FROM Posts
    JOIN Follows ON Posts.user_id = Follows.followed_id
    WHERE Follows.follower_id = user_id
    ORDER BY Posts.timestamp DESC;
END //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE AddComment(IN p_post_id INT, IN p_user_id INT, IN p_comment TEXT, IN p_comment_date DATETIME)
BEGIN
    INSERT INTO Comments (post_id, user_id, comment, comment_date) 
    VALUES (p_post_id, p_user_id, p_comment, p_comment_date);
END //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE CheckLikeExists(IN p_user_id INT, IN p_post_id INT)
BEGIN
    SELECT EXISTS(
       SELECT 1 FROM Likes WHERE user_id = p_user_id AND post_id = p_post_id
    ) AS like_exists;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE InsertLike(IN p_user_id INT, IN p_post_id INT, IN p_like_date DATETIME)
BEGIN
    INSERT INTO Likes (user_id, post_id, like_date) VALUES (p_user_id, p_post_id, p_like_date);
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE DeleteLike(IN p_user_id INT, IN p_post_id INT)
BEGIN
    DELETE FROM Likes WHERE user_id = p_user_id AND post_id = p_post_id;
END //
DELIMITER ;



DELIMITER //
CREATE PROCEDURE GetComments(IN post_id_param INT)
BEGIN
    SELECT Comments.*, Users.first_name 
    FROM Comments
    JOIN Users ON Comments.user_id = Users.user_id
    WHERE Comments.post_id = post_id_param
    ORDER BY Comments.comment_date DESC;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE UpdateUser(IN user_id_param INT, IN field_param VARCHAR(64), IN value_param VARCHAR(255))
BEGIN
    SET @query = CONCAT('UPDATE Users SET ', field_param, ' = ? WHERE user_id = ?');
    SET @value = value_param;
    SET @u_id = user_id_param;

    PREPARE stmt FROM @query;
    EXECUTE stmt USING @value, @u_id;
    DEALLOCATE PREPARE stmt;
END //
DELIMITER ;




DELIMITER //

CREATE PROCEDURE `DeletePost` (
    IN `in_post_id` INT,
    IN `in_user_id` INT,
    OUT `out_status` INT
)
BEGIN
    -- Check if the post exists and belongs to the user
    IF EXISTS (SELECT 1 FROM Posts WHERE post_id = in_post_id AND user_id = in_user_id) THEN
        -- Delete the post
        DELETE FROM Posts WHERE post_id = in_post_id;
        -- Indicate success
        SET out_status = 1;
    ELSE
        -- Indicate failure or unauthorized
        SET out_status = 0;
    END IF;
END //

DELIMITER ;












