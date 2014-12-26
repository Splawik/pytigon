function stick_resize() {
	var dy_win, dy_html, dy_table, dy;
	
	dy_win = $(window).height()-20;
	dy_html = $('body').height();
	dy_table =  $("#tbl_scroll").height();
	
	dy=dy_html - dy_win;
	dy = dy_table-dy;
	if(dy<100)  dy = 100;  

	$('#tbl_scroll').height(dy);
};

function resize_win() {
    var tab2 = [], tab_width
    stick_resize();

    tab_width = $("table[name='tabsort']").width()
    $("#tbl_header").width(tab_width)

    $("table[name='tabsort'] tr:first td").each(function() {
        tab2.push($(this).width())
    });
    tab2 = tab2.reverse();
    $("#tbl_header th").each(function() {
        $(this).width(tab2.pop());
    });
}

function stick_header() {
	var table, tab = [], tab2 = [],  x;

	$("table.tabsort th").each(function() {
		tab.push($(this).width())
	});
	
	table = $('<table id="tbl_header" class="tabsort" style="overflow-x: hidden;"></table>')
	table.append( $("table.tabsort thead") );
	
	$('#tbl_scroll').before(table);

	$("#tbl_header th").each(function() {
		tab2.push($(this).width());
	});

    tab2 = tab2.reverse();

    $("table[name='tabsort'] tr:first td").each(function() {
        x = tab2.pop()
        if(x>$(this).width()) {
            $(this).css("min-width", x)
        }
    });

	tab = tab.reverse();
	$("#tbl_header th").each(function() {
		$(this).width(tab.pop());
	});	

	$(window).resize(resize_win);

	resize_win();
};

