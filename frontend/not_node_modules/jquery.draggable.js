(function($) {
    $.fn.drags = function(opt) {

        var $el;

        opt = $.extend({handle: '', cursor: 'move', windowLock: true}, opt);

        $el = ('' === opt.handle) ? this : this.find(opt.handle);

        return $el
            .css('cursor', opt.cursor)
            .on('mousedown', function(e) {

                var $this = $(this),
                    $drag = ("" === opt.handle) ? $this.addClass('draggable') : $this.addClass('active-handle').parent().addClass('draggable'),
                    z_idx = $drag.css('z-index'),
                    drg_h = $drag.outerHeight(),
                    drg_w = $drag.outerWidth(),
                    pos_y = $drag.offset().top + drg_h - e.pageY,
                    pos_x = $drag.offset().left + drg_w - e.pageX;

                $drag.css('z-index', 1000).parents()
                    .on('mousemove', function(e) {

                        var top = e.pageY + pos_y - drg_h,
                            left = e.pageX + pos_x - drg_w,
                            ch, cw;

                        if(true === opt.windowLock) {
                            ch = $(window).height();
                            cw = $(window).width();

                            top = (top < 0) ? 0 : top;
                            //top = (top + drg_h > ch) ? ch - drg_h : top;

                            left = (left < 0) ? 0 : left;
                            //left = (left + drg_w > cw) ? cw - drg_w : left;
                        }

                        $('.draggable')
                            .offset({
                                top: top,
                                left: left
                            })
                            .on('mouseup', function() {
                                $(this).removeClass('draggable').css('z-index', z_idx);
                            });

                    });

                e.preventDefault(); // disable selection
            })
            .on('mouseup', function() {
                if('' === opt.handle) {
                    $(this).removeClass('draggable');
                } else {
                    $(this).removeClass('active-handle').parent().removeClass('draggable');
                }
            });
    };
})(jQuery);