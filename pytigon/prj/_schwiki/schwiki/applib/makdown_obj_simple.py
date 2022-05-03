import base64
from PIL import Image
import io
import os
import collections

from pytigon_lib.schindent.indent_markdown import (
    BaseObjRenderer,
    IndentMarkdownProcessor,
    register_obj_renderer,
)
from pytigon_lib.schfs.vfstools import get_temp_filename

from pytigon_lib.schdjangoext.widgets import ImgFileInput
from django import forms


class ImgForm(forms.Form):
    from pytigon_lib.schdjangoext.widgets import ImgFileInput

    img1 = forms.ImageField(label="Image 1", required=False, widget=ImgFileInput)
    crop1 = forms.BooleanField(label="Crop", required=False, initial=True)
    desc1 = forms.CharField(label="Description", required=False)
    img1class = forms.CharField(label="CSS class", required=False)
    img1style = forms.CharField(label="Style", required=False)
    img2 = forms.ImageField(label="Image 2", required=False, widget=ImgFileInput)
    crop2 = forms.BooleanField(label="Crop", required=False, initial=True)
    desc2 = forms.CharField(label="Description", required=False)
    img2class = forms.CharField(label="CSS class", required=False)
    img2style = forms.CharField(label="Style", required=False)
    img3 = forms.ImageField(label="Image 3", required=False, widget=ImgFileInput)
    crop3 = forms.BooleanField(label="Crop", required=False, initial=True)
    desc3 = forms.CharField(label="Description", required=False)
    img3class = forms.CharField(label="CSS class", required=False)
    img3style = forms.CharField(label="Style", required=False)
    img4 = forms.ImageField(label="Image 4", required=False, widget=ImgFileInput)
    crop4 = forms.BooleanField(label="Crop:", required=False, initial=True)
    desc4 = forms.CharField(label="Description", required=False)
    img4class = forms.CharField(label="CSS class", required=False)
    img4style = forms.CharField(label="Style", required=False)

    component_view_type = forms.CharField(max_length=16)
    img_view_type = forms.CharField(max_length=16)

    jpeg = forms.BooleanField(label="Jpeg", required=False, initial=False)
    quality = forms.ChoiceField(
        label="Quality",
        required=False,
        initial="1",
        choices=(("0", "standard"), ("1", "good"), ("2", "best")),
    )


