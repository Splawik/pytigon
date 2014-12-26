        {% block jquery_ovr %}var options =
            success: RefreshWin
        function RefreshWin(responseText, statusText):
            start = responseText.indexOf("RETURN_OK")
            if(start > 0 ):
               $("#TableFiltr").submit()
               $('#dialog-form').dialog('close')
            else:
            8   $("#dialog-data").html(responseText)
        {% endblock %}

        $("#dialog-form-error").dialog({
            autoOpen: false
            buttons: {'Zamknij': function() { $(this).dialog('close'); } }
            width: 800

        $("#dialog-form-info").dialog({
            autoOpen: false
            buttons: { 'Zamknij': function() { $(this).dialog('close'); } }
            width: 600

        $("#dialog-form").dialog({
            autoOpen: false {% if form_height %}, height: {{form_height}}{% endif %} {% if form_width %},width: {{form_width}}{% endif %}
            buttons: { 'OK': function() { $("#DialogForm").ajaxSubmit(options); }, 'Anuluj': function() { $(this).dialog('close'); }, 'Pomoc': function() { window.open("{{URL_BASE}}/schwiki/{{title|wiki}}/view/"); } }
            close: function() {}

        $("#dialog-form-delete").dialog({
            autoOpen: false
            dialogClass: alert {% if form_delete_height %}, height: {{form_delete_height}}{% endif %} {% if form_delete_width %}, width: {{form_delete_width}}{% endif %}
            buttons: { 'OK': function() { $("#DialogFormDelete").ajaxSubmit(options); }, 'Anuluj': function() { $(this).dialog('close'); }}
            close: function() {}

        function popup_init():
            $('#popupform').button().click(
                function():
                    $("#dialog-data").load($(this).attr("href"),null,DialogExLoad1)

            $('a.popup[is_button!="1"]').button().attr('is_button','1').click(
                function():
                    if($(this).attr("href").indexOf('127.0.0.2')>=0):
                        $.get($(this).attr("href")+"|dialog-data",null,DialogExLoad1)
                    else:
                        $("#dialog-data").load($(this).attr("href"),null,DialogExLoad1)
                    return false

            $('a.popup_delete').button().click(
                function():
                    if($(this).attr("href").indexOf('127.0.0.2')>=0):
                        $.get($(this).attr("href")+"|dialog-data-delete",null,DialogExLoadDelete)
                    else:
                        $("#dialog-data-delete").load($(this).attr("href"),null,DialogExLoadDelete)
                    return false


            $('a.thickbox').button().click(
                function():
                    $("#dialog-data-info").load($(this).attr("href"),null,DialogExLoadInfo); return false
            $('a.button').button()

        {% block popup_init %}popup_init();{% endblock %}

        function DialogExLoad1(responseText, status, response):
            date_init()
            $('#dialog-form').dialog('open')
            {% block on_dialog_load %}{% endblock %}

        function DialogExLoad2(responseText, status, response):
            popup_init()

        function DialogExLoadInfo(responseText, status, response):
            $('#dialog-form-info').dialog('open')

        function DialogExLoadDelete(responseText, status, response):
            date_init()
            $('#dialog-form-delete').dialog('open')


        $(document).ajaxError(
            function(request, settings):
                var start,end
                start = settings.responseText.indexOf("<body>")
                end = settings.responseText.lastIndexOf("</body>")
                if (start > 0 && end > 0):
                    $("#dialog-data-error").html(settings.responseText.substring(start+6,end-1))
                    if ( $('#dialog-form-error').dialog( "isOpen" )==false):
                        $('#dialog-form-error').dialog('open')
                    if ( $('#dialog-form').dialog( "isOpen" )==true):
                        $('#dialog-form').dialog('close')

        function date_init():
            $('input.jqcalendar').datepicker
                $.extend(
                    {}
                    $.datepicker.regional["pl"]
                    {
                        dateFormat: $.datepicker.ISO_8601
                        showOn: "both"
                        buttonImage: "{{ STATIC_URL }}icons/calendar.png"
                        buttonImageOnly: true
                        duration: ""

        date_init();


