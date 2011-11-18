# -----------------------------------------------------------------------------
#    Ultra Blog - Data type base blog application for Vanda platform
#    Copyright (C) 2011 Behnam AhmadKhanBeigi ( b3hnam@gnu.org)
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
# -----------------------------------------------------------------------------

from django.utils.translation import ugettext as _

from base import PostType, post_types
from forms import TextTypeForm, ImageTypeForm


class TextType(PostType):
    name = "text"
    verbose_name = _("Text Post")
    admin_form = TextTypeForm


## class SoundType(PostType):
##     name = "sound"
##     verbose_name = _("Sound Post")
##     admin_form = SoundTypeForm


class ImageType(PostType):
    name = "image"
    verbose_name = _("Image Post")
    admin_form = ImageTypeForm

post_types.register(TextType)
post_types.register(ImageType)
