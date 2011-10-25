/*
 * Start Twitter Style Flash Messages
 * */

//Provide a variable to hold the callback function
var notifyCallBack;

function showNotification(message, type, callback) {

    notifyCallBack = callback;

    var notification = $("#flash-message");
    notification.removeClass("success notice error");
    notification.addClass(type);

    //Make sure it's visible even when top of the page not visible
    notification.css("top", $(window).scrollTop());
    notification.css("width", $(document).width());

    $("#flash-message-list").html(message);

    //show the notification
    notification.slideDown("slow", function() {
    	setTimeout(hideNotification,4000)
    });
}

function hideNotification() {
    $("#flash-message").slideUp("slow", function() {
        if (null != notifyCallBack && (typeof notifyCallBack == "function")) {
            notifyCallBack();
        }
        //reset the callback variable
        notifyCallBack = null
    });
}

/*
 * End Twitter Style Flash Messages
 * */