class ImgObjRenderer(BaseObjRenderer):

    @staticmethod
    def get_info():
        return { "name": "img", "title": "Image", "icon": "fa fa-picture-o", "show_form": True,}

    def get_edit_form(self):
        return ImgForm

    def convert_form_to_dict(self, form, old_dict=None):
        def calc_sizes(component_view_type, no, vertical=True):
            if component_view_type == "1000":
                if vertical:
                    return (100, 100 * 16 / 16)
                else:
                    return (100, 100 * 9 / 16)
            elif component_view_type == "1200":
                ret = calc_sizes("1000", 1, vertical)
                return (ret[0] / 2, ret[1] / 2)
            elif component_view_type == "1230":
                ret = calc_sizes("1000", 1, vertical)
                return (ret[0] / 3, ret[1] / 3)
            elif component_view_type == "1234":
                ret = calc_sizes("1000", 1, vertical)
                return (ret[0] / 4, ret[1] / 4)
            elif component_view_type == "1213":
                if no == 1:
                    # return (39,69)
                    return (39, 61.7)
                else:
                    return (61, 34)
            elif component_view_type == "1232":
                if no == 2:
                    return (39, 69)
                else:
                    return (61, 34)
            elif component_view_type == "4321":
                if vertical:
                    return (50, 50 * 16 / 9)
                else:
                    return (50, 50 * 9 / 16)
            elif component_view_type == "1423":
                if vertical:
                    return (70, 70 * 16 / 9)
                else:
                    return (70, 70 * 9 / 16)

        def _encode(bstr, crop, component_view_type, no, jpeg=False, quality="0"):
            img = Image.open(io.BytesIO(bstr))
            if img.size[0] > img.size[1]:
                vertical = False
            else:
                vertical = True

            if quality == "2":
                z = 40
            elif quality == "1":
                z = 20
            else:
                z = 10

            ret = calc_sizes(component_view_type, no, vertical)
            max_dx = _dx = int(ret[0] * z)
            max_dy = _dy = int(ret[1] * z)

            max_scale = max(img.size[0] / max_dx, img.size[1] / max_dy)
            min_scale = min(img.size[0] / max_dx, img.size[1] / max_dy)
            if crop:
                scale = min_scale
            else:
                scale = max_scale

            if scale > 1:
                img = img.resize(
                    (int(img.size[0] / scale), int(img.size[1] / scale)),
                    Image.ANTIALIAS,
                )
                if crop:
                    left = (img.size[0] - max_dx) / 2
                    top = (img.size[1] - max_dy) / 2
                    right = (img.size[0] + max_dx) / 2
                    bottom = (img.size[1] + max_dy) / 2
                    img = img.crop((left, top, right, bottom))

            dx2 = int(max_dx * scale)
            dy2 = int(max_dy * scale)

            img2 = Image.new("RGB", (dx2, dy2), (255, 255, 255))
            offset = (int((dx2 - img.size[0]) / 2), int((dy2 - img.size[1]) / 2))
            img2.paste(img, offset)
            img = img2

            img_out = io.BytesIO()
            if jpeg:
                img.save(img_out, format="JPEG")
            else:
                img.save(img_out, format="PNG")
            return base64.b64encode(img_out.getbuffer()).decode("utf-8")

        ret = {}
        component_view_type = form.cleaned_data["component_view_type"]

        jpeg = form.cleaned_data["jpeg"]
        quality = form.cleaned_data["quality"]

        for img, crop, no in [
            ("img1", "crop1", 1),
            ("img2", "crop2", 2),
            ("img3", "crop3", 3),
            ("img4", "crop4", 4),
        ]:
            if form.cleaned_data[img]:
                ret[img] = _encode(
                    form.cleaned_data[img].read(),
                    form.cleaned_data[crop],
                    component_view_type,
                    no,
                    jpeg,
                    quality,
                )
            else:
                if old_dict:
                    if img in old_dict:
                        ret[img] = old_dict[img]
        for i in range(1, 5):
            ret["desc%d" % i] = form.cleaned_data["desc%d" % i]
            ret["crop%d" % i] = form.cleaned_data["crop%d" % i]
            ret["img%dclass" % i] = form.cleaned_data["img%dclass" % i]
            ret["img%dstyle" % i] = form.cleaned_data["img%dstyle" % i]

        ret["component_view_type"] = component_view_type
        ret["img_view_type"] = form.cleaned_data["img_view_type"]
 
        ret["jpeg"] = jpeg
        ret["quality"] = quality
        ret["json_update"] = True

        return ret

    def gen_context(self, param, lines, output_format, parent_processor):
        context = {"param": param}
        cvt = param["component_view_type"]
        
        Element = collections.namedtuple("Element", "type data css_class style")
        elements = []
        img_css_class = ""

        def img_process(no, css_class):
            try:
                css_class2 = (
                    param["img%dclass" % no] if param["img%dclass" % no] else css_class
                )
                imgstyle = param["img%dstyle" % no]
                elm = Element(
                    "img",
                    [param["img%d" % no], param["desc%d" % no]],
                    css_class2,
                    imgstyle,
                )
                elements.append(elm)
            except:
                pass

        if cvt == "1000":
            if not img_css_class:
                img_css_class = "col col-12"
            img_process(1, img_css_class)
        elif cvt == "1200":
            img_css_class = "col col-6"
            img_process(1, img_css_class)
            img_process(2, img_css_class)
        elif cvt == "1230":
            img_css_class = "col col-4"
            img_process(1, img_css_class)
            img_process(2, img_css_class)
            img_process(3, img_css_class)
        elif cvt == "1234":
            img_css_class = "col col-3"
            img_process(1, img_css_class)
            img_process(2, img_css_class)
            img_process(3, img_css_class)
            img_process(3, img_css_class)
        elif cvt == "1213":
            if not img_css_class:
                img_css_class = "col col-12"
            elements.append(Element("data", "<div class='%s'>" % img_css_class, "", ""))
            elements.append(
                Element(
                    "data",
                    "<table width='100%' class='i1213'><tr><td rowspan='2' width='42%' class='t1'>",
                    "",
                    "",
                )
            )
            img_process(1, "")
            elements.append(Element("data", "</td><td class='t2'>", "", ""))
            img_process(2, "")
            elements.append(Element("data", "</td></tr><tr><td class='t3'>", "", ""))
            img_process(3, "")
            elements.append(Element("data", "</td></tr></table>", "", ""))
            elements.append(Element("data", "</div>", "", ""))
        elif cvt == "1232":
            if not img_css_class:
                img_css_class = "col col-12"
            elements.append(Element("data", "<div class='%s'>" % img_css_class, "", ""))
            elements.append(
                Element(
                    "data",
                    "<table width='100%' class='i1232'><tr><td class='t1'>",
                    "",
                    "",
                )
            )
            img_process(1, "")
            elements.append(
                Element("data", "</td><td class='t2' rowspan='2' width='42%'>", "", "")
            )
            img_process(2, "")
            elements.append(Element("data", "</td></tr><tr><td class='t3'>", "", ""))
            img_process(3, "")
            elements.append(Element("data", "</td></tr></table>", "", ""))
            elements.append(Element("data", "</div>", "", ""))
        elif cvt == "4321" or cvt == "1423":
            if not img_css_class:
                img_css_class = "col col-12"
            elements.append(Element("data", "<div class='%s'>" % img_css_class, "", ""))
            elements.append(
                Element(
                    "data",
                    "<table width='100%%' class='i%s'><tr><td class='t1'>" % cvt,
                    "",
                    "",
                )
            )
            img_process(1, "")
            elements.append(Element("data", "</td><td class='t2'>", "", ""))
            img_process(2, "")
            elements.append(Element("data", "</td></tr><tr><td class='t3'>", "", ""))
            img_process(3, "")
            elements.append(Element("data", "</td><td class='t4'>", "", ""))
            img_process(4, "")
            elements.append(Element("data", "</td></tr></table>", "", ""))
            elements.append(Element("data", "</div>", "", ""))
        context["elements"] = elements
        return context

    def get_renderer_template_name(self):
        return "schwiki/img_wikiobj_view.html"

    def get_edit_template_name(self):
        return "schwiki/img_wikiobj_edit.html"


