from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import mysql.connector
from mysql.connector import Error
from datetime import datetime
#from flask import session
import base64
import os

app = Flask(__name__)
#app.secret_key = 'mysql'
CORS(app)


def create_db_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='project',
            user='root',
            password='mysql123'
        )
        return connection
    except mysql.connector.Error as err:
        print("MySQL Error: ", err)
        return None

def call_insert_user_procedure(data):
    try:
        #connection = mysql.connector.connect(host=os.getenv('MYSQL_HOST', 'localhost'),database=os.getenv('MYSQL_DATABASE', 'project'),user=os.getenv('MYSQL_USER', 'root'),password=os.getenv('MYSQL_PASSWORD', 'mysql123'))
        connection = create_db_connection()
        if connection is None:
            return jsonify({"error": "Database error"}), 500
        cursor = connection.cursor()
        cursor.callproc('InsertUser', [
            data['NUID'],
            data['first_name'],
            data['last_name'],
            data['email'],
            data['phone_number'],
            data['profile_picture'],
            data['degree'],
            data['major'],
            data['college'],
            data['password'],
        ])
        
        for result in cursor.stored_results():
            lastrowid = result.fetchone()[0]
        
        connection.commit()
        print(lastrowid)
        return lastrowid
    except mysql.connector.Error as err:
        print("MySQL Error: ", err)
        return jsonify({"error": "Database error", "details": str(err)}), 500
    except Error as e:
        print(f"Error: {e}")
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

  


@app.route('/users', methods=['POST'])
#@cross_origin(origin='*', headers=['Content-Type','Authorization'])  # Or specify domains
def create_user():
    if request.method == 'OPTIONS':
        # Preflight request; the browser expects status 200 with appropriate headers
        response = app.make_default_options_response()
        return response
    data = request.get_json()
    try:
        user_id = call_insert_user_procedure(data)
        if user_id:
            return jsonify({"message": "User created successfully.", "user_id": user_id}), 201
        else:
            return jsonify({"error": "Failed to create user."}), 500
    except mysql.connector.Error as err:
        # MySQL error occurred, return a JSON response with the error
        print("MySQL Error: ", err)
        return jsonify({"error": "Database error", "details": str(err)}), 500
    except Exception as e:
        # General error occurred, return a JSON response with the error
        print("Exception occurred:", e)
        return jsonify({"error": "Failed to create user.", "details": str(e)}), 500


def get_user_id_from_credentials(email):
    connection = None
    try:
        #connection = mysql.connector.connect(host=os.getenv('MYSQL_HOST', 'localhost'),database=os.getenv('MYSQL_DATABASE', 'project'),user=os.getenv('MYSQL_USER', 'root'),password=os.getenv('MYSQL_PASSWORD', 'mysql123'))
        connection = create_db_connection()
        if connection is None:
            return jsonify({"error": "Database error"}), 500
        cursor = connection.cursor()

        cursor.callproc('GetUserIdFromCredentials', [email])
        
        # Fetch the result
        user_record = None
        for result in cursor.stored_results():
            user_record = result.fetchone()

        if user_record:
            return user_record[0],user_record[1]  # Return user_id
        else:
            return None

    except mysql.connector.Error as error:
        print(f"Database Error: {error}")
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()




