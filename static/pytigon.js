var RET_BUFOR;
var RET_OBJ;

function cmd_to_python(value) {
    document.title = ':';
    document.title = ':'+value;
}


function is_hybrid() {
    if(window.location.host == '127.0.0.2') return true; else return false;
}


function to_absolute_url(url) {
    //return window.location.protocol + "//" + window.location.host + "/" + window.location.pathname;
    if(url[0]=='/') {
        return window.location.protocol + "//" + window.location.host  + url;
    }
    else {
        return window.location.protocol + "//" + window.location.host  + window.location.pathname + "/" + url;
    }
}


function ret_submit() {
    RET_OBJ(RET_BUFOR,"OK")
}


function ajax_submit(form, func) {
    if( is_hybrid() ) {
        var queryString = form.formSerialize();
        cmd_to_python('href_to_var|'+to_absolute_url(form.attr('action'))+'?'+queryString+'|RET_BUFOR');
        RET_OBJ = func;
        cmd_to_python('run_js|ret_submit();');
    }
    else {
        form.ajaxSubmit( { success: func } );
    }
}
