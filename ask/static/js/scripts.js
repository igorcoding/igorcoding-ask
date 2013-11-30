jQuery.fn.center = function(parent) {
    if (parent) {
        parent = this.parent();
    } else {
        parent = window;
    }
    this.css({
        "position": "absolute",
        "top": ((($(parent).height() - this.outerHeight()) / 2) + $(parent).scrollTop() + "px"),
        "left": ((($(parent).width() - this.outerWidth()) / 2) + $(parent).scrollLeft() + "px")
    });
    return this;
};

function closeModal(modal) {
    //TODO: добавить проверку на наличие содержимого
    modal.fadeOut();
    $('.darking-thing').fadeOut();
    $('body').removeClass('stop-scrolling');
}

function showModal(modal) {
    var darker = $('.darking-thing');
    darker.fadeIn();

    modal.center(false);
    modal.fadeIn();
}

function setupCsrfAndAjax() {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        crossDomain: false, // obviates need for sameOrigin test
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
}


jQuery(document).ready(function($) {

    /*$('#feed-nav li').click(function(){
        $(this).parents('#feed-nav').children('li').removeClass('active');
        $(this).addClass('active');
    });*/

    setupCsrfAndAjax();

    $.toast.config.align = 'right';
    $.toast.config.closeForStickyOnly = false;

    $('.content-block .rating-button').click(function() {
        var content = $(this).parents('.content-block');
        var way = null;
        var link = null;
        var OK = true;

        if ($(this).hasClass('up-button'))
            way = 'up';
        else if ($(this).hasClass('down-button'))
            way = 'down';
        else
            OK = false;

        if (content.hasClass('question')) {
            link = '/rating/question/';
        }
        else if (content.hasClass('answer')) {
            link = '/rating/answer/';
        }
        else
            OK = false;

        if (OK)
        {
            $.ajax({
              type: "POST",
              url: link + way,
              data: {
                  content_id: content.data('id')
              }
            })
              .done(function( msg ) {
                    content.find('.rating').text(msg['rating']);
                    $('.user-rating-field').text(msg['user_rating']);
                    $.toast(msg['msg'], {sticky: false, type: msg['notify']});
                    //alert(msg['msg']);
              })
              .fail(function( msg ) {
                    $.toast(msg['msg'], {sticky: false, type: msg['notify']});
                    //alert(msg);
              });
            return false;
        }
        else
            $.toast("An error occurred. Try refreshing your page.", {sticky: true, type: 'danger'});
            //alert("An error occurred. Try refreshing your page.");
    });

/*
    $('.tag').click(function() {
        alert("tag");
    });
*/


    $(document).on('click', '.correctness.ratable', function() {
        var answer = $(this).parents('.answer');
        $.ajax({
          type: "POST",
          url: "/setcorrect/",
          data: {
              answer_id: answer.data('id')
          }
        })
          .done(function( msg ) {
                var correctnessObj = answer.find('.correctness');
                if (correctnessObj.hasClass('correct'))
                    correctnessObj.stop().removeClass('correct');
                else
                    correctnessObj.stop().addClass('correct');
                //alert(msg['msg']);
                $.toast(msg['msg'], {sticky: false, type: 'success'});
          })
            .fail(function(msg){
                $.toast(msg['msg'], {sticky: false, type: msg['danger']});
            });
        return false;
    });

    $('.correctness').hover(
        function(){
            if ($(this).hasClass('ratable'))
            {
                if ($(this).hasClass('correct'))
                    $(this).animate({'opacity': 0.2}, 300);
                else
                    $(this).animate({'opacity': 1}, 300);
            }
        },
        function() {
            if ($(this).hasClass('ratable'))
            {
                if ($(this).hasClass('correct'))
                    $(this).animate({'opacity': 1}, 300);
                else
                    $(this).animate({'opacity': 0.2}, 300);
            }
        }
    );









    var darker = $('.darking-thing');
    var loginModal = $('.login-modal');
    var askModal = $('.ask-modal');

    $('#modal_login').click(function() {
        showModal(loginModal);
    });

    $('#ask-button').click(function() {
        showModal(askModal);
    });

    darker.click(function() {
        closeModal(askModal);
        closeModal(loginModal);
    });

    $(document).keyup(function(e) {
        if (e.keyCode == 27) {    // esc
            if(loginModal.css("display") != "none") {
                closeModal(loginModal);
            }
            if(askModal.css("display") != "none") {
                closeModal(askModal);
            }
        }
    });

    $('.modal-close-button').hover(
    function() {
        $(this).animate({opacity : 1.0}, 100);
    },
    function() {
        $(this).animate({opacity : 0.5}, 100);
    });

    $('.modal-close-button').click(function() {
        closeModal(askModal);
    });


});
