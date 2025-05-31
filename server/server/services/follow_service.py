from .user_service import get_user_by_id, get_user_by_username

def follow_user_service(current_user, username):
    user_to_follow = get_user_by_username(username)
    current_user.following.add(user_to_follow)
    return{
        "message": "Zaobserwowano pomyślnie!",
        "obserwator": current_user.id,
        "obserwowany" : user_to_follow.id
    }
def unfollow_user_service(current_user, username):
    user_to_unfollow = get_user_by_username(username)
    current_user.following.remove(user_to_unfollow)
    return{
        "message": "Odobserwowano pomyślnie!",
        "odobserwowany" : user_to_unfollow.id
    }

def get_following_service(username):
    user = get_user_by_username(username)
    following = user.following.all()
    following_data = [{"id": followed_user.id, "username": followed_user.username} for followed_user in following]
    return {
        "following":following_data,
        "following_count": following.count()}

def get_followers_service(username):
    user = get_user_by_username(username)
    followers = user.followers.all()
    followers_data = [{"id": follower.id, "username": follower.username} for follower in followers]
    return {
        "followers":followers_data,
        "followers_count": followers.count()}