@app.route('/login', methods=['POST'])
#@cross_origin(origin='*', headers=['Content-Type','Authorization'])
def login_user():
    data = request.get_json()
    connection = None
    try:

        #connection = mysql.connector.connect(host=os.getenv('MYSQL_HOST', 'localhost'),database=os.getenv('MYSQL_DATABASE', 'project'),user=os.getenv('MYSQL_USER', 'root'),password=os.getenv('MYSQL_PASSWORD', 'mysql123'))
        connection = create_db_connection()
        if connection is None:
            return jsonify({"error": "Database error"}), 500
        cursor = connection.cursor()

        valid_login = cursor.callproc('UserLogin', [data['email'], data['password'], 0])

        if valid_login[2]:
            user_id,nuid = get_user_id_from_credentials(data['email'])

            return jsonify({"success": True, "User":user_id, "NUID":nuid}), 200
        else:
            return jsonify({"success": False, "message": "Invalid credentials"}), 401
    except mysql.connector.Error as err:
        print("MySQL Error: ", err)
        return jsonify({"error": "Database error", "details": str(err)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@app.route('/search_users', methods=['POST'])
def search_users():
    data = request.get_json()
    search_term = data['search']
    try:
        #connection = mysql.connector.connect(host=os.getenv('MYSQL_HOST', 'localhost'),database=os.getenv('MYSQL_DATABASE', 'project'),user=os.getenv('MYSQL_USER', 'root'),password=os.getenv('MYSQL_PASSWORD', 'mysql123'))
        connection = create_db_connection()
        if connection is None:
            return jsonify({"error": "Database error"}), 500
        cursor = connection.cursor(dictionary=True)
        cursor.callproc('SearchUsers', [search_term])
        users = []
        for result in cursor.stored_results():
            for row in result.fetchall():
                # No need to encode as Base64 here, just append the row as is
                users.append(row)
            
        return jsonify(users), 200
    except mysql.connector.Error as error:
        return jsonify({"error": str(error)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


@app.route('/follow_user', methods=['POST'])
def follow_user():
    data = request.get_json()
    follower_id = data['follower_id']
    followed_id = data['followed_id']
    follow_date = data['follow_date']  # Format: YYYY-MM-DDTHH:MM:SS (ISO 8601 format)


    follow_date_parsed = datetime.fromisoformat(follow_date.rstrip('Z'))
    follow_date_mysql_format = follow_date_parsed.strftime('%Y-%m-%d %H:%M:%S')
    try:
        #connection = mysql.connector.connect(host=os.getenv('MYSQL_HOST', 'localhost'),database=os.getenv('MYSQL_DATABASE', 'project'),user=os.getenv('MYSQL_USER', 'root'),password=os.getenv('MYSQL_PASSWORD', 'mysql123'))
        connection = create_db_connection()
        if connection is None:
            return jsonify({"error": "Database error"}), 500
        cursor = connection.cursor()
        cursor.callproc('FollowUser', [follower_id, followed_id, follow_date_mysql_format])
        connection.commit()
        return jsonify({"message": "Followed successfully"}), 200
    except mysql.connector.Error as error:
        return jsonify({"error": str(error)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@app.route('/get_followers/<int:userId>', methods=['GET'])
def get_followers(userId):
    try:
        #connection = mysql.connector.connect(host=os.getenv('MYSQL_HOST', 'localhost'),database=os.getenv('MYSQL_DATABASE', 'project'),user=os.getenv('MYSQL_USER', 'root'),password=os.getenv('MYSQL_PASSWORD', 'mysql123'))
        connection = create_db_connection()
        if connection is None:
            return jsonify({"error": "Database error"}), 500
        cursor = connection.cursor(dictionary=True)

        cursor.callproc('GetFollowers', [userId])
        followers = []
        for result in cursor.stored_results():
            followers = result.fetchall()
        return jsonify(followers), 200
    except mysql.connector.Error as error:
        return jsonify({"error": str(error)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@app.route('/get_following/<int:userId>', methods=['GET'])
def get_following(userId):
    try:
        #connection = mysql.connector.connect(host=os.getenv('MYSQL_HOST', 'localhost'),database=os.getenv('MYSQL_DATABASE', 'project'),user=os.getenv('MYSQL_USER', 'root'),password=os.getenv('MYSQL_PASSWORD', 'mysql123'))
        connection = create_db_connection()
        if connection is None:
            return jsonify({"error": "Database error"}), 500
        cursor = connection.cursor(dictionary=True)

        cursor.callproc('GetFollowing', [userId])
        following = []
        for result in cursor.stored_results():
            following = result.fetchall()
        return jsonify(following), 200
    except mysql.connector.Error as error:
        return jsonify({"error": str(error)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


@app.route('/unfollow_user', methods=['POST'])
def unfollow_user():
    data = request.get_json()
    follower_id = data['follower_id']
    followed_id = data['followed_id']

    try:
        #connection = mysql.connector.connect(host=os.getenv('MYSQL_HOST', 'localhost'),database=os.getenv('MYSQL_DATABASE', 'project'),user=os.getenv('MYSQL_USER', 'root'),password=os.getenv('MYSQL_PASSWORD', 'mysql123'))
        connection = create_db_connection()
        if connection is None:
            return jsonify({"error": "Database error"}), 500
        cursor = connection.cursor()
        cursor.callproc('UnfollowUser', [follower_id, followed_id])

        connection.commit()
        return jsonify({"message": "Unfollowed successfully"}), 200
    except mysql.connector.Error as error:
        return jsonify({"error": str(error)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


@app.route('/submit_report', methods=['POST'])
def submit_report():
    data = request.get_json()
    reporter_id = data['reporter_id']
    reported_id = data['reported_id']
    report_category = data['report_category']
    report_description = data['report_description']
    report_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


    try:
        #connection = mysql.connector.connect(host=os.getenv('MYSQL_HOST', 'localhost'),database=os.getenv('MYSQL_DATABASE', 'project'),user=os.getenv('MYSQL_USER', 'root'),password=os.getenv('MYSQL_PASSWORD', 'mysql123'))
        connection = create_db_connection()
        if connection is None:
            return jsonify({"error": "Database error"}), 500
        cursor = connection.cursor()
        cursor.callproc('InsertReport', [reporter_id, reported_id, report_category, report_description,report_time])
        connection.commit()
        return jsonify({"message": "Report submitted successfully"}), 200
    except mysql.connector.Error as error:
        return jsonify({"error": str(error)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


@app.route('/create_group', methods=['POST'])
def create_group():
    group_name = request.form['group_name']
    description = request.form['description']
    group_image = request.files['group_image'].read()
    date_created = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Convert image to base64
    group_image_base64 = base64.b64encode(group_image).decode('utf-8')

    try:
        #connection = mysql.connector.connect(host=os.getenv('MYSQL_HOST', 'localhost'),database=os.getenv('MYSQL_DATABASE', 'project'),user=os.getenv('MYSQL_USER', 'root'),password=os.getenv('MYSQL_PASSWORD', 'mysql123'))
        connection = create_db_connection()
        if connection is None:
            return jsonify({"error": "Database error"}), 500
        cursor = connection.cursor()


        cursor.callproc('CreateGroup', [group_name, description, date_created, group_image_base64])
        connection.commit()
        return jsonify({"message": "Group created successfully"}), 201
    except mysql.connector.Error as error:
        return jsonify({"error": str(error)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()



@app.route('/get_groups', methods=['GET'])
def get_groups():
    try:
        #connection = mysql.connector.connect(host=os.getenv('MYSQL_HOST', 'localhost'),database=os.getenv('MYSQL_DATABASE', 'project'),user=os.getenv('MYSQL_USER', 'root'),password=os.getenv('MYSQL_PASSWORD', 'mysql123'))
        connection = create_db_connection()
        if connection is None:
            return jsonify({"error": "Database error"}), 500
        cursor = connection.cursor(dictionary=True)

        cursor.callproc('GetGroups')
        groups = []
        for result in cursor.stored_results():
            groups = result.fetchall()
        return jsonify(groups), 200
    except mysql.connector.Error as error:
        return jsonify({"error": str(error)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@app.route('/join_group', methods=['POST'])
def join_group():
    data = request.get_json()
    NUID = data['NUID']
    group_name = data['group_name']

    try:
        #connection = mysql.connector.connect(host=os.getenv('MYSQL_HOST', 'localhost'),database=os.getenv('MYSQL_DATABASE', 'project'),user=os.getenv('MYSQL_USER', 'root'),password=os.getenv('MYSQL_PASSWORD', 'mysql123'))
        connection = create_db_connection()
        if connection is None:
            return jsonify({"error": "Database error"}), 500
        cursor = connection.cursor()
        cursor.callproc('JoinGroup', [NUID, group_name])
        connection.commit()
        return jsonify({"message": "Joined group successfully"}), 200
    except mysql.connector.Error as error:
        return jsonify({"error": str(error)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


@app.route('/get_reports/<int:userId>', methods=['GET'])
def get_reports(userId):
    try:
        #connection = mysql.connector.connect(host=os.getenv('MYSQL_HOST', 'localhost'),database=os.getenv('MYSQL_DATABASE', 'project'),user=os.getenv('MYSQL_USER', 'root'),password=os.getenv('MYSQL_PASSWORD', 'mysql123'))
        connection = create_db_connection()
        if connection is None:
            return jsonify({"error": "Database error"}), 500
        cursor = connection.cursor(dictionary=True)
        
        # Call the stored procedure
        cursor.callproc('GetReportsByUserId', [userId])
        reports = []
        for result in cursor.stored_results():
            reports = result.fetchall()
        return jsonify(reports)
    except mysql.connector.Error as error:
        return jsonify({"error": str(error)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()





@app.route('/check_follow_status/<int:currentUserId>/<int:followedUserId>', methods=['GET'])
def check_follow_status(currentUserId, followedUserId):
    try:
        #connection = mysql.connector.connect(host=os.getenv('MYSQL_HOST', 'localhost'),database=os.getenv('MYSQL_DATABASE', 'project'),user=os.getenv('MYSQL_USER', 'root'),password=os.getenv('MYSQL_PASSWORD', 'mysql123'))
        connection = create_db_connection()
        if connection is None:
            return jsonify({"error": "Database error"}), 500
        cursor = connection.cursor()

        # Call the stored procedure
        cursor.callproc('CheckFollowStatus', [currentUserId, followedUserId])
        follows = False
        for result in cursor.stored_results():
            follows = result.fetchone()[0] > 0
        
        return jsonify({"follows": follows}), 200
    except mysql.connector.Error as error:
        return jsonify({"error": str(error)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    sender_id = data['sender_id']
    receiver_id = data['receiver_id']
    message_body = data['message_body']
    message_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    try:
        #connection = mysql.connector.connect(host=os.getenv('MYSQL_HOST', 'localhost'),database=os.getenv('MYSQL_DATABASE', 'project'),user=os.getenv('MYSQL_USER', 'root'),password=os.getenv('MYSQL_PASSWORD', 'mysql123'))
        connection = create_db_connection()
        if connection is None:
            return jsonify({"error": "Database error"}), 500
        cursor = connection.cursor()
        cursor.callproc('InsertMessage', [sender_id, receiver_id, message_body, message_date])
        connection.commit()
        return jsonify({"message": "Message sent successfully"}), 200
    except mysql.connector.Error as error:
        return jsonify({"error": str(error)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


@app.route('/get_messages/<int:user1Id>/<int:user2Id>', methods=['GET'])
def get_messages(user1Id, user2Id):
    try:
        #connection = mysql.connector.connect(host=os.getenv('MYSQL_HOST', 'localhost'),database=os.getenv('MYSQL_DATABASE', 'project'),user=os.getenv('MYSQL_USER', 'root'),password=os.getenv('MYSQL_PASSWORD', 'mysql123'))
        connection = create_db_connection()
        if connection is None:
            return jsonify({"error": "Database error"}), 500
        cursor = connection.cursor(dictionary=True)
        
        # Call the stored procedure
        cursor.callproc('GetMessages', [user1Id, user2Id])
        messages = []
        for result in cursor.stored_results():
            messages = result.fetchall()
        return jsonify(messages), 200
    except mysql.connector.Error as error:
        return jsonify({"error": str(error)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()



@app.route('/get_all_users', methods=['GET'])
def get_all_users():
    try:
        #connection = mysql.connector.connect(host=os.getenv('MYSQL_HOST', 'localhost'),database=os.getenv('MYSQL_DATABASE', 'project'),user=os.getenv('MYSQL_USER', 'root'),password=os.getenv('MYSQL_PASSWORD', 'mysql123'))
        connection = create_db_connection()
        if connection is None:
            return jsonify({"error": "Database error"}), 500
        cursor = connection.cursor(dictionary=True)
        
        # Call the stored procedure
        cursor.callproc('GetAllUsers')
        users = []
        for result in cursor.stored_results():
            users = result.fetchall()
        return jsonify(users), 200
    except mysql.connector.Error as error:
        return jsonify({"error": str(error)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()




@app.route('/get_followers_posts/<int:userId>', methods=['GET'])
def get_followers_posts(userId):
    try:
        #connection = mysql.connector.connect(host=os.getenv('MYSQL_HOST', 'localhost'),database=os.getenv('MYSQL_DATABASE', 'project'),user=os.getenv('MYSQL_USER', 'root'),password=os.getenv('MYSQL_PASSWORD', 'mysql123'))
        connection = create_db_connection()
        if connection is None:
            return jsonify({"error": "Database error"}), 500
        cursor = connection.cursor(dictionary=True)
        
        # Call the stored procedure
        cursor.callproc('GetFollowersPosts', [userId])
        posts = []
        for result in cursor.stored_results():
            posts = result.fetchall()
        return jsonify(posts), 200
    except mysql.connector.Error as error:
        return jsonify({"error": str(error)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()





@app.route('/create_post', methods=['POST'])
def create_post():
    user_id = request.form['user_id']
    caption = request.form['caption']
    post_image = request.files['post_image'].read()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Convert image to base64
    post_image_base64 = base64.b64encode(post_image).decode('utf-8')

    try:
        #connection = mysql.connector.connect(host=os.getenv('MYSQL_HOST', 'localhost'),database=os.getenv('MYSQL_DATABASE', 'project'),user=os.getenv('MYSQL_USER', 'root'),password=os.getenv('MYSQL_PASSWORD', 'mysql123'))
        connection = create_db_connection()
        if connection is None:
            return jsonify({"error": "Database error"}), 500
        cursor = connection.cursor()
        
        # Call the stored procedure
        cursor.callproc('CreatePost', [user_id, caption, post_image_base64, timestamp])
        connection.commit()

        return jsonify({"message": "Post created successfully"}), 201
    except mysql.connector.Error as error:
        return jsonify({"error": str(error)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()




@app.route('/get_user_posts/<int:userId>', methods=['GET'])
def get_user_posts(userId):
    try:
        #connection = mysql.connector.connect(host=os.getenv('MYSQL_HOST', 'localhost'),database=os.getenv('MYSQL_DATABASE', 'project'),user=os.getenv('MYSQL_USER', 'root'),password=os.getenv('MYSQL_PASSWORD', 'mysql123'))
        connection = create_db_connection()
        if connection is None:
            return jsonify({"error": "Database error"}), 500
        cursor = connection.cursor(dictionary=True)
        
        # Call the stored procedure to get posts
        cursor.callproc('GetUserPosts', [userId])
        posts = []
        for result in cursor.stored_results():
            posts = result.fetchall()

        for post in posts:
            post_id = post['post_id']

            # Call stored procedure for comments
            cursor.callproc('GetPostComments', [post_id])
            comments_result = next(cursor.stored_results()).fetchall()  # Corrected line
            post['comments'] = comments_result

            # Call stored procedure for like count
            cursor.callproc('GetPostLikeCount', [post_id])
            like_count_result = next(cursor.stored_results()).fetchall()
            post['like_count'] = like_count_result[0]['like_count'] if like_count_result else 0

        return jsonify(posts), 200
    except mysql.connector.Error as error:
        return jsonify({"error": str(error)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()




@app.route('/get_followed_users_posts/<int:userId>', methods=['GET'])
def get_followed_users_posts(userId):
    try:
        #connection = mysql.connector.connect(host=os.getenv('MYSQL_HOST', 'localhost'),database=os.getenv('MYSQL_DATABASE', 'project'),user=os.getenv('MYSQL_USER', 'root'),password=os.getenv('MYSQL_PASSWORD', 'mysql123'))
        connection = create_db_connection()
        if connection is None:
            return jsonify({"error": "Database error"}), 500
        cursor = connection.cursor(dictionary=True)

        # Call the stored procedure to get followed users' posts
        cursor.callproc('GetFollowedUsersPosts', [userId])
        posts = []
        for result in cursor.stored_results():
            posts = result.fetchall()

        for post in posts:
            post_id = post['post_id']

            # Call stored procedure for comments
            cursor.callproc('GetPostComments', [post_id])
            comments_result = next(cursor.stored_results()).fetchall()
            post['comments'] = comments_result

            # Call stored procedure for like count
            cursor.callproc('GetPostLikeCount', [post_id])
            like_count_result = next(cursor.stored_results()).fetchall()
            post['like_count'] = like_count_result[0]['like_count'] if like_count_result else 0

        return jsonify(posts), 200
    except mysql.connector.Error as error:
        return jsonify({"error": str(error)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


@app.route('/add_comment', methods=['POST'])
def add_comment():
    data = request.get_json()
    post_id = data['post_id']
    user_id = data['user_id']
    comment = data['comment']
    comment_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    try:
        #connection = mysql.connector.connect(host=os.getenv('MYSQL_HOST', 'localhost'),database=os.getenv('MYSQL_DATABASE', 'project'),user=os.getenv('MYSQL_USER', 'root'),password=os.getenv('MYSQL_PASSWORD', 'mysql123'))
        connection = create_db_connection()
        if connection is None:
            return jsonify({"error": "Database error"}), 500
        cursor = connection.cursor()
        cursor.callproc('AddComment', [post_id, user_id, comment, comment_date])
        connection.commit()
        return jsonify({"message": "Comment added successfully"}), 201
    except mysql.connector.Error as error:
        return jsonify({"error": str(error)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()




@app.route('/toggle_like', methods=['POST'])
def toggle_like():
    data = request.get_json()
    user_id = data['user_id']
    post_id = data['post_id']

    try:
        #connection = mysql.connector.connect(host=os.getenv('MYSQL_HOST', 'localhost'),database=os.getenv('MYSQL_DATABASE', 'project'),user=os.getenv('MYSQL_USER', 'root'),password=os.getenv('MYSQL_PASSWORD', 'mysql123'))
        connection = create_db_connection()
        if connection is None:
            return jsonify({"error": "Database error"}), 500
        cursor = connection.cursor()

        # Call the stored procedure to check if like exists
        cursor.callproc('CheckLikeExists', [user_id, post_id])
        like_exists = None
        for result in cursor.stored_results():
            like_exists = result.fetchone()[0]

        if like_exists:
            # Call the stored procedure to remove the like
            cursor.callproc('DeleteLike', [user_id, post_id])
            message = "Like removed"
        else:
            # Call the stored procedure to add the like
            like_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.callproc('InsertLike', [user_id, post_id, like_date])
            message = "Like added"

        connection.commit()
        return jsonify({"message": message}), 200

    except mysql.connector.Error as error:
        return jsonify({"error": str(error)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()




@app.route('/get_comments/<int:post_id>', methods=['GET'])
def get_comments(post_id):
    try:
        #connection = mysql.connector.connect(host=os.getenv('MYSQL_HOST', 'localhost'),database=os.getenv('MYSQL_DATABASE', 'project'),user=os.getenv('MYSQL_USER', 'root'),password=os.getenv('MYSQL_PASSWORD', 'mysql123'))
        connection = create_db_connection()
        if connection is None:
            return jsonify({"error": "Database error"}), 500
        cursor = connection.cursor(dictionary=True)

        # Call the stored procedure
        cursor.callproc('GetComments', [post_id])

        # Fetch the results
        comments = []
        for result in cursor.stored_results():
            comments = result.fetchall()

        return jsonify(comments), 200
    except mysql.connector.Error as error:
        return jsonify({"error": str(error)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()



@app.route('/update_user', methods=['POST'])
def update_user():
    data = request.get_json()
    user_id = data['user_id']
    field = data['field']
    value = data['value']

    try:
        #connection = mysql.connector.connect(host=os.getenv('MYSQL_HOST', 'localhost'),database=os.getenv('MYSQL_DATABASE', 'project'),user=os.getenv('MYSQL_USER', 'root'),password=os.getenv('MYSQL_PASSWORD', 'mysql123'))
        connection = create_db_connection()
        if connection is None:
            return jsonify({"error": "Database error"}), 500
        cursor = connection.cursor()
        
        # Call the stored procedure
        cursor.callproc('UpdateUser', [user_id, field, value])

        connection.commit()
        
        return jsonify({"message": f"{field} updated successfully"}), 200
    except mysql.connector.Error as error:
        return jsonify({"error": str(error)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()



@app.route('/delete_post/<int:postId>', methods=['DELETE'])
def delete_post(postId):
    data = request.get_json()
    user_id = data['user_id']

    try:
        # Establish the database connection
        #connection = mysql.connector.connect(host=os.getenv('MYSQL_HOST', 'localhost'),database=os.getenv('MYSQL_DATABASE', 'project'),user=os.getenv('MYSQL_USER', 'root'),password=os.getenv('MYSQL_PASSWORD', 'mysql123'))
        connection = create_db_connection()
        if connection is None:
            return jsonify({"error": "Database error"}), 500
        cursor = connection.cursor()

        # Prepare the query to call the stored procedure
        query = "CALL DeletePost(%s, %s, @out_status); SELECT @out_status;"
        cursor.execute(query, (postId, user_id))

        # Fetch the result
        cursor.nextset()  # Skip the results of the CALL statement
        out_status = cursor.fetchone()[0]
        connection.commit()

        # Return the response based on the status
        if out_status == 1:
            return jsonify({"message": "Post deleted successfully"}), 200
        else:
            return jsonify({"error": "Failed to delete post or unauthorized action"}), 403

    except mysql.connector.Error as error:
        return jsonify({"error": str(error)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()




if __name__ == '__main__':
    app.run(debug=True)

