def img_field(elem):
    txt = jQuery(elem).val().replace( __new__(RegExp("^.*[\\\ /]")), '')
    jQuery(elem).closest('label').find('.upload').html(txt)

    if elem.files and elem.files[0]:
        file_name = elem.files[0].js_name
        ext = [ '.jpeg', '.jpg', '.svg', '.gif', '.png']
        test = False
        for pos in ext:
            if pos in file_name:
                test= True
                break
        if test:
            reader = __new__(FileReader())

            def _onload(e):
                nonlocal elem
                x = jQuery(elem).closest('label').find('img')
                if x.length>0:
                    x.remove()
                img = jQuery("<img style='float: left; max-height: 48px; max-width: 48px;'/>")
                img.insertAfter(jQuery(elem).closest('label').find('input'))
                img.attr('src', e.target.result)

        reader.onload = _onload
        reader.readAsDataURL(elem.files[0])

window.img_field = img_field
