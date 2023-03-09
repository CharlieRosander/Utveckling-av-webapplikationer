var originalTitle = document.title;
function showUnreadCount(unread) {
    document.title = originalTitle + "(" + unread + " new messages!)";
}
showUnreadCount(3);