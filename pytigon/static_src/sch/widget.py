def humanFileSize(bytes, si):
    if si:
        thresh = 1000
    else:
        thresh =  1024
    if Math.abs(bytes) < thresh:
        return bytes + ' B', 0
    if si:
        units = ['kB','MB','GB','TB','PB','EB','ZB','YB']
    else:
        units = ['KiB','MiB','GiB','TiB','PiB','EiB','ZiB','YiB']
    u = -1
    while True:
        bytes /= thresh
        u+=1
        if not (Math.abs(bytes) >= thresh and u < units.length - 1):
            break
    return bytes.toFixed(1)+' '+units[u], u+1

def img_field(elem):
    txt = jQuery(elem).val().replace( __new__(RegExp("^.*[\\\ /]")), '')
    jQuery(elem).closest('label').find('.upload').html(txt)

    if elem.files and elem.files[0]:
        file_name = elem.files[0].js_name
        ext = [ '.jpeg', '.jpg', '.svg', '.gif', '.png']
        test = False
        for pos in ext:
            if pos in file_name.lower():
                test= True
                break
        if test:
            reader = __new__(FileReader())

            def _onload(e):
                nonlocal elem
                x = jQuery(elem).closest('label').find('.img')
                if x.length>0:
                    x.remove()
                img = jQuery("<img class='img' />")
                img.insertAfter(jQuery(elem).closest('label').find('input'))
                img.attr('src', e.target.result)

            reader.onload = _onload
            reader.readAsDataURL(elem.files[0])
        else:
            x = jQuery(elem).closest('label').find('.img')
            if x.length > 0:
                x.remove()

            size, level = humanFileSize(elem.files[0].size, True)
            ext = elem.files[0].js_type + "<br><span class='size_level_"+level+ "'>"+ size + "</span>"

            img = jQuery("<p class='img' />")
            img.insertAfter(jQuery(elem).closest('label').find('input'))
            img.html(ext)


window.img_field = img_field
