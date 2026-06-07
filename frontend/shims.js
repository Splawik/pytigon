
import * as jQuery from 'jquery'
globalThis.jQuery = jQuery.jQuery
globalThis.$ = jQuery.jQuery
import initSelect2 from 'select2';
initSelect2(jQuery); 

import * as moment from 'moment';
globalThis.moment = moment;

import { vsprintf, sprintf } from 'sprintf'
globalThis.vsprintf = vsprintf
globalThis.sprintf = sprintf

import * as Cookies from 'js-cookie';
globalThis.Cookies = Cookies;
import * as bootstrap from 'bootstrap';
globalThis.bootstrap = bootstrap;
import * as IMask from 'imask';
globalThis.IMask = IMask;
import * as Ladda from 'ladda';
globalThis.Ladda = Ladda;
import Swal from 'sweetalert2'
globalThis.Swal = Swal

import { Idiomorph } from 'idiomorph';
globalThis.Idiomorph = Idiomorph;
import { PerfectScrollbar } from 'om-perfect-scrollbar';
globalThis.PerfectScrollbar = PerfectScrollbar;
