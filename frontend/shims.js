import * as moment from 'moment';
globalThis.moment = moment;

import { vsprintf, sprintf } from 'sprintf'
globalThis.vsprintf = vsprintf
globalThis.sprintf = sprintf


import { jQuery } from 'jquery';

globalThis.jQuery = jQuery;
globalThis.$ = jQuery;

jQuery.isFunction = function(obj) {
    return typeof obj === 'function';
}
jQuery.trim = function(obj) {
    return obj.trim();
}

jQuery.type = function(obj) {
    return typeof obj;
}

jQuery.isArray = Array.isArray;

import * as bootstrap from 'bootstrap';
globalThis.bootstrap = bootstrap;
import * as Ladda from 'ladda';
globalThis.Ladda = Ladda;
import Swal from 'sweetalert2'
globalThis.Swal = Swal

