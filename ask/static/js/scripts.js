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

function closeAskModal() {
    //TODO: добавить проверку на наличие содержимого
    $('.ask-modal').fadeOut();
    $('.darking-thing').fadeOut();
    $('body').removeClass('stop-scrolling');
}

jQuery(document).ready(function($) {
    $('.user_info').click(function() {
        var username = $(this).data('username');
        var req_url = $.param({username: username});
        document.location.href = "/user?" + req_url;
    });

    $('#user-feed-nav a').click(function() {
        var username = $('.user_info').data('username');
        var req_url = $.param({
                                username: username,
                                tab: $(this).parents('li').data('tab')});
        document.location.href = "/user?" + req_url;
    });


    $('.question, .answer').hover(
        function(){
            if (!$(this).hasClass('disable-hover'))
                $(this).addClass('hovered');
        },
        function(){
            if (!$(this).hasClass('disable-hover'))
                $(this).removeClass('hovered');
        }
    );

    $('#feed-nav li').click(function(){
        $(this).parents('#feed-nav').children('li').removeClass('active');
        $(this).addClass('active');
    });

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


    $('.question .up-button').click(function() {
        var question = $(this).parents('.question');
        $.ajax({
          type: "POST",
          url: "/qrating/",
          data: {
              q: $(this).parents('.question').data('id'),
              user_id: 1,
              way: "increase"
          }
        })
          .done(function( msg ) {
                question.find('.rating').text(msg['rating']);
                alert(msg['msg']);
          });
        return false;
    });

    $('.question .down-button').click(function() {
        var question = $(this).parents('.question');
        $.ajax({
          type: "POST",
          url: "/qrating/",
          data: {
              q: $(this).parents('.question').data('id'),
              user_id: 1,
              way: "decrease"
          }
        })
          .done(function( msg ) {
                question.find('.rating').text(msg['rating']);
                alert(msg['msg']);
          });
        return false;
    });

    $('.answer .up-button').click(function() {
        var answer = $(this).parents('.answer');
        $.ajax({
          type: "POST",
          url: "/arating/",
          data: {
              a: answer.data('id'),
              user_id: 1,
              way: "increase"
          }
        })
          .done(function( msg ) {
                answer.find('.rating').text(msg['rating']);
                alert(msg['msg']);
          });
        return false;
    });

    $('.answer .down-button').click(function() {
        var answer = $(this).parents('.answer');
        $.ajax({
          type: "POST",
          url: "/arating/",
          data: {
              a: answer.data('id'),
              user_id: 1,
              way: "decrease"
          }
        })
          .done(function( msg ) {
                answer.find('.rating').text(msg['rating']);
                alert(msg['msg']);
          });
        return false;
    });


    $('.tag').click(function() {
        alert("tag");
    });



    $(document).on('click', '.correctness.clickable', function() {
        var answer = $(this).parents('.answer');
        $.ajax({
          type: "POST",
          url: "setcorrect/",
          data: {
              answer_id: answer.data('id')
          }
        })
          .done(function( msg ) {
                answer.find('.correctness').stop().addClass('correct').removeClass('clickable');
                alert(msg['msg']);
          });
        return false;
    });

    $('.correctness').hover(
        function(){
            if (!$(this).hasClass('correct'))
            {
                $(this).animate({'opacity': 1}, 300);
                $(this).addClass('clickable');
            }
        },
        function() {
            if (!$(this).hasClass('correct'))
            {
                $(this).animate({'opacity': 0.1}, 300);
                $(this).removeClass('clickable');
            }
        }
    );









    var darker = $('.darking-thing');
    var modal = $('.ask-modal');

    $('#ask-button').click(function() {
        //$('#askModal').modal({"show":true});
        //$('body').addClass('stop-scrolling');
        darker.fadeIn();

        modal.center(false);
        modal.fadeIn();
    });

    darker.click(function() {
        closeAskModal();

    });

    $(document).keyup(function(e) {
        if (e.keyCode == 27) {    // esc
            if(modal.css("display") != "none") {
                closeAskModal();
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
        closeAskModal();
    });


});
