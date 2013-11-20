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
                    alert(msg['msg']);
              })
              .fail(function( msg ) {
                    alert(msg);
              });
            return false;
        }
        else
            alert("An error occurred. Try refreshing your page.");
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
        showModal(modal);
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
