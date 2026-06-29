"""
Widget utility functions for form fields and UI components.

Provides helper functions for file input display, human-readable
file sizes, and image preview functionality.
"""


def humanFileSize(bytes, si):
    """Convert a byte count into a human-readable file size string.

    Args:
        bytes: The number of bytes (numeric).
        si: If True, use SI units (1000-based: kB, MB, ...).
            If False, use IEC units (1024-based: KiB, MiB, ...).

    Returns:
        tuple: (formatted_size_string, unit_level)
            - formatted_size_string: e.g. "1.5 MB"
            - unit_level: 0-based index into the unit array (0 = B, 1 = kB/KiB, ...)
    """
    thresh = 1000 if si else 1024

    # If smaller than threshold, just return bytes
    if Math.abs(bytes) < thresh:
        return bytes + " B", 0

    if si:
        units = ["kB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]
    else:
        units = ["KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB"]

    u = -1
    while True:
        bytes /= thresh
        u += 1
        if not (Math.abs(bytes) >= thresh and u < units.length - 1):
            break

    return bytes.toFixed(1) + " " + units[u], u + 1


def img_field(elem):
    """Handle file input change event for image/file upload fields.

    Displays a preview of the selected file:
    - For image files (jpeg, jpg, svg, gif, png): shows an img thumbnail.
    - For other files: shows file name, MIME type, and size.

    Args:
        elem: The file input DOM element that triggered the change event.
    """
    # Update the upload label text with the file name
    txt = jQuery(elem).val().replace(RegExp(r"^.*[\\\ /]"), "")
    jQuery(elem).closest("label").find(".upload").html(txt)

    if elem.files and elem.files[0]:
        file_name = elem.files[0].name
        ext = [".jpeg", ".jpg", ".svg", ".gif", ".png"]

        # Check if the file has an image extension
        test = False
        for pos in ext:
            if pos in file_name.lower():
                test = True
                break

        if test:
            # Image file: read as data URL and display as <img>
            reader = FileReader()

            def _onload(self, e):
                nonlocal elem
                # Remove any existing preview image
                x = jQuery(elem).closest("label").find(".img")
                if x.length > 0:
                    x.remove()
                # Insert new preview image after the file input
                img = jQuery("<img class='img' />")
                img.insertAfter(jQuery(elem).closest("label").find("input"))
                img.attr("src", e.target.result)

            reader.onload = _onload
            reader.readAsDataURL(elem.files[0])
        else:
            # Non-image file: remove any existing image preview
            x = jQuery(elem).closest("label").find(".img")
            if x.length > 0:
                x.remove()

            # Show file metadata: name, type, size
            size, level = humanFileSize(elem.files[0].size, True)
            ext = (
                elem.files[0].name
                + "<br/>"
                + elem.files[0].type
                + "<br /><span class='size_level_"
                + level
                + "'>"
                + size
                + "</span>"
            )

            img = jQuery("<p class='img' />")
            img.insertAfter(jQuery(elem).closest("label").find("input"))
            img.html(ext)


window.img_field = img_field
