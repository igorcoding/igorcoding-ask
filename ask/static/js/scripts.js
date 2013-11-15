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
        alert("some user info");
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

    $('.up-button').click(function() {
        var question = $(this).parents('.question');
        $.ajax({
          type: "GET",
          url: "qrating/",
          data: {
              q: $(this).parents('.question').data('id'),
              way: "increase"
          }
        })
          .done(function( msg ) {
                question.find('.rating').text(msg['rating']);
                alert(msg['msg']);
          });
    });

    $('.down-button').click(function() {
        var question = $(this).parents('.question');
        $.ajax({
          type: "GET",
          url: "qrating/",
          data: {
              q: $(this).parents('.question').data('id'),
              way: "decrease"
          }
        })
          .done(function( msg ) {
                question.find('.rating').text(msg['rating']);
                alert(msg['msg']);
          });
    });


    $('.tag').click(function() {
        alert("tag");
    });







    var darker = $('.darking-thing');
    var modal = $('.ask-modal');

    $('#ask-button').click(function() {
        //$('#askModal').modal({"show":true});
        $('body').addClass('stop-scrolling');
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