register_obj_renderer("img", ImgObjRenderer)


class SvgForm(forms.Form):
    src = forms.CharField(label="Text", widget=forms.Textarea, required=False)
    svgsize = forms.CharField(label="Svg size", required=False)
    svgclass = forms.CharField(label="Svg CSS class", required=False)
    svgstyle = forms.CharField(label="Svg style", required=False)
    text = forms.CharField(label="Text", widget=forms.Textarea, required=False)
    textright = forms.BooleanField(label="Text on the right", required=False)
    textclass = forms.CharField(label="CSS class", required=False)
    textstyle = forms.CharField(label="Style", required=False)


class SvgObjRenderer(BaseObjRenderer):

    @staticmethod
    def get_info():
        return { "name": "svg", "title": "Svg", "icon": "fa fa-puzzle-piece", "show_form": True, }

    def get_edit_form(self):
        return SvgForm

    def get_renderer_template_name(self):
        return "schwiki/svg_wikiobj_view.html"


register_obj_renderer("svg", SvgObjRenderer)


class VideoForm(forms.Form):
    src = forms.CharField(label="Source video address", required=True)
    poster = forms.CharField(label="Poster file address", required=False)
    controls = forms.BooleanField(label="Controls?", required=False, initial=True)
    videosize = forms.CharField(label="Video size", required=False)
    videoclass = forms.CharField(label="Video CSS class", required=False)
    videostyle = forms.CharField(label="Video style", required=False)
    text = forms.CharField(label="Text", widget=forms.Textarea, required=False)
    textright = forms.BooleanField(label="Text on the right", required=False)
    textclass = forms.CharField(label="CSS class", required=False)
    textstyle = forms.CharField(label="Style", required=False)


class VideoObjRenderer(BaseObjRenderer):

    @staticmethod
    def get_info():
        return { "name": "video", "title": "Video", "icon": "fa fa-video-camera", "show_form": True,}

    def get_edit_form(self):
        return VideoForm

    def gen_context(self, param, lines, output_format, parent_processor):
        context = {"param": param}
        if "src" in param:
            x = param["src"].split(";")
            sources = []
            tracks = []
            for pos in x:
                if pos.lower().endswith(".webm"):
                    sources.append((pos, "video/webm;"))
                if pos.lower().endswith(".mp4"):
                    sources.append((pos, "video/mp4;"))
                if ".vtt" in pos.lower():
                    name = pos
                    label = "English subtitles"
                    srclang = "en"
                    default = False
                    kind = "subtitles"
                    if "," in pos:
                        p = pos.split(",")
                        name = p[0]
                        label = p[1]
                        if len(p) > 2:
                            srclang = p[2]
                            if len(p) > 3:
                                if p[3]:
                                    default = 3
                                if len(p) > 4:
                                    kind = p[4]
                    tracks.append((name, label, srclang, default, kind))
            context.update({"sources": sources, "tracks": tracks})
        return context

    def get_renderer_template_name(self):
        return "schwiki/video_wikiobj_view.html"


register_obj_renderer("video", VideoObjRenderer)


PLOT_OBJ_RENDERER_FORM = """
name//Plot name
width
height
"""

class PlotObjRenderer(BaseObjRenderer):

    @staticmethod
    def get_info():
        return { "name": "plot", "title": "Plot", "icon": "fa fa-line-chart", "show_form": True,}

    def get_edit_form(self):
        return PLOT_OBJ_RENDERER_FORM

    def get_renderer_template_name(self):
        return "schwiki/plot_wikiobj_view.html"


register_obj_renderer("plot", PlotObjRenderer)


class ReadMoreObjRenderer(BaseObjRenderer):

    @staticmethod
    def get_info():
        return { "name": "read_more", "title": "Read more", "icon": "fa fa-eye-slash", "show_form": False,}
    
    def render(self, param, lines, output_format, parent_processor):
        return "<div class='read_more'></div>"


register_obj_renderer("read_more", ReadMoreObjRenderer)


